## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on what fails or is missing in CI, with the workflow, job or run

### Solution
1-2 paragraphs summarizing the change to the workflows or pipelines

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* needs release X of tool Y
* backports to follow

1 indicator line on AI disclaimer/use


## Example 1 (based on dhis2/dhis2-core#26258)

### Problem
New PR preview instances (`deploy` label) fail with `stack not found: dhis2-db`.
`deploy-instance.yml` finds the latest im-manager tag with `git ls-remote --sort='v:refname'`.
IM removed the `v` prefix at 0.69.0, and this sort puts all `v*` tags last.
Thus the workflow uses `v0.68.0`, which creates retired stacks.

### Solution
Sort on the version without an optional `v`.
The step logs the tag that it uses, and it fails if it finds no tag.

**Caveats**
- `destroy-instance.yml` gets the same fix.
- A restart of an existing instance was not broken.

AI Assisted 🤖


## Example 2 (based on dhis2/dhis2-core#26045)

### Problem
A restart of an IM Play or PR instance restarts the full stack, Postgres too.
DHIS2 can start before the database is ready.
Then DHIS2 stays unhealthy, and the `dhis2-core-dev` build stops.

### Solution
Restart only the `dhis2` component.
This applies to `jenkinsfiles/dev`, `jenkinsfiles/stable` and `deploy-instance.yml`.

**Caveats**
- This needs an im-manager release with `restart.sh <id> <component>`. Until then, IM ignores the extra argument.
- Backports to 2.43, 2.42 and 2.41 follow.

No AI used


## Example 3 (based on dhis2/dhis2-core#25491)

### Problem
The Codecov upload is not reliable.
Codecov outages fail CI, and its coverage numbers do not agree with local JaCoCo.
We cannot update from v3: v4 broke our build, and v5 needs a token.

### Solution
Remove the Codecov upload.
JaCoCo stays, so you can make coverage reports locally.

No AI used
