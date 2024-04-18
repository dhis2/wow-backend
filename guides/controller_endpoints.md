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
* 🚀 do use a dedicated path for parameters that change either the result or how the action is performed in a fundamental way
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

**Remember**
* 💡 parameter based mapping (`@GetMapping( params = "x" )`) results in a mapping error when more than one of such endpoints matches
* 💡 parameter based mapping (`@GetMapping( params = { "a", "b" } )`) match when **all** parameters are present/match

### Parameter Objects
A good example for parameter object usage:

```java
@Data
@OpenApi.Shared
class EntryQueryParams {
    int page = 1;
    int pageSize = 50;
    String filter;
    CustomField custom = CustomField.empty();
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

## Parameters binding

Spring will try to convert parameters from String into the proper type using a `PropertyEditor` if available, otherwise a `Converter`. `PropertyEditor`s are registered and bind to a class in `CrudControllerAdvice.initBinder(WebDataBinder binder)` method. `Converter`s are registered in `WebMvcConfig.addFormatters(FormatterRegistry registry)` method.
`PropertyEditor`s and `Converter`s work in a similar way but in different context, the former is used only in Spring web MVC context to bind request parameters, the latter is a global converter that can be used in any layer of the system.

Spring raises a `MethodArgumentTypeMismatchException` if the conversion of a `@RequestParam` fails. Spring raises a `BindException` if the conversion of a parameter object field fails. Both exceptions are handled in `CrudControllerAdvice`.

Create a `PropertyEditor` to properly validate a custom field and to expose a relevant validation message.
A `PropertyEditor` takes the parameter as a string as input and it tries to convert to the proper type, if it cannot convert it throws an `IllegalArgumentException` with a relevant message that is shown to the client.
`PropertyEditor`s should throw an `IllegalArgumentException` when the parameter is null or an empty string because this happens when the parameter is specified without value in the URL like `/entries?page` or `/entries?page=`

**Do**
* 🚀 do prefer primitives with defaults over wrappers
* 🚀 do use enum typed fields (instead of `String`) for `enum` values
* 🚀 do initialise fields with default values where applicable
* 🚀 create `PropertyEditor` for custom fields and throw an exception if the source is null or an empty string

**Avoid**
* ❌ avoid creating a `Converter` for a parameter as it will not handle the empty case in the proper way

## Authorisation Checking
We used to use `@PreAuthorize` on endpoints when we wanted to enforce a specific `Authority` for a `User` on a Specific endpoint. e.g.  
`@PreAuthorize("hasRole('ALL') or hasRole('F_DATAVALUE_ADD')")`  

This has been replaced with a type-safe alternative `@RequiresAuthority` e.g.  
`@RequiresAuthority(anyOf = F_DATAVALUE_ADD)`  
- type-safe (using `Authorities`)
- can use at class or method level
- `ALL` Authority is automatically checked (no need to pass in)
- when used, it will advise which `Authorities` are missing in the response

## Troubleshooting
What to do if the API is already release in a way that causes trouble?

#### How to add additional parameters to an inherited method?
* Override the inherited method and add a mapping that is unlikely to match, e.g. `@GetMapping( params = "doesnotexist" )`
* Annotate the overridden inherited method with `@OpenApi.Ignore`
* Implement a new method that has the same path as the inherited method
* Add the "inherited" and the additional parameters to the new method
