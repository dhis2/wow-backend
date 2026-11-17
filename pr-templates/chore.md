## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on why the clean-up or maintenance is necessary, linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the change; say if the behaviour stays the same

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* removed X
* Flyway migration deletes Y

1 indicator line on AI disclaimer/use

1 indicator line qualifying test coverage


## Example 1 (based on dhis2/dhis2-core#25979)

### Problem
The `TWO_YEARLY` period type stopped working in 2011.
We decided to remove it in 2.44.

### Solution
Remove `TWO_YEARLY` from the code.
A Flyway migration deletes its periods and its period type.

**Caveats**
- The migration keeps them if a data set or a data approval workflow uses the type.
  Then it logs an error, and an admin must clean up by hand.

Code: human, Flyway: AI 🤖

Existing period tests pass without `TWO_YEARLY`.


## Example 2 (based on dhis2/dhis2-core#26066)

### Problem
Data integrity check selection (`checks=program*`) uses a regex to match wildcard names.
A regex is more than this simple match needs.

### Solution
A small matcher, `DefaultDataIntegrityService.matchesWildcard`, replaces the regex.
The behaviour stays the same: `*` matches any characters.
Names are still lower case, with `-` changed to `_`.

Changes made by AI 🤖

A new test compares the matcher with the old regex on 5,000 random pairs.


## Example 3 (based on dhis2/dhis2-core#26096)

### Problem
Our tests use three different PostGIS images.
The e2e image `postgis/postgis:16-3.5-alpine` is available for amd64 only.

### Solution
Use `ghcr.io/baosystems/postgis:16-3.5` in the integration and e2e tests.
Performance tests and `docker-compose.yml` already use it.
It is Debian based, like most production servers.

**Caveats**
- The collation stays `C` (`LC_COLLATE=C`).

No AI used

Integration and e2e tests pass on the new image.
