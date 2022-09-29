# Java 11+ Pitfalls
This page wants to point out mistakes that are easily made when using JDK11 features.
Mostly the pitfalls have their origin in reasonable expectations that aren't meat by the new APIs.

Overview
| Pitfall                                                    | Beware ... |
| ---------------------------------------------------------- | ---------- |
| `List.of` / `List.copyOf` as a replacement for `Arrays.asList` and alike   | `null` is not allowed |
| `collect(toUnmodifiableList())` instead of `collect(toList())` | `null` is not allowed |
| `Stream.forEach` as a replacement for `for`/`while` loops  | `forEach` does not guarantee order, consider `forEachOrdered` |
| `Map.of` to create maps with few entries                   | `null` is not allowed and map does not retain order of entries |
| `Set.of` for deduplication                                 | does not allow `null` or duplicates |

----

### `List.of` as a replacement for `Arrays.asList` and alike 
While `List.of` lets you create effectivly immutable `List`s 
they also have the special semantic of not allowing `null` values 
or the factory function will throw a `NullPointerException`.

Use `List.of` with care and can only replace `Arrays.asList` and co 
when the list is initialised with constants that are clearly not `null`.

Same is true for `List.copyOf` and its cousins `Set.copyOf` and `Map.copyOf`. 

----

### `collect(toUnmodifiableList())` instead of `collect(toList())`
Consistent with the immutable lists created by `List.of` 
the unmodifiable list created by a collector do also not allow `null` values.
If there is a chance for `null` values in the stream use `collect(toList())`.

In JDK16 `Stream.toList()` is added which results in an unmodifiable list which does allow `null` values.

----

### `Stream.forEach` as a replacement for `for`/`while` loops
While the name `forEach` is easily understood as the proper replacement for a `for`-each loop
the javadoc of `Stream.forEach` states: _The behavior of this operation is explicitly nondeterministic._
The proper replacement for ordered iteration is called `Stream.forEachOrdered`.

----

### `Map.of` to create maps with few entries
Consistent with `List.of` the `Map.of` has special semantics of not allowing `null` references
for both keys and values. 

A quick lock at the implementation `MapN` appears to preserve the order of key-value pairs. 
This is misleading. Maps created by `Map.of` do **not** provide a determenistic order.
To create a map with fixed entry order still a class like `LinkedHashMap` is required.

### `Set.of` to perform deduplication
Besides not allowing `null` values unmodifiable sets also do not allow duplicate values.
