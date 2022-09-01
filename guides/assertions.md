# Assertions

A page on usage of assertions in tests.

**Which one to use? Where to add?**

1. prefer junit5 assertions if a suiting one exists
2. otherwise check if a suiting assertion exist in DHIS2's own `Assertions` class
3. otherwise add a new assertion to DHIS2's `Assertions` class

In summary: In tests only junit and DHIS2 `Assertions` should be used directly.

**When implementing a new assertion**
* use junit5 convention of expected, actual, message argument order
* delegating to a 3rd party assertions library is fine (remember to flip parameter order where needed)
* do not expose 3rd party types in the method parameters

**Known Problems**

Assertions on specfic DHIS2 types might not be possible to add to DHIS2's `Assertions` class because of module dependencies.
Long term it would be nice to move such types to the `web-api` package.
Short term the workaround is to make the assertion work on more general types, maybe introduce an interface in `web-api`.
