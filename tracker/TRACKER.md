# Tracker

These are guidelines specific to the tracker team. As always there will be exceptions :yum: This
should be an active guide that we work on together :smile:.

Keep [the prime directive](http://retrospectivewiki.org/index.php?title=The_Prime_Directive) in mind
when reading about any examples and code :smile:.

## Naming

Naming is hard :sweat_smile: This guide will thus not relieve you of the burden of finding good
names :grin: It only provides a couple of things to consider to make tracker code more consistent
and easier to read. The following applies to packages, classes and variables.

IDEs give us type information. There is no need to repeat the type in a class or variable name.

Tracker code currently contains types prefixed with `Tracker`. Tracker code should be in the
`dhis-service-tracker` module or within a tracker package (like in `dhis-web-api`). It is thus clear
that we are in the context of `tracker`. We should therefore not prefix any tracker types with
`Tracker` as its superfluous.

Imagine you are in a `validation` package. There is no need to prefix or suffix all types with
`Validation` as the context is already given by the package. One exception is if a type is visible
outside the package. In such a case a prefix or suffix might be appropriate as it gives important
information and or distinguishes the type from similar ones. Tracker import consists of multiple
stages like `preprocess`, `validation`, ... If every stage returns an implementation of a `Result`
type it makes sense to name the implementations `PreprocessResult`, `ValidationResult`.

Consistency over personal preference. Stick to a name if we have already settled on one for a class
or package with a certain responsibility. For example `Store` is used for what you might know as
`Repository`. Use `Store` instead of what you favor. If you have a good reason for why another name
would be better discuss it within the team.

Spend time finding a good name. This can mean talking to a domain expert. Looking up potential names
in a dictionary or finding synonyms might also be a good idea. Distilling a [Ubiquitous
Language](https://martinfowler.com/bliki/UbiquitousLanguage.html) is useful beyond our code. We can
learn from domain-driven design even if we do not practice it. An example is that we talk about
`events` within the tracker domain. Related DB tables and types are named `programstageinstance` for
historical reasons. It is just an example of a translation we would not have to do when working with
our code if we would stick to the same domain terms everywhere.

**Do**
* be concise
* be consistent
* find and use known names from our domain

**Avoid**
* prefixing with the Maven module name
* prefixing with the current package name unless important context will be lost for exported types

TODO(ivo): discuss whether we prefer singular or plural and where. Should packages always be
singular?

## Javadoc

Documenting our modules, packages and types makes it easier for us to understand why this particular
code exists, what its responsibility is and how it can be used and extended.

### Package

Adding a `package-info.java` serves the above mentioned purpose. It tells us what can be found in it
and what should be put in it.

Mention its purpose, its entry and exit points with regards to the types it exposes. This can help
in navigating a large package. The `validation` package can be used as an example
[package-info.java](https://github.com/dhis2/dhis2-core/blob/20f4fb95e269fe6276ccc4d1ca88988f20cf5d64/dhis-2/dhis-services/dhis-service-tracker/src/main/java/org/hisp/dhis/tracker/validation/package-info.java).

