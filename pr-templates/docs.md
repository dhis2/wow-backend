## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs on what is missing, wrong or not clear in the documentation, and who needs it

### Solution
1-2 paragraphs summarizing the documentation change and where it is

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* moved page X to Y
* removed outdated section Z

1 indicator line on AI disclaimer/use

1 indicator line qualifying test coverage


## Example 1 (based on dhis2/dhis2-core#24207)

### Problem
To write a Gatling scenario by hand takes a long time.
The performance test module has no guide on how to record a scenario in the browser.

### Solution
Add a Gatling Recorder guide to `dhis-test-performance`.
It shows how to record a browser session and change it into a simulation.

No AI used

Docs only.


## Example 2 (based on dhis2/dhis2-core#22626)

### Problem
The README says that our Docker Compose setup is ready for production.
It is not ready yet.

### Solution
Change the text: the Docker Compose setup is work in progress.

No AI used

Docs only.


## Example 3 (based on dhis2/dhis2-core#23872)

### Problem
The performance tests README does not describe the CI runner.
Contributors do not know that each run has exclusive use of one shared self-hosted runner.

### Solution
Add a short paragraph to the CI section.
It links the runner.
It asks contributors to try changes locally and to use CI only for published numbers.

Changes made by AI 🤖

Docs only.
