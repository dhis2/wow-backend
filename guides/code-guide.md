# Code Best Practices and Conventions

## Transactions
Transaction handling is done on the service level. 
All `public` methods of a `@Service` level bean should be annotated with one of the following

* `@Transactional(readOnly=true)`: a **reading** TX handled by spring opens/closes, usually uses stores, might call other services
* `@Transactional`: a **writing** TX handled by spring opens/closes, usually uses stores, might call other services
* `@IndirectTransactional`, a TX happens but not via spring, usually using programmatic TX via JDBC
* `@NonTransactional`, there is no TX, just computation, maybe cache access and alike

> [!Note]
> There are a few exceptions where `@Transactional` is used on the store level.
> In some special circumstances this is needed to avoid a otherwise taskless intermediate service level.
> Don't get inspired by these ;)

## Lombok
Limit use of lombok to the following annotations:

* `@AllArgsConstructor`, `@NoArgsConstructor`, `@RequiredArgsConstructor` (preferrred)
* `@Value` + `@With` or `@Data` or `@ToString` + `@EqualsAndHashCode` + `@Getter` + `@Setter` 
* `@Builder` + `Builder.@Default` + `@Singular`
* `@Accessors`
* `@Slf4j`

> [!Caution]
> `@ToString` and `@EqualsAndHashCode` require to think about the fields that should
> be included or excluded. Use the `@Include` and `@Exclude` annotations.
> The preferred default for objects which should not include all fields is to use
> explciit inclusion. 

> [!Important]
> The codebase contains a few more annotations in a few places.
> These should be removed/replaced. Specifically `@SneakyThrows` should not be used!

## Constructors
* use lombok annotations where possible, prefer `@RequiredArgsConstructor` and mark fields `final`
* use `record`s over lombok where possible
* spring injected contstructors do not need nullability annotations

## Nullability & Immutability
* avoid allowing `null` as a possible value
* use `@Nonnull` and `@CheckForNull` in `interface`s (and where it seems benefitial)
* use immutable value types as much as possible
* assume objects passed into a public method are immutable

## Collections & Streams
* return empty collections, not `null`
* assume collections are immutable unless they have been created within the scope (method, file)
* avoid "nested" streams, a stream should be a chain of operations on the same level
* use JDK collections only
* use `List.of`, `Set.of`, `Map.of`, `List.copyOf`, `Set.copyOf`, `Map.copyOf` where possible
* use stream `toList()` when possible (allows `null`)

> [!Caution]
> `List.of`, `Set.of`, `Map.of`, `List.copyOf`, `Set.copyOf`, `Map.copyOf` and alike do not allow
> `null` as a value nor calling methods like `contains` with `null`.
> Before using them consider if `null` is a possibility.
> Note also that `Set.of` does not allow duplicates in the source collection,
> `Map.of` does not preseve order.

## Utilities
* provide operations on **simple** types
* operations that require complex types should be located in a service
* should not accept persisted objects (exception: test helpers)
* should not accept spring beans (exception: test helpers)

## Javadoc
* document `interface`s with javadoc
* don't repeat facts the code already communicates
* make use of `{@link}` and `{@code}`

## Naming Conventions
* a bean annotated `@Service` should have the `Service` suffix
* a bean annotated `@Repositiry` should have the `Store` suffix
* a bean annotated `@Configuration` should have the `Config` suffix
* a dedicated record-like class used for an endpoint's request body should have the `Request` suffix
* a dedicated record-like class used for an endpoint's response body should have the `Response` suffix
* a dedicated record-like class used for an endpoint's parameters should have `Params` suffix 
* a test class should have the `Test` suffix
* an abstract text class should have the `TestBase` suffix
* a `get` store or service method should never return `null`, but throw an exception if no result exists
* a `find` store or service method should return an `Optional<X>` if no result exists
* use `of` and `copyOf` for factory methods where suitable, e.g. `UID.of`
