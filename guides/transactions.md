# Transactions best practices

## Annotating methods

In DHIS2, transaction boundaries are specified declaratively, via the `@ org.springframework.transaction.annotation.Transactional` annotation on Service methods of concrete classes (as opposed to interfaces).

Each Service method that does use a Store class to access the database should be annotated with the `@Transactional` annotation.

### Read-only transactions

If the method does not require to modify the database (only read data), the `@Transaction` annotation should have the `readOnly` property set to `true`.

```java
@Transactional(readOnly = true)
public User getUser(Long id)
{
   ...
}
```

By setting the transaction as read-only, Hibernate flush mode is set to `FlushType.MANUAL` in the current Hibernate Session, preventing the session from committing the transaction. Furthermore, `setReadOnly(true)` will be called on the JDBC Connection, which is also a hint to the underlying database.

When entering a method annotated with a read-only transaction, Postgres sets the `SESSION CHARACTERISTICS` as `READ ONLY`:

`SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY;`

Note that a method annotated with `@Transactional(readOnly = true)` will throw an exception if there is any kind of database modification happening within the scope of that method.

If the read-only method has no need to be executed within the context of a database transaction, consider removing the annotation altogether.

### Non-annotated transactions
Some **public** service methods do not rely on spring annotation level transactions to allow a more fine grained transaction management.
Mostly this is used to avoid opening a transaction unless it is absolutly necessary.
Example are reading cached state, like settings, or the lazy creation of periods that should not affect transaction requirements of the calling code.
In such cases a service method should be annotated with `@IndirectTransactional` to inform the reader 
that this method is intentionally **not** annotated with `@Transactional` but it will potentially database access which is transparent to the caller.

### Non-transational service metods
Some **public** service methods are known to not doing any transactions at all. 
For example, they might just read or write to a memory cache.
Such methods should be annotated with `@NonTransactional` to inform the reader that this service method intentionally is **not** annotated with `@Transactional`.

## Annotating classes

A Service class should be annotated with the `@Transactional` annotation only if all the methods require a transaction with a specific attribute (e.g. all methods are read-only):

```java
@Transactional(readOnly = true)
public class UserService()
{
	public User getUser(Long id) {};

	public List<User> getUsers() {};

	public User getUserByUsername(String username) {};
}
```

## Boundaries

Transactional boundaries should always start at the Service layer.
Repository classes should not have methods annotated with the `@Transactional` annotation, unless there is a strong case for it.

## JPA/Hibernate and Transactions

If a Service method is marked as `@Transactional`, there is no need to explicitly call an Hibernate save operation. 
When a method is transactional, then entities retrieved within this transaction are in _managed_ state (https://vladmihalcea.com/a-beginners-guide-to-jpa-hibernate-entity-state-transitions), which means that all changes made to them will be persisted to the database automatically *at the end* of the transaction.

```java
@Transactional
public void changeName( long id, String name )
{
 	User user = userRepository.getById(id);
 	user.setName(name);
 	userRepository.save(user); // redundant!
}
```

In the above example, the last line is redundant.
