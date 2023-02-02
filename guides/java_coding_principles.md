# Java Coding Principles

This guide describes a collection of good Java coding principles.

* **Auto-generate constructors:** Use *Lombok* over manual constructors, except when calling the super constructor.

* **Use @RequiredArgsConstructor:** Use `@RequiredArgsConstructor` over `@AllArgsConstructor` to ensure dependencies are marked as `final`.

* **Initialize collections:** Use `java.lang` over Guava  and `com.google.common.collect` where possible. Use `List.of` and `Set.of` over `ImmutableList.of` and `ImmutableSet.of`. Use `Map.of` over `ImmutableMap.builder()` for less than 10 entries. Be aware that `java.util` methods are immutable and do not accept null values in the collection nor as an argument to the `contains` method.

*  **Return empty collections:** For methods with collection based return type, return an empty collection instead of returning null. Avoid redundant null checks in calling code.

* **Avoid long streams:** Avoid very long and complex stream code blocks as it makes reading the code difficult. Find the right balance between readability and compact code.

* **Factor out utility functions:** Look for potential utility functions within long methods, and factor the code out into smaller, well-documented, static utility methods. This improves code readability and testability and ensures logic is handled consistently across the system.

* **Make methods do one thing:** Favor small, documented methods over long methods with inline comments. Make sure a method handles one concern, and split the method into multiple methods to handle multiple concerns. This makes code more readable, reusable and testable.

* **Write Javadoc:** Write proper Javadoc for methods. Fill out `@params`, `@return`. Use `{@link}` for class entity references. Use `{@code}` for inline code. Keep Javadoc up to date.

* **Immutable collections:** Do not directly modify collections which are passed into methods. This will lead hidden state changes from the perspective of the calling code. Make a copy of the collection internally before modifying it instead. Ensure unit tests use immutable collections as arguments to detect internal collection modification.

* **Avoid null arguments:** Avoid having methods where calling code frequently uses `null` as arguments. This makes the code error prone. Favor a query object or enum instead, or refactor the logic to avoid null values.

  