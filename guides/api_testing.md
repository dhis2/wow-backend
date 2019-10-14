
# General guidelines for API testing

  
API tests are good options for testing code in certain situations, but in other cases unit and integration tests are better suited. This guide will provide some guidelines for both when API tests are suitable or not, as well as what you should and should not do when writing one. 


## When should I choose API test?

- When you want to validate the API contract with consumers

- When a functional environment is required to execute the desired scenario

- When API contract is decided, but the internals volatile and are subject to change.

- When the code is not well designed for testability, and an API test is an easier and quicker alternative.

  

## When not to choose API test?

- If a feature can more easily be tested with a unit or integration test. Usually when a lot of conditions needs to be set up before the test.

- Avoid testing cases that are not showstoppers. If a test fails, it should block the release until it has been resolved. (This means if a test can be `@Disabled`, it might not be that valuable)

- If you need to test a wide range of flows in your test, unit or integration tests are often a better option. 
For example: you want to test validation messages, edge-case scenarios.  Controlling the test flow is harder in API tests than in unit tests, where mocking is possible, so writing API tests for every scenario is going to be more expensive than writing several unit tests. In this case, you might want to test one of the edge-case scenarios or validation messages to make sure that the response structure is as expected, but test the other flows with unit tests. 

  

## About API tests

  

When writing API tests, your objective is to test without knowing the implementation details. Keeping this in mind, here are some tips for what to do and what to avoid when writing tests.

  

### What to avoid when writing an API test

- Do not depend on other DHIS2 modules than the dhis-e2e-test. Think from consumers, who doesn't know implementation details, perspective.

- Do not write complex code. Test code should be as straight-forward and error-prone as possible.

- Don’t write tests that depends on execution order of other tests. Your test should not fail when executed alone, selectively picking few tests from different categories or when executed with different test runners.

- Don’t write the tests that depends on data you didn't create. Your test should pass on empty database just as fine as it passes on SL database.

  


## What to keep in mind writing an API test

- Test the test. Simulate a scenario where the test case is expected to fail and make sure it actually fails.

- Keep the test short. Make sure the test doesn't test too much. Looking at the test name should give you a good idea about the test coverage.

- Create convenience methods for setting up the test data

- Provide useful error messages when assertions fail. This will make it easier to understand the problem when the test fails.

- In jUnit assertions, make sure error messages are left where appropriate. i.e

	```java 
  assertEquals( 403, response.statusCode(), "Wrong status code when creating org unit without permissions" );
  ```
- Set up your own data for testing, don’t rely on existing data. This way you have full control over what you are testing.

  

## Writing API tests

The framework for writing API tests have been developed while writing our API tests, and should be further extended based on needs when required. This means the framework might not support all the possible ways to test and interact with the DHIS2 API. However, the following sections gives an introduction to the framework as it is today.

### Framework

#### Actions

Action classes can be found in `src/main/java/org/hisp/dhis/actions` and represents API-endpoints, or groups of endpoints. For example _UserActions_, _ProgramActions_, _DataValueActions_, etc.

**Note:** Every Action class should extend the `RestApiActions` class, which wraps around rest-assured and simplifies the execution of API requests.

#### TestRunStorage

`TestRunStorage` deals with cleaning up the created data. Entities that were created using methods from the `RestApiActions` class will be automatically stored and cleaned up after the test run. This means you don’t need to worry about cleaning up after the test for the most part.

#### ApiTest

All test-classes have to extend `ApiTest`. `ApiTest` is the base class for tests, which manages things like configuration, global preconditions and clean-up hooks.

`ConfigurationExtension` is responsible for rest-assured configuration and `MetadataSetupExtension` is responsible for importing data required for all tests (The global preconditions) and cleaning it up after the tests finished. Both of these classes and their role is orchestrated through `ApiTests`.

**Note:** `MetadataSetupExtension` imports data from `test/resources/setup`

  
#### ApiResponse

`ApiResponse` is a wrapper for rest-assured responses. It provides useful methods for working with the DHIS2 API, such as `extractUid()`, `extractList()`, `getImportSummaries()` and more. All `Action`/ `RestApiAction` classes return `ApiResponse`.

**Note:** Due to a lack of consistency across the DHIS2 API’s responses, it might not always have suitable method for working with the response. In these cases, we should improve `ApiResponse` to support working with the new response.

  

### API test Flow

Every test should follow the same flow:

1. Set up preconditions

