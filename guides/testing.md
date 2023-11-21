# Testing guidelines and architecture

## Testing and PRs

### Platform Team Goal
The goal the platform team has set for test coverage in PRs:

* minimum of 1 test for each PR
* mockito based tests do not count (to not encourage them)
* bugfix PRs should have a test to show the absense of the bug after the fix
* new REST APIs should cover each request parameter with at least 1 test (test scenarios that cover multiple parameters count for each of them)


## Test categories

In DHIS2 there are currently 3 categories of tests:

- Unit tests
- Integration tests using H2
- Integration tests using Docker and Postgres

There is also a fourth test category, used for end to end testing, which is not in scope of this document.

### Unit tests

Unit tests are meant to test classes and methods in isolation (no external dependencies required, such a database or a bean injected by the Spring context).
These tests make heavy use of _mocks_ for mocking dependencies and are meant to be fast and simple.

See [https://github.com/dhis2/wow-backend/blob/master/guides/test_mocking.md](Mockito guidelines) for more information on mocking and stubbing.

Unit tests do not inherit from any superclass and are automatically executed when running `mvn test`.

### Integration tests using H2

This category of tests make use of an embedded H2 database in order to test code that depends on a database being present.
This category of tests is considered deprecated in favour of Docker-based Integration tests, since H2 doesn't support the `Postgis` extension and doesn't guarantee that a query that runs successfully on H2 will also run on Postgres (and _viceversa_).
Additionally, H2-based tests require the Spring context to be loaded. Therefore, they run significantly slower than Unit Tests.

A H2-based integration test, creates the database schema automatically using the `hibernate.hbm2ddl.auto` property. Additionally, a small amount of data is created in the test database (see `org.hisp.dhis.system.startup.StartupRoutineExecutor`). 
 
 There are **two** sub-types of Integration tests: transactional and non-transactional
 
 In the majority of cases, transactional tests are recommended. Once the test is completed, the transaction is automatically rolled-back and the database is not modified.
 
 There are cases where text fixtures are setup using Hibernate entities and, in the course of the test, the same data is read back using JDBC. Since Hibernate and the `JdbcTemplate` do not share the same Transaction Manager, the data inserted by Hibernate are not "visible" by the  `JdbcTemplate`-based operations. Hence we need to actually commit those data to the DB before it becomes visible.
 The setup-up data must be cleaned up manually in invoking `org.hisp.dhis.dbms.DbmsManager.emptyDatabase()`.
 
 A transactional integration test must extend `org.hisp.dhis.DhisSpringTest`.
 
 A non-transactional integration test must extend `org.hisp.dhis.DhisTest`. 
 
 Additionally, there is a third test superclass which must be used for testing the API: `org.hisp.dhis.webapi.DhisWebSpringTest`. This superclass also loads the Spring context and can be used to test the interaction with the Web API endpoints.
 
 H2-based integration tests are automatically executed when running `mvn test`.
 
### Integration tests using a Dockerized Postgres

 This category of tests make use of a Postgres database running within a Docker container. The container is started and stopped by the test infrastructure. The Postgres database is initialised using Flyway (see [Flyway guidelines](https://github.com/dhis2/wow-backend/blob/master/guides/db_migration.md)), including all the schema evolutions.
 
 Similarly to H2-based tests, this test category is slower than Unit Tests and should be used when database access is mandatory (e.g. testing a query that uses Postgis features).
  
 A Postgres-based Integration test must 
 - extend `org.hisp.dhis.IntegrationTestBase` 
 - be annotated with `@org.junit.experimental.categories.Category( IntegrationTest.class )`.
 
 The test can override the `setUpTest()` method for initialisation of [test fixtures](https://github.com/junit-team/junit4/wiki/test-fixtures).
 
 This category of tests depends on Docker being installed locally.
 
 This category of test is not executed automatically when running `mvn test`. It requires a dedicated Maven profile, named `integration`.
 To run Docker-based tests using Maven, use `mvn test -Pintegration`

### Integration tests for Spring REST-Controllers

A convinient way to test REST controllers in a spring integration test is to extend `DhisControllerConvenienceTest`.

They offer `GET`, `POST`, `PUT`, `PATCH` and `DELETE` methods with:

* 2 args: URL + body (except `GET`)
* 1 arg + varargs: URL +  arguments for URL parameters

The result returned by these is implicitly or explcitly verified against a HTTP status code or series (2xx,3xx etcetera)
and can be "virtually mapped" as some JSON object which can be used to make assertions.

All details are found on page [Spring controller testing](guides/spring_controller_testing.md).


## Test architecture

The unit/integration testing architecture is based on JUnit 4 and a number of test frameworks, such as [Spring Test](https://docs.spring.io/spring/docs/current/spring-framework-reference/testing.html), Mockito, [Test Containers](https://www.testcontainers.org/), etc.

All the test above test categories are executed using a Spring profile named `test`.
The profile is applied by the `org.hisp.dhis.DhisConvenienceTest` superclass, from which all the tests derives.
There are two additional profiles in use, which determine the database to use during the test run:

- `h2-test`
- `test-postgres`

These profiles are applied whenever a test extends from `org.hisp.dhis.DhisSpringTest` or `org.hisp.dhis.IntegrationTestBase`.

Flyway database evolutions are only applied if the `test-postgres` profile is in use.


## Assertions

**Which one to use? Where to add?**

1. prefer _junit5_ assertions if a suiting one exists
2. otherwise check if a suiting assertion exist in DHIS2's own `Assertions` class
3. otherwise add a new assertion to DHIS2's `Assertions` class

In summary: In tests only _junit_ and DHIS2 `Assertions` should be used directly.

**When implementing a new assertion**
* use _junit5_ convention of expected, actual, message argument order
* delegating to a 3rd party assertions library is fine (remember to flip parameter order where needed)
* do not expose 3rd party types in the method parameters

**Known Problems**

Assertions on specfic DHIS2 types might not be possible to add to DHIS2's `Assertions` class because of module dependencies.
Long term it would be nice to move such types to the `web-api` package.
Short term the workaround is to make the assertion work on more general types, maybe introduce an interface in `web-api`.
