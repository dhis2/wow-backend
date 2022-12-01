# Controller Endpoint Guide
A brief overview of Dos and Don'ts of controller endpoint design.


## Path
A good example for "one path per operation":

```java
class EntryController {
  @GetMapping(value = "/{id}", produces = "application/json")
  Entry getEntryJson( @PathVariable String id ) {
      //...
  }

  @GetMapping(value = "/{id}.xml", produces = "application/xml")
  Entry getEntryXml( @PathVariable String id ) {
    //...
  }
}
```

**Do**
* 🚀 do use a unique path per operation; even: different media type => different operation => different path
* 🚀 do use the "nice" path for JSON or plain text, use suffixes for XML, CSV, ...

**Avoid**
* ❌ avoid multi-media-type endpoint methods
* ❌ avoid mapping based on request `Content-Type` (`@GetMapping( consumes = "text/csv" )`)
* ❌ avoid mapping based on request `Accept` (`@GetMapping( produces = "text/csv" )`)
* ❌ avoid mapping based on presence of parameters (`@GetMapping( params = "x" )`)
* ❌ avoid mapping based on presence of headers (`@GetMapping( headers = "x" )`)

To clarify: do use `consumes` and `produces` but not as a means to make the operation unique.
The path alone should already be unique.


## Parameters

**Do**
* 🚀 do use dedicated but minimal parameter objects (when in doubt overuse, details see below)
* 🚀 do annotate `String` typed parameters with `@OpenApi.Param` if a more specific type can be given

**Avoid**
* ❌ avoid reading from `HttpServletRequest`
* ❌ avoid reading parameters via `Map<String, String>`
* ❌ avoid adding the super-set of all use case to a parameter object,
  either use different parameter objects or use the intersection of common parameters

### Parameter Objects
A good example for parameter object usage:

```java
@Data
@OpenApi.Shared
class EntryQueryParams {
    int page = 1;
    int pageSize = 50;
    String filter;
}

class EntryController {
    @GetMapping( "/entries" )
    List<Entry> queryEntries(EntryQueryParams params, @RequestParam boolean special) {
        EntryQuery query = EntryQuery.from(params)
            .withSpecial(special)
            .withUser(currentUser);
        return entryQueryService.runQuery(query);
    }
}
```

**Do**
* 🚀 do use when a set of parameters is occurring in more than one endpoint (keep inheritance in mind) or when parameters belong to a common role
* 🚀 do include only reoccurring parameters
* 🚀 do create a dedicated params class only used on controller level (API input)
* 🚀 do use `@Data`
* 🚀 do initialise fields with default values where applicable
* 🚀 do prefer primitives with default over wrappers
* 🚀 do use enum typed fields (not `String`) for `enum` values
* 🚀 do use `@OpenApi.Shared` on parameter object types used by multiple endpoints

**Avoid**
* ❌ avoid reusing query/params defined outside webapi module
* ❌ avoid including fields that are not provided via user input (e.g. current user and such)
* ❌ avoid using service level parameter objects (these often use non input types and have non input fields)
* ❌ avoid including persisted types in parameter objects (consider creating a dedicated object for expected input)


## Responses

**Do**
* 🚀 do prefer plain return values (exceptions: streaming, field filtering, performance)
* 🚀 do use `ResponseEntity` wrapper only in case further response properties need to be set
* 🚀 do return `204 NO_CONTENT` status when there is no response body (not default `200 OK`)
* 🚀 do use `@OpenApi.Response` to declare how a response looks like in case it is directly written to output stream

**Avoid**
* ❌ avoid writing directly to `HttpServletResponse` output stream (exceptions: streaming, field filtered, performance and alike)