2. Execute the test body

3. Tear down the test context

Make sure you put your code in the right place. That way if any errors occurs, it is easy to identify if the problem is part of the preconditions, or with the test itself.

The following example shows the three parts of the flow:

```java
@BeforeAll
public void preconditions()
{ 
	// Create user role
	...
	// Create user
	...	
	// Add user role
	...
}

@Test
public void shouldAddUserRoleToTheUser()
{
	JsonObject userBody = userActions.get(userId).getBody();
	userBody.get("userRoles").getAsJsonArray().add(userRoleId);
	 
	ApiResponse response = userActions.update(userId, userBody);
	ResponseValidationHelper.validateObjectUodate(response);
	
	response = userActions.get(userId);
	response.validate()
		.statusCode(200)
		.body("userRoles.id", contains(userRoleId));
}

@AfterAll
public void cleanUp()
{
	// Clean up any data created during preconditions or test
	// In this case, TestRunStorage will take care of clean up.
}

```

**Note:** In most cases, the clean up is handled by `ApiTest`, which means you usually don’t need to implement you own `cleanUp()`.

  
  
### Convenience methods

  

Convenience methods are great for keeping you test classes short and concise. These methods are located in classes found in the `org.hisp.dhis.actions` package, in the dhis-e2e-test module.

  

#### About convenience methods

- Methods should be created in appropriate classes and/or packages. Avoid dumping all the convenience methods in one class.

- If possible, avoid creating classes for convenience methods for each controller. Instead, merge classes where it make sense from a client perspective.

- For example, from a client perspective adding user groups and user roles are closely connected to the user, so it might make sense to keep all the convenience methods for it in `UserActions` class.

- Convenience methods should primarily only be used when setting up the preconditions or tearing down tests.

- Using convenience methods in the test body might obscure what test behaviour, or even unexpectedly alter the test. Avoid this as much as possible.

- In simple cases, these methods can be used in test bodies as well, if they do not alter the behaviour of the test steps. For example to create a JSON body.

  

Example:

```java
@Test
public void shouldAddUserRoleToTheUser()
{

  // Avoid this:

  ApiResponse response = userActions.addUserRoleToTheUser("userRole", "userId"); // <-- Using convenience method
  
  response.validate.statusCode(200);

  // Do something like this, showing each step required.

  JsonObject userBody = userActions.get(userId).getBody();
  
  userBody.get("userRoles").getAsJsonArray().add(userRoleId);

  ApiResponse response = userActions.update(userId, userBody);

  response.validate();

  ....
}
```
  

### Test data


There are two ways to create test data required for test preconditions: Creating individual entities using the API, or importing files of data using the API.

  

When creating individual entities using the api, you would commonly send `POST` requests to the respective endpoints, like `/users` to create a new user. This approach makes the most sense when you are creating a small amount of entities.

  

In other cases, you might need to set up a lot of data to run your test. In these cases, going for a file-based import is more suitable. This way you can construct a file containing all your data you want, and import it in one go. Files like these should be stored in `test/resources` in a suitable category.

  

To import a metadata file, see the following example:

  

```java
// Like this

new MetadataActions().importMetadata(new File("..."));
 
// Or like this

new MetadataActions().importAndValidateMetadata(new File("..."));

// Or for other entities

new RestApiActions("/dataValueSets").postFile(new File("..."));

```

**Note:** When using a file-based method for importing data, make sure the `userGroupAccess` properties are set up and include TA user group:

  

```json
"userGroupAccesses": [
	{
		"access": "rwrw----",
		"userGroupUid": "OPVIvvXzNTw",
		"id": "OPVIvvXzNTw"
	}
]
```

  

#### Random test data

In certain cases you want the metadata to be totally random. In that case, there are currently several options available (More can be included in the future).

- Use `DataGenerator`, which takes information from `/api/schemas` and generates JsonObject with all the required properties randomly generated.

- Use `FileReaderUtils`, which supports csv, xml and json files and lets you overwrite property values with randomly generated or supplied values. This is especially useful when you have a program and you want to link all the program stages in the metadata import file to that program.

  

#### Where to add test data

There are two options as the where you should create your test data:

  

 **Global preconditions**

- Create and add the metadata import file in `/test/resources/setup` and make sure the file is used in `MetadataSetupExtension`.

- You can also add metadata to already existing files, such as `userGroups.json`, `metadata.json`, `aggregate_metadata.json` and so on.

