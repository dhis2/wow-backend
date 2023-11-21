# Writing Tests for Spring Controllers

In this context this is specifically about spring integration tests for REST controllers based on spring's `MockMvc` feature that return JSON bodies.

Using `MockMvc` directly is not recommended.

Instead the preferred way should be to use the utility layer that was created on top of `MockMvc`.
It ...
* allows to work with a (virtual) JSON tree and vanilla JUnit assertions, 
* makes sure response codes are checked, and 
* has build in convenience functions that build on the conventions used in DHIS2 project

The details of this layer are described in more detail in this document.


## Base Setup
The easiest way to use the convenience layer is to extend `DhisControllerConvenienceTest`.

Usually the extending test class for a specific controller does not need to override any further setup methods.

The current user will be the _admin_ user having the `ALL` authority.

If the base setup of `DhisControllerConvenienceTest` is not suitable for the test scenario the
convenience layer can be "mixed in" by implementing the `WebClient` interface in the test and
implement its abstract method similar or identical to the way `DhisControllerConvenienceTest` does.

## Making HTTP requests
The core API to make HTTP requests is provided by `WebClient` interface that is implemented by 
`DhisControllerConvenienceTest`. It provides convenience methods to make `GET`, `POST`, `PUT`, `PATCH` and `DELETE` requests. 

By intention the API does not support all features of HTTP. 
It is a simplified API to make the kind of RESTful API request that occur within DHIS2.

The main method for HTTP methods that can have a body has 2 arguments,

1. **URL** (in case of integration tests this is everything after `/api/{version}`, so for example `/me` instead of `/api/33/me`)
2. **request body (payload)**: The body can be provided in different ways using the same parameter.
  * when the string provided ends with `.json` it assumes a filename was passed and tries to load the file. It will automatically use content-type `application/json`.
  * when the string provided starts with a mime-type followed by a colon the rest of the string is assumed as the body using the specified mime type, for example: `text/plain:the text`. It will automatically use content-type provided.
  * otherwise the body is assumed to be JSON. It is allowed to use single quotes where the JSON standard expects double quotes, for example `{'field': 'string value'}`. It will automatically use content-type `application/json`.

Examples:

```java
PUT( "/me/changePassword", "{'oldPassword':'district','newPassword':'$ecrEt42'}" );
POST( "/me/verifyPassword", "text/plain:district" );
```

## Asserting HTTP Status and Errors
The simplest way to assert the response status is to use the utility method `assertStatus` from `WebClientUtils`:

```java
assertStatus( HttpStatus.CREATED, POST( "/dataStore/ns/key", "['yes']" ) );
```

Alternatively if the exact status is less important, and we only want to ensure the request was successful the utility method `assertSeries` from `WebClientUtils` can be convenient:

```java
assertSeries( Series.SUCCESSFUL, POST( "/userGroups/" + groupId + "/users/" + userId ) );
```

If the result of a HTTP call should be further validated the status check can be made in combination with accessing the `content` of the response:

```java
JsonObject users = GET( "/users/" ).content( HttpStatus.OK );
```

This equally works for the `Series`:

```java
JsonObject users = GET( "/users/" ).content( Series.SUCCESSFUL );
```

If the plain `content()` is used this is identical to `content( Series.SUCCESSFUL )`.

This way, by design, we cannot access the JSON content of the HTTP response without checking the status or at least the series.

When an error is expected we can use `error()` as a short form of `content().as( JsonError.class )`.
The plain `error()` method makes sure the response status is either a `4xx` or a `5xx` status code.

Similarly to `content` there are variants of `error` that accept the expected `Status` or `Series`:

```java
JsonError error = GET( "/users/" ).error( HttpStatus.FORBIDDEN );
JsonError error = GET( "/users/" ).error( Series.CLIENT_ERROR );
```

Most often the `JsonError` is simply used to check its error message. This can be done in a compact form with the help of vanilla `assertEquals`:
```java
assertEquals( "You do not have the authority to access the key: 'cat' in the namespace:'pets'",
    GET( "/dataStore/pets/cat" ).error( HttpStatus.FORBIDDEN ).getMessage() );
```


## Response Content - A Virtual JSON Tree
The content is presented as generic, "virtual" JSON tree that has the role of an access API.
It is not an actual representation of the parsed HTTP response body but a way to access this content in a convenient way based on what we belief to have received.

The HTTP response can be assigned to any of the basic JSON node types:

* `JsonValue` (any of the below)
* `JsonObject`
* `JsonArray`
* `JsonNumber`
* `JsonString`
* `JsonBoolean`

```java
JsonString value = GET( "/dataStore/pets/cat" ).content();
JsonObject metaData = GET( "/dataStore/pets/cat/metaData" ).content();
```

It is important to realise that a JSON node is purely an access API for value but not a value itself.
The leaf values or properties of these are always accessed via the according methods on the nodes.

```java
JsonString cat = GET( "/dataStore/pets/cat" ).content();
String catValue = cat.string();
JsonObject metaData = GET( "/dataStore/pets/cat/metaData" ).content();
boolean isObject = metaData.isObject();
```

Nodes are "virtual" in the sense that we can navigate to both nodes that exist in the response and nodes that might turn out to not exist in the response. 
Navigation does **not** check existence. 
This is a good thing as it saves us from asserting the existing of parent.
Existence of a node is either checked explicitly using `exists()` or implicitly using a value accessing methods like `string()`:

```java
assertTrue( GET( "/dataStore/pets/cat" ).content().exists() );
assertEquals( "cat-value", GET( "/dataStore/pets/cat" ).content().string() );
```

