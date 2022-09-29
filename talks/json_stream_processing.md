# JSON Stream Processing

Original source is found at https://github.com/jbee/json-streama/blob/main/PRESENTATION.md

## Stream-What?

Here: about processing JSON input, for example a data import 

Typical basic case:
```json
{
  "header": {
    "id": "xyz",
    "name": "collection"
  },
  "entries": [{...}, {...}, ...]
}
```

#### Mapping 

    JSON => Objects => process(Objects)

vs


#### Streaming 
(stream processing)

    JSON => process(JSON*)

`*`: a access "wrapper" API that reads the input as they are processed

could also think of it as: 

    JSON => new Wrapper(JSON) => process(Wrapper) 





## Why Streaming?  - Pros & Cons

#### Mapping

**Pros**:

* object graph as API
  * familiar 
  * order does not matter
  * navigate graph freely 
  * DTOs (high re-usability)
  * straight forward (not very error-prone)
  * easy(er) to maintain 😍
* well-supported in common libraries (e.g. jackson)
  * usually easy to extend and customise the mapping

**Cons**:

* object graph 
  * larger JSON => larger graph => more memory => `OutOfMemoryError` 🥴
  * slow(er) 😴
  * needs guard against too large input


#### Streaming

**Pros**:

* no intermediate representation
  * can handle almost any size input (GB or even beyond) 😎
  * fast(er)
  * no guard against large input required

**Cons**:

* usually library specific or hand-crafted API
* usually requires custom coded processing
  * 1-off solution (low re-usability) 
  * not straight forward (error-prone)
  * hard(er) to maintain 🤯
* in streams order is significant by nature
* streams by nature are transient

----

#### Wouldn't it be nice to have the best of both worlds?






## What makes stream processing difficult?

#### 1. Order Matters
_What we are used to_: 
    
* for JSON order of object members does not matter

_Reality_: 

* In streams order of object members matters
* (or the code gets very complicated and still only true for primitive members) 


#### 2. Transient Data
_What we are used to in OO_:

* Data can be accessed at any time and does not change unless we do that change ourselves

_Reality_:

* Stream values are only present at that point in the stream.
* Remembering previous values must be coded for each case. 





## Stream Processing JSON with Jackson

For example: https://github.com/dhis2/dhis2-core/pull/9574/files

Jackson's "Wrapper" is `JsonParser`

**Properties**:

* token based (object-start, object-end, ...)
* very low level
* quite error-prone
* quite hard to understand and maintain
* 1-off solution per input JSON format
* order very important => difficult to code
* internal state tracking nightmare 😱

Pseudo code:
```java
while (parser.hasTokens()) {
  String value = null;
  switch (parser.nextToken()) {
    case OBJECT_START: // what state are we in again?
    case STRING: // what state are we in again?
      value = parser.nextString();
  } 
  // what to do with the value now? 
  // and... what state are we in again?
}
```
**what is the state in the parser???**

**what is the state of the processing code variables???**

<center><img src="https://i.kym-cdn.com/photos/images/newsfeed/000/498/390/4a8.jpg" width="250" /></center>


## Wouldn't it be nice...

... to have best of both worlds?