- Metadata created using this method will be removed after all the tests were executed.

**Note**: Use this option when more tests can benefit from the metadata.

**Test preconditions**

- Import the metadata in a method annotated with `@BeforeAll` or `@BeforeTest` in the same class where your tests are implemented.

- Metadata will be cleaned up after the tests defined in that class are executed.

- Additional cleanup might be required where it might block removal of other metadata. For example, if you reference data/metadata to other global metadata.

**Note**: Use this option when the metadata is only relevant for a small set of tests.

  
  
  

### Assertions

There are currently two ways to write assertions for the API tests:

1. jUnit

2. Rest-assured

  

When using jUnit for your assertions, make sure you provide descriptive and relevant messages, to make it easier to pinpoint the problem in the test report if it fails.

  

Rest-assured assertions provides nice reporting when assertions fail. It displays the request which was executed, as well as the response received. It also supports searching with the JsonBody with jsonPath.

  

Example rest-assured assertion:

```java

userActions.get(userId)
	.validate()
	.statusCode(200)
	.body("users", emptyArray());

```
More information about rest-assured assertions can be found [here](https://github.com/rest-assured/rest-assured/wiki/Usage#verifying-response-data).
  
#### Writing assertions

When writing assertions think about reporting and potential situations where your assertions might not provide enough information. If you see the test failing without reasonable reporting or throwing an exception, please add the necessary assertion which will let the test fail gracefully.
 

Example of a situation where you can an assertion to improve reporting

```java

@Test
public void shouldImportUsers()
{
	JsonObject users = new JsonObject();
	...

	userActions.post(users)
		.validate()
		.statusCode(200)
		//.body("response.status", equalTo("SUCCESS") ) //this might 	throw exception if "response is null

		.body("response", isNotNull())
    .body("response.status",equalTo("SUCCESS"));
}

```

### Example test

The following example represents a complete test, which can be used for reference when writing your own tests.

  

```java

@BeforeAll
public void preconditions()
{
	metadataActions = new MetadataActions();
	loginActions = new LoginActions();
	
	// if there’s no action class or there is no need for one,
	// you can use RestApiActions class directly.
	
	// i.e metadataActions = new RestApiActions(‘/metadata’);’	
	
	loginActions.loginAsSuperUser();
}

@Test
public void shouldImportUniqueMetadataAndReturnObjectReports() throws Exception
{
	// Arrange

	String params = "?async=false" +
		"&importReportMode=DEBUG" +
		"&importStrategy=CREATE";

	File metadataFile = new File( "src/test/resources/metadata/uniqueMetadata.json" )

	JsonObject object = new FileReaderUtils().readJsonAndGenerateData( metadataFile );

	// Act

	ApiResponse response = metadataActions.post( params, object );

	// Assert

	response.validate()
		.statusCode( 200 )
		.body( "stats", Matchers.notNullValue() )
		.body( "stats.total", Matchers.greaterThan( 0 ) )
		.body( "typeReports", Matchers.notNullValue() )
		.body( "typeReports.stats", Matchers.notNullValue() )
		.body( "typeReports.objectReports", Matchers.notNullValue());

	List<HashMap> stats = response.extractList( "typeReports.stats");

	stats.forEach( x -> {
		assertEquals( x.get( "total" ), x.get( "created" ) );

	} );

	...
}

```


## Running the tests

Some setup is required to run the API tests:

- A running instance

- A database (Preferably empty, to have full control of conditions)

- Proper API test configuration

  

### API test configuration

API tests are run against a DHIS2 instance. The following properties are required to connect to this instance and run the tests:

- **baseUrl:**

	- Represents the URL of the API that tests should interact with: `http://play.dhis2.org/dev/api`

- **superUserUsername & superUserPsw:**

	- Tests needs to know the superuser username and password to add the user to TA user group and perform tests requiring super user access.

  

#### Running against existing instance with SierraLeone database

- Set the baseUrl property to already running instance.

- Set superUserUsername, superUserPassword to system user or “taadmin” user (created in API tests)

  

#### Running against empty database

- Set the baseUrl property to already running instance.

- Set superUserUsername and superUserPsw to “aadmin”, “Test1212?”

  

#### Running tests using maven

```

> cd dhis-2/dhis-e2e-test

> mvn test -DbaseUrl=http://localhost:8080/api -DsuperUserUsername=taadmin -DsuperUserPsw=Test1212?

````