Note that leaf value accessors that return reference types like `String`, `Number` or `Boolean` by default return `null` when a node does not exist or exists but is defined as JSON `null`.

For primitives like `boolean`, `int` or `double` will throw an exception if the JSON node does not exist. These each have their special access method.

```java
assertEquals( 42, GET( "/dataStore/pets/cat" ).content().intValue() );
assertEquals( 42.0d, GET( "/dataStore/pets/cat" ).content().doubleValue() );
assertTrue( GET( "/dataStore/pets/cat" ).content().booleanValue() );
```

The reason for this design is so we can focus on making assertions based on what we expect 
without having to check or assert intermediate steps or make detailed distinctions where they do not matter to us.

## Asserting (Complex) Response Content

When asserting values from the response JSON content this can be based on the generic JSON tree using `JsonObject` and `JsonArray` API with `getArray` and `getObject` to navigate to the leafs and `getString`, `getNumber` or `getBoolean` to get a leaf node of an array or object by index or name.

This soon becomes cumbersome and repetitive as the expected structure and names have to be kept in mind and duplicated in tests with reoccurring structures.
Therefore this way of navigating the tree is not recommended.

Instead it is often better to create a dedicated interface (extending `JsonValue` or a more specific node type) which then captures the shape of the expected JSON.

Then a node can be "cast" to such a shape using the `as` method:

```java
JsonObject me = GET( "/me" ).content();
// becomes
JsonUser me = GET( "/me" ).content().as( JsonUser.class )
```

Now with the extended API we can assert properties of the `me` user more comfortably:
```java
assertEquals( "Peter", me.getFirstName() );
```

Like the generic JSON tree any extended API is just a view using `default` methods to implement further methods based on the methods provided by the generic tree to provide convenient ways to navigate the JSON tree and extract or even transform leaf values.

Hence, both complex and simple nodes can be extended. 
For example a `JsonDate` is an extended `JsonString`, while a `JsonUser` is an extended `JsonObject`.

Similar to the inheritance hierarchy used in DHIS2 domain model we can use multiple levels to capture common methods. 
As we are using interfaces this even allows for "mix-in" style inheritance of convenience methods.

This means long term we can encode the DHIS2 RESTful API using extension interfaces.
This then allows to work with JSON responses similar to the domain model.
For example:

```java
assertEquals( LocalDateTime.now(), 
	GET( "/users/{id}", id ).content().as( JsonUser.class ).getUserCredentials().getLastLogin() );
```

## Extending the Response Content JSON Tree
Extending the "virtual" JSON tree is very simple as a section of the `JsonError` extension shows:

```java
public interface JsonError extends JsonObject
{
    default String getHttpStatus()
    {
        return getString( "httpStatus" ).string();
    }

    default int getHttpStatusCode()
    {
        return getNumber( "httpStatusCode" ).intValue();
    }
    //...
}
```
With this we can use `content().as(JsonError.class)` which is (basically) what `error()` does.

It is important to make these interfaces `public` accessible.

Another example of a simple yet very useful extension is `JsonDate`:

```java
public interface JsonDate extends JsonString
{
    default LocalDateTime date()
    {
        return parsed( str -> LocalDateTime.parse( str, DateTimeFormatter.ISO_LOCAL_DATE_TIME ) );
    }
}
```

### Lists
To make working with uniform lists of elements easier there is the `JsonList` interface which
can be accessed using `getList` on a `JsonArray` for the array element or a `JsonObject` for the property.

The second argument to `getList` is the node type of the elements.
For example as used in the following example of an extension to `JsonObject` (as found in `JsonDashboardItem`):

```java
default JsonList<JsonUser> getUsers()
{
    return getList( "users", JsonUser.class );
}
```
The elements of such a `JsonList` can then be accessed by index using `get(int index)`.

`JsonList` are also `Iterable` so they can be used in `for`-each loops.

### Maps
Equivalent to `JsonList` there is a helper to understand a JSON object node as a map with `String` keys and a uniform value type. This API is captured by the `JsonMap` interface which is accessed using `getMap` on object or array nodes.

```java
public interface JsonSharing extends JsonObject
{
	//...
    default JsonMap<JsonObjectAccess> getUsers()
    {
        return getMap( "users", JsonObjectAccess.class );
    }

    default JsonMap<JsonObjectAccess> getUserGroups()
    {
        return getMap( "userGroups", JsonObjectAccess.class );
    }
}
```

The values of the map are then accessed using `get(String key)`.

## Switching Users
Many of the REST endpoints do behave quite differently depending on which authorities the current user has.
Therefore switching users before or during a test scenario is very common operations.

The `DhisControllerConvenienceTest` provides a few helpers to make switching between users easy.

At the start of a test the current user is always an administrator with `ALL` authority to not fail tests that don't target the security aspect.

To switch to another user with special authorities use `switchToNewUser` passing:

1. user name
2. a varargs list of authorities the user should have

```java
switchToNewUser( "anonymous" ); // has no authorities
assertStatus( HttpStatus.FORBIDDEN, DELETE( "/dataStore/pets" ) );

switchToNewUser( "someone", "pets-admin" ); // has the "pets-admin" authority
assertStatus( HttpStatus.OK, DELETE( "/dataStore/pets" ) );
```

Tip: To switch back to the administrator user use `switchToSuperuser()`

The currently logged in user is also accessible using `getCurrentUser()`.

The UID of the superuser (logged in or not) is also available using `getSuperuserUid`.