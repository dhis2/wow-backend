# Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

**Jira**: [full link to the Jira]

## What
1-3 sentences on what the clean-up or maintenance changes and why it is necessary, linking it to key place or entry point in the code


# Example 1 (based on dhis2/dhis2-core#25817)

## What
The performance tests download async-profiler 4.4 in `docker-compose.profile.yml`.
This PR changes the version to 4.6.
Version 4.6 adds a tree view to `profile.html` and shows real units in flame graphs.
It is a drop-in update, so the profile scripts do not change.
DHIS2 code, the API and the database do not change.


# Example 2 (based on dhis2/dhis2-core#26066)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22396

## What
Data integrity check selection (`checks=program*`) uses a regex to match wildcard names.
A regex is more than this simple match needs.
A small matcher, `DefaultDataIntegrityService.matchesWildcard`, replaces the regex.
The behaviour stays the same: `*` matches any characters.

AI Assisted


# Example 3 (based on dhis2/dhis2-core#26096)

## What
Our tests use three different PostGIS images.
The e2e image `postgis/postgis:16-3.5-alpine` is available for amd64 only.
This PR uses `ghcr.io/baosystems/postgis:16-3.5` in the integration and e2e tests.
Performance tests and `docker-compose.yml` already use it.
The collation stays `C` (`LC_COLLATE=C`).
