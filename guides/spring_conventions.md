# Spring DHIS2 conventions

## Bean definitions

Spring Beans are normal classes annotated with one of the standard Spring stereotype annotations:

- `@Repository`
- `@Service`
- `@Component`

### Repository

The `@Repository` stereotype is used to indicate that the class provides the mechanism for storage, retrieval, search, update and delete operation on objects. DHIS2 `*Store` classes are annotated with `@Repository`.

### @Service

The `@Service` annotation indicates that the class is responsible for some kind of business logic. DHIS2 `*Service` classes are annotated with `@Service`.

### @Component

We can use `@Component` across the application to mark the beans as Spring’s managed components. In DHIS2, any class that is not a Service or a data store and requires to be managed by Spring, can be annotated with `@Component`.

### Bean id

Each annotated Spring bean should have an `id` corresponding to the full path of the implementing interface.

```java
@Service( "org.hisp.dhis.analytics.AnalyticsTableManager" )
public class JdbcAnalyticsTableManager implements AnalyticsTableManager
{
	...
}
```

### Spring Configuration

Beans that are not defined using prototype annotations, are configured inside _ad-hoc_ classes, annotated with `@Configuration`. Annotating a class with the `@Configuration` indicates that the class can be used by the Spring IoC container as a source of bean definitions.

Each `@Configuration`-annotated class is located in a `config` package, within each subproject. A simple naming convention has been used when possible to name the `@Configuration` classes.
If a @Configuration contains only services or components, the name is `ServiceConfig`.
If a @Configuration contains only “*Store” classes, the name is `StoreConfig`.

Additionally, in order to avoid conflicts with `@Configuration` classes having the same name, each `@Configuration`-annotated class should have a unique id defined - based on the package name.

For instance, `@Configuration( "coreServiceConfig" )`.

## XML-based configuration

Spring XML-based configuration should be avoided.

## Injection

All Spring Beans should only use consutructor-based injection.

1. All the bean dependencies must be declared as `final`.
2. The bean should have one constructor, where all the dependencies are resolved.
3. The constructor should **not** be annotated with `@Autowired`.

Points 1. and 2. are fullfilled by lombok in the following example

```java
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
private final UserStore userStore;

    private UserGroupService userGroupService;

    private UserCredentialsStore userCredentialsStore;

    private UserAuthorityGroupStore userAuthorityGroupStore;

    private CurrentUserService currentUserService;

    private SystemSettingManager systemSettingManager;

    private PasswordManager passwordManager;
```

## Bean initialization

Use the `@PostConstruct` annotation to execute initialization code for a Spring bean.

