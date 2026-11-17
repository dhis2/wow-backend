# Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

**Jira**: [full link to the Jira]

## What
1-3 sentences on what the feature is

## Why
1-3 sentences on what users cannot do today and why they need it, linking it to key place or entry point in the code

## How
1-3 sentences summarizing the feature implementation and how to use it (endpoint, parameter, setting)

## (optional) Caveats
max 1 paragraph


# Example 1 (based on dhis2/dhis2-core#25977)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22371

## What
Validation rule analysis can run a list of rules, not only a rule group.

## Why
`POST /api/dataAnalysis/validationRules` runs all rules or the rules of one group (`vrg`).
To run one rule, users must make a group only for that rule.

## How
The request body accepts an optional `vr` list of rule UIDs, maximum 50.
The analysis runs only the listed rules, on the same org units and periods.

## Caveats
`vr` together with `vrg` gives 400, and unknown UIDs in `vr` give 404.
Behaviour change: an unknown `vrg` now gives 404. Before, it ran all rules in the system.

AI Assisted


# Example 2 (based on dhis2/dhis2-core#26064)

Revisits #23598.

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-21284

## What
A new data integrity check, `server_base_url_not_configured`, reports a missing, blank or invalid `server.base.url`.

## Why
A missing or wrong `server.base.url` breaks links in emails and in shared interpretations.
Since #23628 the server logs a warning at startup.
System admins often cannot read the logs, so they do not see the warning.

## How
The check and the startup warning use the same `ServerBaseUrlValidator`.
The check is fast, so it runs by default.

## Caveats
A blank value now also counts as "not set".
`registerNonDatabaseIntegrityCheck` gets an `isSlow` parameter.

AI Assisted


# Example 3 (based on dhis2/dhis2-core#25405)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-14977

## What
`java -jar dhis.war` now stops Tomcat and DHIS2 cleanly on a stop signal.

## Why
SIGTERM, Ctrl-C and `systemctl stop` did not stop Tomcat.
The Spring context did not close, so jobs, the connection pool and caches did not stop.
The `/tmp/tomcat.*` folders stayed on disk.

## How
A JVM shutdown hook in `Main` stops Tomcat, which closes the Spring context.
Then the hook deletes the Tomcat base folder and stops Log4j.

## Caveats
A stop signal during startup still exits immediately.
The Log4j shutdown hook is off, so the shutdown logs stay complete.

AI Assisted
