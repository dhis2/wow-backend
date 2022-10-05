# Preferred Coding Patterns

The presented patterns are meant as a general guide but should not be understood 
as rules to follow blindly or use as a knockout argument or sledgehammer 
approach to everything. Each problem deserves to be judged individually 
considering all its aspects and complexity when choosing a fitting solution. 

However, when in doubt which approach might be more fitting the guides provide
a reasoning and direction with the goal of a more uniform codebase which can
benefit from the advantages that emerge when using the described patterns.

## Overview
| Pattern | Prefer | Over                    |
|---------|---------------------|-------------------------|
| Consider collection unmodifiable | copy before modification | copy before returning |

## Patterns

Provides more detailed reasoning why and when to use a certain pattern. 

### Consider Collections as _unmodifiable_
When working with collections errors can arise from trying to manipulate an
_unmodifiable_ collection. One way to defend against this is to make copies of
collections to be sure they can be modified by a consumer. This often results
in collections being copied multiple times over as they pass through the layers
of abstractions and the application architecture. The other approach to this
is to generally consider any collection that wasn't created within or as part 
of the code that wants to modify the collection as _unmodifiable_. 

In practice this means any collection received from a virtual method call or
as parameter to a method should be considered _unmodifiable_ and copied once
where the algorithm needs a modifiable collection.

**Goals:** 
* keep copying of collections to a minimum
* make code easy to understand and reason about
* make code about the essential problem (less ceremony/clutter)

**Exceptions** (known mutable collections)**:**
* collections of hibernate entities in DHIS2 entities
* collections created in or as part of the algorithm (same method, 
  other `private` helper methods and alike)

**Also:**
* consider using alternative algorithms that can avoid manipulation, 
  e.g. `stream().map(...)` and alike.