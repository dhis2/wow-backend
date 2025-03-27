# Code Best Practices and Agreements

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
* `@Builder` + `Builder.@Default`
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
