---
theme: default
class: invert
headingDivider: 2
---

# Reflection, Generics & Type Erasure
 

A lengthy and dry topic - but you asked for it 😜 

## Reflection - Inspection

**Reflection ~ "inspection as declared in source"**

What can be inspected?

* "raw type": `Class`
* "generic type": `java.lang.reflect.Type`
* names
* members
* parameters
* exceptions
* => "signatures"
* annotations


## Reflection - Manipulation


🚧 Not in this talk 🚧


## Reflection - Accessibility

What is reflective access?

Not:
* `Class.getEnumConstants()`
* `Class.getRecordComponents()`
* `Class.getName()` & co (names, package, module)
* `Class.isInterface()` & co (only read modifier flags) 
*  => `Class.getModifiers()` (also exist on methods and fields)

Pretty much everything else shown soon is considered "reflection".

**OBS!** This matters because with Java modules types are generally inaccessible for reflection unless they are explicitly `open` for it.


## Type Inspection - Element Type

Type of the element itself:

| returns =>    | `Class`               | `java.lang.reflect.Type` |
|---------------|-----------------------|--------------------------|
| `Method`      | `getReturnType()`     | `getGenericReturnType()` |
| `Field`       | `getType()`           | `getGenericType()`       |
| `Constructor` | `getDeclaringClass()` | -                        |
| `Parameter`   | `getType()`           | `getParameterizedType()` |


## Type Inspection - `Executable` Parameters

Type of parameters:

| returns =>    | `Class[]`             | `java.lang.reflect.Type[]`   |
|---------------|-----------------------|------------------------------|
| `Method`      | `getParameterTypes()` | `getGenericParameterTypes()` |
| `Constructor` | `getParameterTypes()` | `getGenericParameterTypes()` |

Alternative: `getParameters()` => `Parameter[]`

**OBS!** `Parameter` does **not** have a `getIndex()` 😩


## Declarations - `Member`s

Child elements of `Class`es:

| returns         | _public_ "children" (+inherited) | all _local_ "children" (-inherited) | 
|-----------------|----------------------------------|-------------------------------------|
| `Method[]`      | `getMethods()`                   | `getDeclaredMethods()`              |
| `Field[]`       | `getFields()`                    | `getDeclaredFields()`               |
| `Constructor[]` | `getConstructors()`              | `getDeclaredConstructors()`         |


## Declarations - Parents

From child back to its "parent":

| "child"       | "parent" element           | returns      | 
|---------------|----------------------------|--------------|
| `Method`      | `getDeclaringClass()`      | `Class`      |
| `Field`       | `getDeclaringClass()`      | `Class`      |
| `Constructor` | `getDeclaringClass()`      | `Class`      |
| `Parameter`   | `getDeclaringExecutable()` | `Executable` |


## Declarations - Inheritance

Super*

| `Class` method           | returns            |
|--------------------------|--------------------|
| `getSuperclass()`        | `Class<? super T>` |
| `getGenericSuperclass()` | `Type`             |
| `getInterfaces()`        | `Class<?>[]`       |
| `getGenericInterfaces()` | `Type[]`           |


## Names

Names of elements:

|               | name          |
|---------------|---------------|
| `Method`      | `getName()`   |
| `Field`       | `getName()`   |
| `Constructor` | `getName()`*  |
| `Parameter`   | `getName()`** |

- *: = `getDeclaringClass().getName()`
- **: **OBS!** only available with compiler option `-parameters`


## Annotations

Essential:
```java
interface AnnotatedElement {
    // check
    boolean isAnnotationPresent( Class<? extends Annotation> type );
    
    // single
    <A extends Annotation> A getAnnotation( Class<A> type );
    
    // repeater
    <A extends Annotation> A[] getAnnotationsByType( Class<A> type );
    
    //...
}
```

## Annotations - `@Repeatable` Annotations

```java
@Target( ElementType.PARAMETER )
@Retention( RetentionPolicy.RUNTIME )
@Repeatable( Params.class )
@interface Param
{
    String name();
}

@Target( ElementType.PARAMETER )
@Retention( RetentionPolicy.RUNTIME )
@interface Params
{
    Param[] value();
}
```


## Annotations - Surprises 

| Method                  | `@Repeatable` transparent | 
|-------------------------|---------------------------|
| `isAnnotationPresent`   | no 😰                     |
| `getAnnotation`         | no 😰                     |
| `getAnnotationsByType`  | yes                       |

Workarounds: 
- use only `getAnnotationsByType`
- use `ConsistentAnnotatedElement`

More surprises: `@Inherited`, spring & co


## Annotations - Are Just Interfaces

```java
@interface Name {
    String value();
}

record NameValue(
    String value
) implements Name {
    @Override 
    public Class<? extends Annotation> annotationType() {
        return Name.class;
    }
}
```
This works just fine:
```java
Name annotation = new NameValue("hello");
```
(also: Implemented by `Proxy`)


## "Generics" 

`java.lang.reflect.Type` Flavours:

* `Class` Types (all types before 1.5; a.k.a "raw types"): `String`, `Boolean`, ...
* `ParameterizedType`: `List<T>`
* `TypeVariable`: `<T>`
* `WildcardType`: `<? super Number>`, `<? extends Number>`, `<?>`
* `GenericArrayType`: `T[]`

(What needs to be considered by code trying to handle "all types")


## "Generics" - Class Types vs. Raw Types

What is the difference?

* `String` is a _class type_
* `List` is a _raw type_ of a parameterized type `List<T>`
* Array types `String[]` are _class types_.
* (confusingly `Class<?>` itself is a parameterized type)


