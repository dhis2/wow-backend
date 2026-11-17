## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on the test gap or test failure (missing, flaky or wrong), linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the test change

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* product code changes, if any
* new test dependency X

1 indicator line on AI disclaimer/use


## Example 1 (based on dhis2/dhis2-core#26137)

### Problem
Surefire runs only classes named `Test*`, `*Test`, `*Tests` or `*TestCase`.
Seven data integrity controller tests do not have this suffix, so CI never ran them.
Thus two bugs in the user org unit checks were not found.

### Solution
Rename the seven classes to end in `Test`.

Changes made by AI 🤖


## Example 2 (based on dhis2/dhis2-core#26183)

### Problem
On Jenkins, `dhis-test-web-api` runs all tests in one JVM with 2 GB heap.
`OpenApiControllerTest` generates an R client for the full API and needs about 800 MB.
When this test runs late, the heap is full and the build fails.

### Solution
Run `OpenApiControllerTest` in a separate surefire execution with a new JVM.
The new `openapi-own-jvm` profile in `dhis-test-web-api` does this.

**Caveats**
- With `-Dtest` the profile is off. Local runs execute only the requested tests, one time.
- No CI job sets `-Dtest`.

AI Assisted 🤖


## Example 3 (based on dhis2/dhis2-core#26281)

### Problem
`PerfLandMnchTrackerTest` is one long list of requests.
It is hard to see which Capture screen sends a request.
The ANC program cannot use the same requests again.

### Solution
Group the requests by user journey and by screen, as Capture shows them.
Each journey is built for a program, so ANC can use it too.

**Changes**
- The dashboard and the event page send requests concurrently, as Capture does.
- This needs Gatling 3.15 or later, so Gatling goes to 3.16.1.
- The 11 p95 thresholds stay on the same requests.

No AI used
