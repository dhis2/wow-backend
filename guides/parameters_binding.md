# Parameters binding Guide

This guide explains how the binding for request parameters and fields inside a parameter objects
works and what happens when the binding fails.


### Parameter Objects
Lets have a look at this example:

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

Spring will try to convert parameters from String into the proper type using a `PropertyEditor` if available, otherwise a `Converter`. `PropertyEditor`s are registered and bind to a class in `CrudControllerAdvice.initBinder(WebDataBinder binder)` method.
`Converter`s are registered in `WebMvcConfig.addFormatters(FormatterRegistry registry)` method.

`PropertyEditor`s and `Converter`s work in a similar way but in different context, the former is used only when binding parameters, the latter is a global converter that can be used in any layer of the system.

If the conversion fails Spring will raise an exception, `MethodArgumentTypeMismatchException` if the failing conversion happened for a @RequestParam field and a `BindException` if the fails happened in a field of a parameter object.
Both exceptions are handled in `CrudControllerAdvice`, the first one is a simple exception that will carry the information about the failing field, the failing value and the type of the field.
On the other side, a `BindException` is a complex exception that wraps field and global errors, at the moment we are not using any validator framework so only field errors are possible.
To be consistent through the API we are also only considering one field error, even though multiple of them can be present.
A `FieldError` wraps a `TypeMismatchException` that is similar to a `MethodArgumentTypeMismatchException` and handled in the same way.
In the case of failure on fields that are `Enums` or `primitive` types, we are building a message for the user with all the relevant information needed to fix the issue. When the failure happens in a "custom" field, then the message returned by the `PropertyEditor` or the `Converter` is returned.

`PropertyEditor`s should throw an exception when the parameter is null or an empty string because this happens when the parameter is specified without value in the URL like `/entries?page` or `/entries?page=`

**Do**
* 🚀 do prefer primitives with default over wrappers
* 🚀 do use enum typed fields (instead of `String`) for `enum` values
* 🚀 do initialise fields with default values where applicable
* 🚀 create `PropertyEditor` for custom fields and throw an exception if the source is null or an empty string

**Avoid**
* ❌ avoid creating a `Converter` for a parameter as it will not handle the empty case in the proper way
