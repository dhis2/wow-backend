# Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

**Jira**: [full link to the Jira]

### Problem
1-3 sentences on the test gap or test failure (missing, flaky or wrong), linking it to key place or entry point in the code

### Solution
1-3 sentences summarizing the test change or addition; use bullets for several separate parts


# Example 1 (based on dhis2/dhis2-core#26137)

### Problem
Surefire runs only classes named `Test*`, `*Test`, `*Tests` or `*TestCase`.
Some data integrity controller test classes do not have this suffix, so CI never ran them.
Thus nobody found two bugs in the user org unit checks.

### Solution
Rename these classes to end in `Test`.

AI Assisted


# Example 2 (based on dhis2/dhis2-core#26183)

### Problem
On Jenkins, `dhis-test-web-api` runs all tests in one JVM with 2 GB heap.
`OpenApiControllerTest` generates an R client for the full API and needs about 800 MB.
When this test runs late, the heap is full and the build fails.

### Solution
Run `OpenApiControllerTest` in a separate surefire execution with a new JVM.
The new `openapi-own-jvm` profile in `dhis-test-web-api` does this.
With `-Dtest` the profile is off, so local runs execute only the requested tests.


# Example 3 (based on dhis2/dhis2-core#26281)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22429

### Problem
`PerfLandMnchTrackerTest` is one long list of requests.
It is hard to see which Capture screen sends a request.
The ANC program cannot use the same requests again.

### Solution
- Group the requests by user journey and by screen, as Capture shows them.
- The journeys do not depend on one program, so ANC can use them too.
- The dashboard and the event page send requests concurrently, as Capture does.
  This needs Gatling 3.15 or later, so Gatling goes to 3.16.1.
