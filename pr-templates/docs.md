# Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

**Jira**: [full link to the Jira]

### What
1-3 sentences on what is missing, wrong or not clear in the documentation, who needs it, and what this PR changes

# Example 1 (based on dhis2/dhis2-core#24207)

### What
To write a Gatling scenario by hand takes a long time.
The performance test module has no guide on how to record a scenario in the browser.
This PR adds a Gatling Recorder guide to `dhis-test-performance`.
It shows how to record a browser session and change it into a simulation.


# Example 2 (based on dhis2/dhis2-core#22626)

### What
The README says that our Docker Compose setup is ready for production.
It is not ready yet.
This PR changes the text: the Docker Compose setup is work in progress.


# Example 3 (based on dhis2/dhis2-core#23872)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-19797

### What
The performance tests README does not describe the CI runner.
Contributors do not know that each run has exclusive use of one shared self-hosted runner.
This PR adds a short paragraph with a link to the runner to the CI section.
It asks contributors to try changes locally and to use CI only for published numbers.
