# OpenAPI

## Generating OpenAPI documents

### About the Generation
The generation of OpenAPI documents is a multistep process.

1. `ApiAnalyse`: Analyse controllers and used classes using reflection to build a `Api` model
2. `ApiDescribe`: Read descriptions from markdown files to insert into the `Api` model
3. `OpenApiGenerator`: Generate the OpenAPI document from the `Api` model

During the 3rd step of generating the document Java endpoints can be found to
collide in terms of OpenAPI semantics. In that case the colliding endpoints
are merged by the `ApiMerger`.

### Generating OpenAPI documents via Java Application
The easiest way to generate the documents is to use the `OpenApiTool`.
This is a plain old Java program that starts from a `main` method.

The tool will use the `.class` files of the controllers as starting point. 
Therefore, it is necessary to use the tool after DHIS2 has been compiled
successfully.

While it theoretically is possible to use the tool directly from command
line this would require adding all dependent modules to the classpath.

The much easier way is to just run the tool in the IDE which will automatically
add the maven dependencies.

To run, create a _Java Application_ _Run Configuration_. The easiest is to click
the run arrow displayed on `OpenApiTool` class or it's `main` method.
This prints back the usage info:
```
Usage: [<options>] [<path or tag>...] <output-file-or-dir>
--group (flag)
  generate multiple files where controllers are grouped by tag
```
Edit the created configuration and add options, filters and target dir or file.

| _Program Arguments_ | Output |
|---------------------|--------|
| `openapi-target.json` | generates a single document for all controllers with the provided name |
| `--group /example/openapi`| generates multiple documents in the target dir, controllers are grouped into documents by their first `@OpenApi.Tags` tag |
| `/users openapi-users.json`| generates a single document with the provided name including any controller with the root path `/users` |
| `/users /userGroups openapi-users-and-groups.json`| generates a single document with the provided name including any controller with a root path either being `/users` or `/userGroups` |
| `user openapi-tagged-user.json`| generates a single document with the provided name including any controller tagged `user` on the controller class |
| `user system openapi-tagged-user-or-system.json`| generates a single document with the provided name including any controller tagged `user` or tagged `system` on the controller class |

A filter starting with a `/` is a path filter, otherwise it is a tag filter.
Path and tag filters can be combined, then a controller has to match both filters.


### Generating OpenAPI documents via Server Endpoint
The generation of OpenAPI documents is also accessible on a running server.

The document is generated "on-the-fly" when it is requested. 
Similar to the application tool content can be filtered by `path` and/or by `tag`.

For example,
* https://play.dhis2.org/dev/api/openapi/openapi.json generates a document including all controllers
* https://play.dhis2.org/dev/api/openapi/openapi.json?path=/users generates a document containing only controllers with root path `/users`
* https://play.dhis2.org/dev/api/openapi/openapi.json?tag=user generates a document containing only controller tagged `user`

Again multiple filters can be used and path and tag filters can be combined.

## Publishing OpenAPI documents
The generated JSON documents can be turned into browsable documentation 
using tools like swagger or stoplight studio. 

Be careful with MB size files. Some tools cannot handle them at all or freeze.

We use https://dhis2.stoplight.io/studio/dhis2:main to manage. 
Special authority is required.

To view the latest published documents goto https://dhis2.stoplight.io/docs/dhis2 .


## Adjusting OpenAPI documents
The generated document originates from a reflection based analysis.
This analysis makes use of Java language declarations as well as spring and
jackson annotations.

However, anything not visible in type or method signatures cannot be inferred.
Some framework conversions or conventions can cause a misrepresentation of the 
actual REST API.  

To correct such errors or missing information the family of `@OpenApi` 
annotations is used To adjust or correct the OpenAPI document without having to
change the function of the code.

In some occasions it might still be easier and more meaningful to instead
express the code differently, so it becomes more clear both for the reader
and the reflection analysis.

By default, any class annotated `@Controller` or `@RestController` is analysed
and (if not filtered) included in the generated document.

