## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on why the build, a dependency or the packaging must change, linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the change: which version or setting, and what it affects (shipped WAR or test scope only)

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* WAR size changes by X
* Dependabot ignores version Y

1 indicator line on AI disclaimer/use

1 indicator line qualifying test coverage


## Example 1 (based on dhis2/dhis2-core#25652)

### Problem
The tests use Spring REST Docs 2.0.8, which is built for Spring Framework 5.
DHIS2 uses Spring Framework 6.2.

### Solution
Update Spring REST Docs to 3.0.6, the last 3.0 release, built on Spring Framework 6.2.19.
It is in test scope only, so the WAR does not change.
One property changes, and no code changes.

**Caveats**
- Dependabot ignores REST Docs 4.0 and later (#25647).

AI Assisted 🤖

Unit tests and samples of the H2 and Postgres tests give the same results as the base.


## Example 2 (based on dhis2/dhis2-core#25403)

### Problem
The released stable WARs have no `Main-Class`.
Users cannot start them with `java -jar dhis.war`.

### Solution
Build the stable WAR with the `embedded` profile.
The WAR still works in an external Tomcat 10.1 and in the Docker image.

**Caveats**
- The WAR is about 26 MiB larger.
- Only `jenkinsfiles/stable` changes. The dev and EOS pipelines stay the same.
- A release manager must agree, because the published artifact changes.

AI Assisted 🤖

Checked by hand: the WAR starts with `java -jar`, in Tomcat 10.1 and in Docker.


## Example 3 (based on dhis2/dhis2-core#25413)

Cherry-pick of #23707 to 2.43.

### Problem
2.43 needs a newer json-tree version.
The update to json-tree 1.9 is on `master` only.

### Solution
Cherry-pick the update to 2.43.
One file had import conflicts.

No AI used

Existing tests pass on 2.43.
