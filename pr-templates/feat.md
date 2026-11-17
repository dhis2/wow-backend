## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on what users cannot do today and why they need it, linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the feature and how to use it (endpoint, parameter, setting)

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* new parameter X on endpoint Y
* behaviour change: Z now returns 404

1 indicator line on AI disclaimer/use


## Example 1 (based on dhis2/dhis2-core#25977)

### Problem
`POST /api/dataAnalysis/validationRules` runs all rules or the rules of one group (`vrg`).
To run one rule, users must make a group only for that rule.

### Solution
The request body accepts an optional `vr` list of rule UIDs.
The analysis runs only the listed rules, on the same org units and periods.

**Caveats**
- Maximum 50 rules in a request. `vr` together with `vrg` gives 400.
- Unknown UIDs in `vr` give 404 with the missing UIDs.
- Behaviour change: an unknown `vrg` now gives 404. Before, it ran all rules in the system.

Changes made by AI 🤖


## Example 2 (based on dhis2/dhis2-core#26064)

Revisits #23598.

### Problem
A missing or wrong `server.base.url` breaks links in emails and in shared interpretations.
Since #23628 the server logs a warning at startup.
System admins often cannot read the logs, so they do not see the warning.

### Solution
A new data integrity check `server_base_url_not_configured` reports a missing, blank or invalid URL.
The check and the startup warning use the same `ServerBaseUrlValidator`.

**Changes**
- `registerNonDatabaseIntegrityCheck` gets an `isSlow` parameter. This check is fast, so it runs by default.
- A blank value now also counts as "not set".

Code by AI 🤖, reviewed by the author


## Example 3 (based on dhis2/dhis2-core#25405)

### Problem
`java -jar dhis.war` did not stop Tomcat on SIGTERM, Ctrl-C or `systemctl stop`.
The Spring context did not close, so jobs, the connection pool and caches did not stop.
The `/tmp/tomcat.*` folders stayed on disk.

### Solution
A JVM shutdown hook stops Tomcat, which closes the Spring context.
Then the hook deletes the Tomcat base folder and stops Log4j.

**Caveats**
- A stop signal during startup still exits immediately.
- The Log4j shutdown hook is off, so the shutdown logs stay complete.

AI Assisted 🤖
