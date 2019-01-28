# Mocking and Stubbing guidelines

## What is mocking

Unit tests are designed to test the behaviour of specific classes or methods without relying on the behaviour of their dependencies. 
Mocking is the act of removing external dependencies from a unit test in order to create a controlled environment around it. Typically, we mock all other classes that interact with the class that we want to test. Common targets for mocking are:

- Database connections,
- Web services,
- Classes that are slow
- Classes with side effects
- Classes with non-deterministic behaviour

Mockito is the most popular mocking library in Java. It is based on a simple API that has evolved from EasyMock. The examples in this guidelines will make use of the latest version of Mockito (2.x). 

## Mocking vs. Stubbing

Mocks and stubs are "fake" Java classes that replace these external dependencies. These fake classes are then instructed before the test starts to behave as you expect. More specifically:

- A **stub** is a fake class that comes with predefined return values. It’s passed (or injected) into the class under test to allow controlling what's being tested as input. A typical stub is a database connection that simulates accessing the underlying data without the database being actually present.

- A **mock** is a fake class that can be examined after the test is finished for its interactions with the class under test. For example, you can ask it whether a method was called or how many times it was called. Typical mocks are classes with side effects that need to be examined, e.g. a class that sends emails or sends data to another external service.

Notice that, even though stubbing and mocking are two different things, Mockito uses "mocks" for everything so we will follow the same terminology in the sample source code.

Mockito offers an additional type of mock, called a "Spy".
In contrast to mocks, creating a spy requires an instance to spy on. By default, a spy delegates all method calls to the real object and records what method was called and with what parameters. That’s what makes it a spy: It’s spying on a real object. As a general principle, it is preferable to use mocks.

## Mockito basics

There are several way to create mocks using Mockito.