## "Generics" - `ParameterizedType`s

Are types with **type parameters** (free _type variables_; here `A`, `B`)

```java
interface Function<A, B> {
    B apply( A a );
}
```
See 
* `Class.getTypeParameters()` => `TypeVariable[]`
* `ParameterizedType.getRawType()` => `Type` is always: `Class<?>`
* `ParameterizedType.getActualTypeArguments()` => `Type[]`


## "Generics" - Parameterized Types II

Not to be confused with _type arguments_ (here `String`)
```java
class StringList extends ArrayList<String> {}
```


## "Generics" - `TypeVariable`s

- Are named type placeholders
- By convention use single letter upper case names

When type parameters occur directly as type (here `T`) => `TypeVariable`
```java
// class level type parameters
interface Predicate<T> { boolean test(T value); }

class Util {
    // method level type parameters
    static <T> List<T> prepend(T e, List<T> tail);
}
```

See
* `Method.getTypeParameters()` => `TypeVariable[]`


## "Generics" - `WildcardType`s

Any subtype of ...
```java
interface Adder {
    
    int intSum( List<? extends Number> values );
}
```
`WildcardType.getUpperBounds()` => `Type[]`

Any supertype of ...

```java
interface Calculator {

    <T> void calc( T left, BinaryOperator<? super T> op, T right );
}
```
`WildcardType.getLowerBounds()` => `Type[]`


## "Generics" - `WildcardType`s II

Interesting...

* `<?>` is just an alias for `<? extends Object>`
* Why are upper bounds a `Type[]` array? 
* Because: `<T extends Member & AnnotatedElement>`
* Why are lower bounds a `Type[]` array?
* Because: reasons :D ATM there can only be one lower bound 

## "Generics" - `GenericArrayType`s

`T[]` is neither... 

- a _class type_ (because its element type is not a _class type_)
- nor a _type variable_ (because it is also an _array type_)

Tends to be forgotten


## "Generics" - Type Assignability

What? `<? extends X>` != `<? extends X>`? 

Two wildcard types are only compatible if they originate from the same capture.

**Solution:**
Use same type variable


## "Generics" - Type Assignability II

Why use wildcard types then?

```java
class Adder {

    static int intSum(List<? extends Number> values) {
        return values.stream().mapToInt(Number::intValue).sum();
    }
}
```
Can be called with:
```java
Adder.intSum(List.of(1, 2, 3));          // = 6
Adder.intSum(List.of(1.4f, 2.5f, 3.6f)); // = 6
```

## "Generics" - Type Assignability III

Similar...
```java
interface Calculator {
    
    <T> void calc( T left, BinaryOperator<?super T> op, T right );
}
```
Can be called with:
```java
BinaryOperator<Number> plusInt = (left, right) -> left.intValue() +  right.intValue();
Calculator c = new CalculatorImpl();
c.calc(1, plusInt, 2);       // = 3
c.calc(1.4f, plusInt, 2.5f); // = 3
```


## Type Erasure

What does type erasure entail?

* the JVM only supports _class types_ 
* => object instances can only "know" their _class type_ (which might be their _raw type_)
* => JVM call mechanics build on erased signatures 
    

## Type Erasure - Basics

Source:
```java
interface Consumer<T> {
    
    void apply( T e );
}
```

JVM:
```java
interface Consumer {
    
    void apply( Object e );
}
```


## Type Erasure - Bounds

Source:
```java
interface Parser {

    <T extends Number> T parse( String value, Function<String, T> toNumber );
}
```

JVM:
```java
interface Parser {

    Number parse( String value, Function toNumber );
}
```


## Type Erasure - Collisions

Source:
```java
interface Adder {

    Number add( List<String> values, Function<String, Number> toNumber );

    Integer add( List<Number> values, Function<Number, Integer> toInt );
}
```

JVM:
```java
interface Adder {

    Number add( List values, Function toNumber ); // 🚫 compiler error

    Integer add( List values, Function toInt ); // 🚫 compiler error
}
```


## Type Erasure - Bridge Methods

Source:
```java
interface Box<T> {
    void put(T value);
}
class StringBox implements Box<String> {
    public void put(String value) { }
}
```

JVM:
```java
interface Box {
    void put(Object value);
}
class StringBox implements Box {
    public void put(String value) { }
}
```

## Type Erasure - Bridge Methods II

```java
Box<String> box = new StringBox();
box.put("I get bridged"); // call put(Object) from Box interface
```

But `StringBox` defines `put` as `put(String)` 😱

```java
class StringBox implements Box {
    public void put(String value) { }
    // bridge method generated by the compiler
    public void put(Object value) { 
        put((String) value);
    }
}
```
Also: a "synthetic" method (modifiers) 


## Return Type Overrides

Not a "generics" feature, but it appears _as if_:

```java
interface Num {
    
    Num addInt(Int other);
}
class Int implements Num {
    
    Int addInt(Int other) {}
}
```
Return types are not part of the signature 🤯

It is allowed to _override_ them with a subtype

## Lessons

From this presentation...

* Reflection = "inspection as declared in source"
* Avoid raw types: `List<String>` over `List<?>` over `List`
* Introduce type variables to capture a wildcard type as "the same=compatible type" 

From experience...

* Avoid type parameters by design
  - 1 is **maybe** unavoidable 🤷
  - 2 is suspicious
  - &gt;= 3 is most likely bad design :D
  - => rethink the design, simplify (but don't hack around with casts or raw types)