### Ignoring
**TLDR:** Anything that should not be in the generated OpenAPI document can be
excluded by annotating the element with `@OpenApi.Ignore`.

To ignore...

* an entire controller class annotate the class with `@OpenApi.Ignore`
* a specific endpoint method annotate the method with `@OpenApi.Ignore`
* a specific parameter of an endpoint method annotate the parameter with `@OpenApi.Ignore`
* a property field or method of a schema annotated the field or getter method with `@OpenApi.Ignore`

Ignoring always takes precedence over other adjustment annotations. 

### Tagging Controllers
**TLDR:** Add `@OpenApi.Tags` with at least one tag to each controller class

All controller classes should be tagged to add them to a group and to further
structure the generated document.

```java
@OpenApi.Tags({"user", "query"})
class UserLookupController {}
```

In context of OpenAPI specification tags do not have order semantics but
tools such as stoplight give special semantics to tags based on their position.

We use the first tag to group documents when `--group` is used.
The second tag becomes the first for the endpoints within the document which is
used by stoplight to group the endpoints.

All tags present on a controller class are added to all endpoints in that class.
Tags can also be applied directly to endpoint methods which adds further tags
to that endpoint in the document. This has only informal purposes at this point.


### Adding Endpoints Parameters
**TLDR:** Use `@OpenApi.Param` (single) and `@OpenApi.Params` (multi) on endpoint methods.

Not all parameters become visible from the endpoint method signature.
In such a case the `@OpenApi.Param` and `@OpenApi.Params` annotations can be
used to add additional parameters.

To add a single parameter to a target endpoint method annotate it with
`@OpenApi.Param` providing the name and type of the parameter.

```java
class Controller {
    @OpenApi.Param(name = "fields", value = String[].class)
    @GetMapping
    List<Entry> getEntryList(Map<String, String> params) {
    }
}
```

Since annotations do not allow for generics use array types instead of 
collection types. For the resulting OpenAPI document this makes no difference.

To add multiple parameters to a target endpoint method annotate it with
`@OpenApi.Params` providing the type of the parameters class.

```java
class Controller {
    @OpenApi.Params(WebOptions.class)
    @GetMapping
    List<Entry> getEntryList(Map<String, String> params) {
    }
}
```

Usually such classes should then be annotated `@OpenApi.Shared`. 
This will use globally shared parameter definitions in the resulting
OpenAPI document.

To adjust what members are made into parameters the fields or getters can be
annotated with either `@OpenApi.Ignore` or `@OpenApi.Property`.


### Adjusting Endpoint Parameters
**TLDR:** Use `@OpenApi.Param` on parameters to change their assumed type

In some situations parameters are inferred from the spring annotations but the
type used in the endpoint method signature is not what represents them best.
To substitute the type with a more specific one annotate the parameter with
`@OpenApi.Param`. This can be applied on top of spring's `@PathVariable` and
`@RequestParam` or on method parameters that have neither of these.

`OpenApi.Param` takes precedence over spring's annotations but when name is left
empty it falls back to name from spring annotation. Similar the required status
is determined considering both annotations when present. 

```java
class Controller {
    
    @GetMapping( "/{uid}" )
    Entry getEntry( @OpenApi.Param( UID.class ) @PathVariable( "uid" ) String pvUid ) {}
}
```
For example, the more specific `UID` type overrides `String` for the `uid` 
parameter while the name still falls back to `"uid"` from `@PathVariable`
because `@OpenApi.Param` did not specify another name.


### Adjusting the Request Body
**TLDR:** Use `@OpenApi.Param` with no (empty) `name` to set/override the request body type

To set or override the request body of an endpoint the `@OpenApi.Param` 
annotation is used with no (empty) `name` property.
When present the request body from the signature is ignored.


### Adding Responses
**TLDR:** Use `@OpenApi.Response` to add responses for further HTTP status codes