#### Wishlist
* fast
* low-footprint (memory, CPU)
* can handle large input
* easy to understand
* easy to use and extend
* re-usable "objects", composable
* "OO think" and Java types
* order is (mostly) irrelevant (in streams it is by nature)
* values are (more) stable (again, in streams the can't by nature)
* no internal and variable state tracking in our brains
* no JSON level concerns in our code => we want to deal with objects


<center><img src="https://memegenerator.net/img/instances/71645180/computer-says-no.jpg" width="250" /></center>



## 1 ½ Magic Trick

Fake it 'till you make it 😎

Let's just pretend we have objects...

Use interfaces to model an object graph API:

<table><tr><td>


```java
interface Payload {
  Header header();
  Stream<Entry> entries();
}
interface Header {
  String id();
  String name();
}
interface Entry {
  //...
}
```

</td>
<td valign="top">

```json
{
  "header": {
    "id": "xyz",
    "name": "collection"
  },
  "entries": [{...}, {...}, ...]
}
```

</td></tr></table>


Usage:
```java
Payload root = JsonStream.ofRoot(Payload.class, inputStream);
Header header = root.header();
root.entries().forEach(entry -> {
  //...
});
```

* 1 "auto" implements using Java `Proxy`
* ½ order and reading is given/driven by usage (method calls on proxy API)

## Yeah, but...

* can primitive fields be accessed in a random order? **Yes**
* can there be multiple stream processed collections? **Yes**
* can stream processing be nested? **Yes**
* can the JSON contain members that are not "mapped"? **Yes**
* can stream processing be applied to JSON arrays and object "maps"? **Yes**
* can the root be an array or object "map"? **Yes**
* can stream processed entries use other Java types than `Stream`? **Yes**, supported are:
  * `Stream`
  * `Iterator`
  * `Consumer`

```java
interface Payload {

  Stream<Entry> entries();

  Iterator<Entry> entries();

  void entries(Consumer<Entry> forEachEntry);
}
```




## Object "Maps" vs. Arrays

Map-of-objects style:
```json
[{ "1": {"name": "Track 1"}, "2": {"name": "Track 2"}}]
``` 
can be mapped directly to `Stream<Track>`:
```java
interface Track {
  @JsonProperty(key = true)
  int no();
  String name();
}
```
still, this array-of-objects style input will also work:
```json
[{"no": 1, "name": "Track 1"}, {"no": 2, "name": "Track 2"}]
``` 

also a property named `key` does not require the annotation.


## Managing Expectations

For example, tracks of a music album:
```json
{"tracks": [{"name": "A"}, {"name": "B"}]}
```

Make properties mandatory using `required`:

```java
interface Track {
  @JsonProperty(required = true)
  String name();
}
```

Restricting size using `minOccur` and `maxOccur`:

```java
interface Album {

  @JsonProperty(minOccur = 1, maxOccur = 25)
  Stream<Track> tracks();
}
```



## Or else...

If a value is not in the JSON input, return a default

Simply give the "getter" a parameter of the return type:

```java
interface Track {
  String name(String defaultValue);
}

String name = track.name("unknown");
```


## Next Level "Yeah, but..."

* is malformed JSON detected? **Yes**, => exception
* are accidental "out of order" usages of proxy objects detected? **Yes**, => exception
* are stream members out of order detected? **Yes**, => exception
* can the supported Java types be extended? **Yes** (WIP)

```
______                       __  
|  _  \                     /  |
| | | |___ _ __ ___   ___   `| |
| | | / _ \ '_ ` _ \ / _ \   | |
| |/ /  __/ | | | | | (_) | _| |_
|___/ \___|_| |_| |_|\___/  \___/
```



## How are we doing?

* [x] fast
* [x] low-footprint (memory, CPU)
* [x] can handle large input
* [x] easy to understand
* [x] easy to use and extend
* [x] re-usable "objects", composable
* [x] "OO think" and Java types
* [x] order is (mostly) irrelevant (in streams it is by nature)
* [x] values are (more) stable (again, in streams the can't by nature)
* [x] no internal and variable state tracking in our brains
* [x] no JSON level concerns in our code => we want to deal with objects

Noice!


## Implementation Notes

* **Proxies**: creates only one per member (independent of the number of items in a stream)
* **Simple Values**: are stored and accessed via index access in a reused array per member
* **Parser**:
  * zero look ahead 
  * "self-suspending" PEG parser

```
______                       _____ 
|  _  \                     / __  \
| | | |___ _ __ ___   ___   `' / /'
| | | / _ \ '_ ` _ \ / _ \    / /  
| |/ /  __/ | | | | | (_) | ./ /___
|___/ \___|_| |_| |_|\___/  \_____/
```





## Questions?


Work in progress:

* `IntStream`, `LongStream`, ...
* `Stream<String>`, `Stream<Date>`, ...
* `List<String>`, `Map<String,Integer>` ...
* manual skipping  