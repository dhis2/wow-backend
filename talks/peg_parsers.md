---
theme: default
class: invert
headingDivider: 2
---

# PEG Parsers

Original source is found at https://github.com/dhis2/expression-parser/blob/main/PRESENTATION.md

## DHIS2 Expression Language

What is DHIS2 expression language?

```js
    // math
    1 + 1

    // functions
    log(100)

    // logic
    true && 2 > 1

    // data
    #{abcdefghijk}
```


## Parsing - Grammars - Terminal vs. Non-Terminal

Butchered (but useful) terminology:

**Terminal**: 

- something that **is not** composed of parts
- a leaf in a tree

Examples: literals (numbers, constants, strings)


**Non-Terminal**: 

- something that **is** composed of parts
- a node in a tree

Examples: operators


## Parsing - Grammars - Production Rules

```
NonTerminal = (NonTerminal | Terminal)+
```
The non-terminal on the left is defined as the sequence of non-terminal and terminals on the right.

More (usually):
* `a | b` => a OR b (in order of precedence)
* `+` left block 1 or more times
* `*` left block 0 or more times
* `?` left block 0 or 1 times
* `{n}` left block exactly _n_ times
* `{n,m}` left block at least _n_ but at most _m_ times
* `(a b)` grouping to a block
* `[a-z]` a character set of the letters a-z
* or `[a b]` ~~could mean: same as `(a b)?`~~ (not here)


## Parser Jargon

Terms

* _consume_: moving current position forward in the input
* _gobble_: consume and discard input (ignore, like WS)


## CFGs (Context-Free Grammars)

https://en.wikipedia.org/wiki/Context-free_grammar

* reply on precedence (order of declaration) to express intent
* use a "solver" to find the "best match" given a set of rules

A toy expression language:
```
expr = term '*' term
     | term '+' term
term = number | constant
```

## CFGs (Context-Free Grammars) - Example

Example expression:
```
a + b * c + d
```
a possible AST
```
    +
   / \
  +   d
 / \
a   *
   / \
  b   c
```
or short `(a + (b * c)) + d `; but could also be `a + ((b * c) + d)`



## Backtracking

Parsing is a left to right process...
```
((a + b) * c) + d
```
😩 that isn't right... lets go back and try again, this time trying something different
```
a + ((b * c) + d)
```
better 😌


**Parsing is somewhere between linear and factorial complexity**



## PEG (Parsing Expression Grammar)

https://en.wikipedia.org/wiki/Parsing_expression_grammar

* PEGs cannot be ambiguous (unlike CFGs)
* if a string parses, it has exactly one valid parse tree
* (presumably: OR not allowed in production rules) 


## PEG (Parsing Expression Grammar) - Example 

The toy example again, defined slightly different
```
expr = term (op term)*
term = number | constant
op   = '+' | '*'
```

After a `term` if there is a `+` or `*` there must be another `term`
and so forth, otherwise this is an illegal input for the language.

**Parsing is linear***

_* theoretically one could build backtracking into PEG parsers..._ 


## Lookahead

Usually refers to the number of "not yet consumed" characters in the input
that need to be considered to make the right choice.

```
expr   = number | date
number = [0-9]+('.'[0-9]+)?
date   = [0-9]{4}'.'[0-9]{2}'.'[0-9]{2}
```

How can we decide that we are reading a number or a date?

=> A date has two `.` 

We need to look ahead and see of if we find the second `.`

* PEG grammar must be "decidable" purely based on lookahead.
* Ideally the lookahead is 1 character only => fast, simple, unambiguous by design


## How to do correct operator precedence in linear time?

```
a + b * c + d
```
Linearly parsed gives
```
a + (b * (c + d))
```
😩

What if operators are leaves? We get:
```
a, +, b, *, c, +, d 
```
Everything is in a "flat" sequence of typed nodes.


## Recreating a tree from a flat sequence

Now we walk the "tree" and merge only the operator with the highest precedence 
into a structured operator with children:

```
1. a, +, (b * c), +, d
2. ((a + (b * c)) + d) 
```
Voila. 😌

The time is still linear as there is a fixed number of operators to do.


## CFG vs PEG

CFGs (ANTLR)

* bad syntax choices ("collisions") are first recognised much later (solver hides them)
* solver means a framework is used, which means limitations
* multiple transformations because of the layers of abstraction
* whitespace is hard to control as it is implicitly assumed 
* worst case complexity is factorial  
* => bend your problem to suit the parser


## CFG vs PEG II

PEGs

* decidability problem forces to recognise and solve collisions right away
* language methods are the "framework"
* direct translation (as complicated as needed but not more)
* just methods calling each other (possibly with a convenience layer on top)
* whitespace is no different but needs explicit consideration and modelling
* generally: "special" handling is not different
* worst case complexity is linear*
* => write the parser to suit the problem


## How do PEGs work?

Key idea:
```java
void what(Input in, Context ctx);
```
* _what_ is the name of the token/block processed
* `Input` 
  - is whatever is processed and "consumed" while parsing
* `Context` 
  - is whatever is build, the "output"
  - usually emitting the base data for creating nodes in an AST
  - also might hold state like lookup by name

Example Grammar:
```
expr = term (op term)*
term = number | constant
op   = '+' | '*'
```

## How do PEGs work? - Example Parser

PEG parser:
```java
void expr(Input in, Context ctx) {
    term(in, ctx);
    char c = in.lookahead();
    while (c == '+' || c == '*') { // isOperator(c)
        op(in, ctx);
        term(in, ctx);
        c = in.lookahead();
    }
}
void term(Input in, Context ctx) {
    in.consumeWhitespace();
    char c = in.lookahead();
    if (isDigit(c)) {
        number(in, ctx);
    } else if (isLetter(c)){
        constant(in, ctx);
    } else {
        throw in.error();    
    }
    in.consumeWhitespace();
}
void op(Input in, Context ctx) {
    char op = in.consume();
    ctx.emitOperator(op);
}
void number(Input in, Context ctx) {
    String n = in.consumeWhile(c -> isDigit(c) || c == '.');
    ctx.emitNumber(n);
}
void constant(Input in, Context ctx) {
    String c = in.consumeWhile(c -> isLetter(c));    
    ctx.emitConstant(c);
}
```
  