The default response is inferred from the endpoint method signature and spring's
`@ResponseStatus` annotation. To add further responses add one or more 
`@OpenApi.Response` annotations to the endpoint method.

```java
class Controller {
    @OpenApi.Response(ObjectListResponse.class)
    @OpenApi.Response(status = FORBIDDEN, value = WebMessage.class)
    @GetMapping
    List<Entry> getEntryList(Map<String, String> params) {
    }
}
```

### Adjusting the Default Response
**TLDR:** Use `@OpenApi.Response` with no status to override the default response

When no `status` is specified the response overrides the type of the default
response. So, in the above example `List<Entry>` is effectively replaced by
`ObjectListResponse`.

### Adjusting Object Properties
**TLDR:** Use `@OpenApi.Ignore` and `@OpenApi.Property` on fields or getter methods

Properties are used for parameters objects as well as data objects like DHIS2's
persistent and DTO objects as they occur in request and response. 

By default, that analysis is looking for jackson's `@JsonProperty` annotation. 
If no annotations are present all properties based on getters are added. 

To adjust the described property selection use `@OpenApi.Ignore` to exclude a
property. This should be placed where jackson's `@JsonProperty` is present if
it is used. 

To add a property that otherwise is not picked up annotate the field or getter
with `@OpenApi.Property`. This can also be used adjust the assumed type of 
properties. 

If both `@JsonProperty` and `@OpenApi.Property` are present `@OpenApi.Property`
takes precedence.


### Generic Types and Inheritance
**TLDR:** Use `@OpenApi.EntityType` on class and method level to define the 
substitution within the class/method context, use `@OpenApi.EntityType` in 
other annotations to use the type from the actual endpoint context.

The analysis does not perform type parameter substitution during analysis.
As a consequence the actual type of type parameters is lost or unknown.
However, a much simpler type substitution was added instead.

Each controller can define one substitution type by annotating the class:

```java
@OpenApi.EntityType( ActualType.class )
class Controller {}
```

This default is inherited by each endpoint method in that class 
unless it is overridden by a method level annotation:

```java
@OpenApi.EntityType( ActualType.class )
class Controller {
    
    @EntityType( AnotherActualType.class )
    @GetMapping
    ResponseEntity<?> getObject() {}
}
```

To use the defined type use `EntityType.class` in any of the `OpenApi` 
annotations that specify a type of parameters or responses. 

```java
class Controller extends BaseController {
    
    @OpenApi.Response( EntityType.class )
    @GetMapping
    ResponseEntity<?> getObject() {}
}
```

At first glance this appears to substitute one specific type with another one.
However, when adding inheritance this is no longer the case. 
The endpoint context defines `@EntityType` differently for different
controllers inheriting an endpoint from a common abstract base class. 
For each of these the actual type used is different now.

This can also be applied to complex DTOs which have a field based on the
context dependent type.

```java
class ExampleResponse<T> {
    
    @JsonProperty
    Pager pager;
    
    @OpenApi.Property( EntityType[].class )
    @JsonProperty
    List<T> entries;
}
```
In this example `List<T>` is now substituted with different actual array
types based on what is the substitution type for the endpoint. For example,
`User[]`, `UserGroup[]`... . Again, making use of the fact that array and 
collection types have the same result in an OpenAPI document.


### Context Dependent Property Names
**TLDR:** Use `path$` as property name to substitute it with root path (minus `/`)

In some responses the name of a property should be different based on that type
of objects is returned. For example a list of users is named `users`, a list of
data elements `dataElements`. This is usually solved by some jackson 
serialisation mechanism that the analysis does not understand.

A simple mechanism was added for the specific use case in DHIS2.
The property name `path$` is substituted to the root path of the current
controller context.

```java
@RequestMapping("/users")
class UserController {}
```

In this example a property named `path$` in the source (either this is the
actual name of the field or method or the name given via annotation) is 
replaced with `users`.

Similar to `EntityType` substitution for types the actual value now depends on 
the controller context and can become different actual names for different
controllers using or inheriting the type with the special `path$` property.
