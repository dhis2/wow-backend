# Updates to OpenAPI in 2.42

## Overview

**Major**

* Java `Class` to input + output schema
* `@OpenApi.Description` annotation to be used for endpoints, parameters and responses
* `@OpenApi.Document` for grouping controllers into OpenAPI documents
* `@OpenApi.Tag` got removed (tags are computed, not user defined due to their special treatmeant)
* `@OpenApi.Filter` to limit visibility of inherited endpoints


**Minor**

* `deprecated` picked up from `@Deprecated`
* `required` considers more sources (e.g. `@Nonnull`)
* all `UID` "links" refer to `IdentifiableObject` `Class`es
* `@OpenApi.Identifiable` to declare the UID type for views of `IdentifiableObject`s

**Scaleing**

* reduce schemas included in a document to those actually referenced
* => named schemas are last in the document
* all named types are "singletons" (simpler, less work)
* skip properties that have the same value as the one that is assumed when they are omitted
* no description defaults to `?` (required) or ommitted (non-required)

**Readability**

* compact (single line) arrays
* no unnecessary empty lines
* alphabetical sorting of named schemas (UIDs at the end)


   
## Outlook Descriptions

Allow descriptions on inherited methods to contain placeholders for the `OpenApi.EntityType`
so that annotations can be useful on methods that are inherited to many different object types. 
