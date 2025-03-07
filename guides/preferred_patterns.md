# Preferred Coding Patterns

The presented patterns are meant as a general guide but should not be understood 
as rules to follow blindly or use as a knockout argument or sledgehammer 
approach to everything. Each problem deserves to be judged individually 
considering all its aspects and complexity when choosing a fitting solution. 

However, when in doubt which approach might be more fitting the guides provide
a reasoning and direction with the goal of a more uniform codebase which can
benefit from the advantages that emerge when using the described patterns.

#### Overview
| Type                | Pattern                                | Prefer | Over                    |
|---------------------|----------------------------------------|---------------------|-------------------------|
| Avoid `null`        | Use `@Nonnull` in APIs                 | annotate bit too much | annotate too little |
| Prefer Immutability | Consider collections as _unmodifiable_ | copy before modification | copy before returning |

## Avoid Null

### Use `@Nonnull` in APIs
Using an annotation to communicate expectations (parameters) and guarantees
(return values) in regard to whether or not they can be `null` helps both
programmers and static analysis tools to avoid NPEs. 

Heavy use of extra information can also clutter the code and make it less
readable. To strike a balance it is recommended to use 
`javax.annotation.Nonnull` (and `javax.annotation.CheckForNull`) 
first and foremost in APIs for both method parameters and return values. 

Another useful example are private helper methods that deal with mutable
state and low level details, where some methods have to handle `null` and 
others don't, adding annotations helps to draw the line between the two.

While it is useful to know that return values can be `null` by annotating them
with `@CheckForNull` the goal for the codebase should be to keep the usage low.
Before using `@CheckForNull` it is recommended to consider if `null` can be
avoided instead or if the use of `Optional` could improve the API.

**Goals:**
* communicate `null` dependent behaviour
* enable static analysis
* avoid adding too much annotation "clutter"

**Exceptions:**
* constructors of spring injected beans do not benefit much from the annotation 
  as spring will throw exception for missing dependencies


## Prefer Immutability
Manipulation of mutable state is hard to follow and opens for permutation of
possibilities that programmers need to consider. This unnecessarily creates a
larger surface for error. Immutability as a concept should help keeping
effects local,easy to follow and think through. 

The idea of immutability can take many forms some of which are presented here 
in greater detail. In Java this usually is not all are black and white banning
mutable state altogether. Typically, mutation is limited to a small scope that 
is easy(er) to think though and on the boundaries immutability is assumed
(parameters) or ensured (return values).

### Consider Collections as _unmodifiable_
When working with collections errors can arise from trying to manipulate an
_unmodifiable_ collection. One way to defend against this is to make copies of
collections to be sure they can be modified by a consumer. This often results
in collections being copied multiple times over as they pass through the layers
of abstractions and the application architecture. The other approach to this
is to generally consider any collection that wasn't created within or as part 
of the code that wants to modify the collection as _unmodifiable_. 

In practice this means any collection received from a non-private method call or
as parameter to a method should be considered _unmodifiable_ and copied once
where the algorithm needs a modifiable collection.

**Goals:** 
* keep copying of collections to a minimum
* make code easy to understand and reason about
* make code about the essential problem (less ceremony/clutter)

**Exceptions** (known mutable collections)**:**
* collections of hibernate entities in DHIS2 entities
* collections created in or as part of the algorithm (same method, 
  other `private` helper methods and alike)

**Also:**
* consider using alternative algorithms that can avoid manipulation, 
  e.g. `stream().map(...)` and alike.


## Declarative Service API
The API offered by the service layer should be declarative and communicate in
terms of concepts that have a counterpart on the HTTP level.

**Goals:**
* keep the controller level code minimal
* make it easy to call services
* prevent breaking abstraction by mixing input (what to do; intent) with processing state (how to do it; solution)
* fail with checked exceptions that directly map to HTTP status codes

**Follow:**
* Use UIDs (not objects) as inputs
* throw checked exceptions from the `org.hisp.dhis.feedback` package
* use `ErrorCode`s to add context to exceptions

**Avoid:**
* avoid asking for objects as input that are hard to obtain (e.g. DB or managed objects), use symbols instead (like a UID)
* avoid mutating the input (what to do) inside the service
* avoid creating more checked exceptions (unless they are for a used but not yet covered HTTP response code)

**Exceptions:**
* internally services should use subtypes of `RuntimeException` in the low level code
  * reuse existing ones like `IllegalArgumentException`, `NoSuchElementException` where suitable,
  * create new ones in complex domains when needed
