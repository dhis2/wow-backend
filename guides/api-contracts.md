# API Contracts

> [!Note]

> This is a proposal 

## Stability vs. Maintainability

DHIS values stability; however, its APIs reflect an evolving platform which cannot always keep all API details the same when the internals change.

Common reasons that force API details to change are:

* establish consistency across multiple endpoints and/or operations
* implementing equivalent operations using the same code
* correcting use of a bad default
* making validation explicit that has always been an (unchecked) assumption or requirement

Changes that are too numerous and/or hard to track to be included in changelogs 😵‍💫:

* HTTP error code changes from one `4xx` code to another `4xx` code
* HTTP success code changes from one `200` code to a more suitable `2xx` code (`201`, `204`)
* The  `message` of an error response object changes its phrasing

This means: a client should avoid to...

* ❌ expect a specific HTTP response code (check `2xx` 😃 not `200` 🥲)
* ❌ parse an error `message` to extract parts 🥲 (use arguments data where available)