The recommended way is to annotate the classes that we wish to mock.

	public class CustomerServiceTest {
		
		@Mock
		private CustomerDao customerDao;
		
		private CustomerService subject;
		
		@Rule
	  public MockitoRule mockitoRule = MockitoJUnit.rule();

		@Before
		public void setUp() {
			subject = new CustomerServiceImpl(customerDao);
		}
		
		@Test
		public void canFetchCustomer() {
			// implement test
		}
		
In the example above, we have a `CustomerServiceImpl` class that is the subject of our test (hence, the variable name `subject`).
`CustomerServiceImpl` has a single dependency, the `CustomerDao` interface. The implementation of this interface is what we want to mock in our test, since it requires database access.

The `customerDao` interface is mocked using the `org.mockito.@Mock` annotation.
The `@Rule` annotation initialises the mock, and automates the framework validation; is preferable to JUnit Runners, because a test may already need a runner (e.g. PowerMock or Spring).

In the `setUp` method, the test initialises the class under test, by injecting the initialised mock using constructor-based injection. Constructor-based injection is preferable to setter based injection. A class that takes a required dependency as a constructor argument can only be instantiated if that argument is provided (you should have a guard clause to make sure the argument is not null.) A constructor therefore enforces the dependency requirement whether or not you're using Spring, making it container-agnostic.
Additionally, starting from Spring 4.3, Spring performs implicit injection in single-constructor scenarios, making your code more independent of Spring by potentially not requiring an `@Autowired` annotation at all. 

At this point, the class under test does not really know that the `CustomerDao` is fake. It will just call its method and get the sample Customer unaware that Mockito is behind everything.

## Stubbing methods

It is possible to call any method on `CustomerDao` mock:
by default, all methods of a mock return "uninitialized" or "empty" values, e.g., zeros for numeric types (both primitive and boxed), false for booleans, and nulls for most other types. 

 Usually, we want to configure the mock and define what to do when specific methods of the mock are called. This is called _stubbing_.
 
 Mockito offers two ways of stubbing. The first way is "_when this method is called, then do something._" Consider the following snippet:
	 
	 Customer sampleCustomer = new Customer();
   sampleCustomer.setFirstName("John");
   sampleCustomer.setLastName("Good");
	 when(customerDao.get(10L)).thenReturn(sampleCustomer);
	 
	 Customer c = customerService.getCustomerById(10L);
	 
	 // c.getFirstName() == "John"

The code is intuitive: _when_ the `get` method of the `CustomerDao` interface is called, _then_ return a new `Customer`. 


The second way of stubbing reads more like "Do something when this mock’s method is called with the following arguments." This way of stubbing is harder to read as the cause is specified at the end. Consider:	 
	 
	 doReturn(sampleCustomer).when(customerDao).get(10L);
	 
The _when-then-return- form is preferred, because of better readability.	 The second form is normally used when stubbing `void` methods.

## Throwing exceptions

`thenThrow()` and `doThrow()` configure a mocked method to throw an exception:

	when(customerDao.get(10L)).thenThrow(new CustomerNotFoundException());

or

	doThrow(new CustomerNotFoundException()).when(customerDao.get).customerDao.get(10L);
	
Mockito checks that the exception is valid for that specific stubbed method and will fail if the exception is not in the method’s checked exceptions list.

## Argument matchers

In the previous example, the method `get` is stubbed by telling Mockito: when the method `get` is invoked with value `10L` then return this Customer. In those cases, Mockito just calls `equals()` internally to check if the expected values are equal to the actual values.
In certain scenarios, the test may not know these values beforehand or may not care about the actual value or, perhaps, we want to define a reaction for a wider range of values.

All these scenarios (and more) can be addressed with argument matchers. The idea is simple: instead of providing an exact value, the test uses an **Argument Matcher** for Mockito to match method arguments against.

	when(customerDao.get(anyLong())).thenReturn(sampleCustomer);

The `anyLong()` ArgumentMatcher matches any **non null** Long. Therefore, Mockito will return the same `sampleCustomer` as long as the method is invoked with a Long value.

If a method has more than one argument, it isn’t possible to use ArgumentMatchers for only some of the arguments. Mockito requires you to provide all arguments either by matchers or by exact values.

Let's add a new method to the `CustomerDao` interface:

	boolean updateEmail(Customer customer, String email)

This code will not work, because we are mixing an ArgumentMatcher (`any(Customer.class)`) with a an exact value (`bob@gmail.com`).

	when(customerDao.updateEmail(any(Customer.class), "bob@gmail.com)).thenReturn(false);
 
To fix the previous code, it is necessary to use an ArgumentMarcher also for the second argument, like so:
	
	when(customerDao.updateEmail(any(Customer.class), eq("bob@gmail.com))).thenReturn(false);

The `eq()` ArgumentMarcher simply uses `equals()` to match the given parameter. For a full list of argument matchers refer to the documentation on the `org.mockito.ArgumentMatchers` class.

## Custom matchers

The Mockito standard library offers a large number of Argument Matchers; however, in certain scenario a Custom Matcher can be used to provide some matching logic that is not already available in Mockito.
	
	@Mock
	private CustomerInvoiceService subject;
	
	ArgumentMatcher<File> isInvoice = file -> file.getName().endsWith("invoice");
	
	when(subject.accept(argThat(isInvoice))).thenReturn(true);

	assertTrue(subject.accept(new File("/test/customerInvoice")));
	
Here we have created a `isInvoice` Argument Matcher and use `argThat()` to pass the Matcher as argument to a mocked method, tubbing it to return true if the filename ends with "invoice".

## Verifying behaviour

Mockito can ensure whether a mock method is being called with the required arguments or not. It is done using the `verify()` method. 
Verifying arguments is often redundant, so it has to be used only in specific cases.
Let's make two examples to clarify this.
	
	1. Customer sampleCustomer = new Customer();
	2. sampleCustomer.setFirstName("John");
	3. sampleCustomer.setLastName("Good");
	4. when(customerDao.get(10L)).thenReturn(sampleCustomer);
	5.
	6. Customer c = customerService.getCustomerById(10L);
	7. assertThat(c.getFirstName(), is("John"));
  8.
	9. verify(customerDao).get(10L);
  
In the above example, the last line verifies that the method `get` was effectively called with the exact value `10L`.

Since we already assert that `getFirstName()` is "John" the verification is redundant (if the method `get()` was not called   by the `customerService.getCustomerById(Long id)` or was called with a different argument, the assertion at line 4 would fail).

It is considered good Mockito style to explicitly verify only the interactions that can't be implied from well-crafted stubs and postcondition assertions. For instance, a method that is `void` can be tested using verification.

	void sendEmail(Customer c, String subject, String body) {
		boolean result = this.emailService.send(c.getEmail(), subject, body);
		if (!result) {
			log.error("An error occurred!");
		}
	}
	
The method above, calls an `emailService` which has a return value that is not returned by the `sendEmail` method.

In this case, it is appropriate to use `verify` to check that the email service was actually invoked.

	verify(emailService).send("bob@gmail.com", "Test subject", Hello World!");
	
By default, Mockito verifies that the method was called once, but it's possible to verify any number of invocations:

	// verify the exact number of invocations
	verify(service, times(42)).get(anyLong());

	// verify that there was at least one invocation
	verify(service, atLeastOnce()).save(any(Customer.class));
	
	// verify that there were at least five invocations
	verify(service, atLeast(5)).get(anyLong());
	
	// verify the maximum number of invocations
	verify(service, atMost(5)).get(anyLong());

	// verify that there were no invocations
	verify(service, never()).remove(anyLong());
	
Argument Matchers can be used in verification assertions.

## Capturing arguments

Besides verifying that a method was called with specific arguments, Mockito allows you to capture those arguments so that you can later run custom assertions on them.

Let's look at an example:

	public Customer merge(Customer c1, Customer c2) {
	
		Customer mergedCustomer = new Customer();
		if (c1.getFirstName().equals(c2.getFirstName()) {
			mergedCustomer.setFirstName(c1.getFirstName());
	  } else {
		  mergedCustomer.setFirstName(c2.getFirstName());  
	  }
		
		...
		
		customerDao.remove(c1);
		customerDao.remove(c2);
		
		return customerDao.save(mergedCustomer);
		
	}
	
If we would have to write a test for the above method, we would need to be sure that the method `save(Customer c)` is called with the right argument. Since the logic that 'creates' the argument (`mergedCustomer`) is within the tested method, we need a way to verify that.
In other words, Mockito allows you to capture arguments so that you can later run custom assertions on them.

	@Mock
	private CustomerDao customerDao;
	
	@Captor 
	Customer captor;
	
	@Test
	public void verifyMerge() {
		Customer c1 = makeCustomer("John", "Doe");
		Customer c2 = makeCustomer("Phil", "Doe");
		
		subject.merge(c1, c2);
		
		verify(customerDao).save(captor.capture());
		Customer merged = captor.getValue();
		
		assertThat(merged.getFirstName(), is("Phil"));
		verify(customerDao).remove(c1);
		verify(customerDao).remove(c2);
		
	}
	
In the above example, we pass the `captor` variable (initialised with the `@Captor` annotation) as an argument of `save()` for verification; this, internally. creates an Argument Matcher that **saves** the argument. Then, we retrieve the captured value with `captor.getValue()` and inspect it with standard assertions.

## Mockito anti-patterns

- Everything is a mock
- Do not mock value objects or data structures
- Don't mock type you don't own (like a 3rd party lib)
