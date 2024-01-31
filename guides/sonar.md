# Sonar
We use sonar to help us write clean, quality, secure code.  
SonarLint should be used during local development to:
- catch issues early
- easily resolve existing issues (usually code smells)

Useful links:  
- [dhis2-core sonar project link](https://sonarcloud.io/project/overview?id=dhis2_dhis2-core)  
- weekly backend team
  - [meeting](https://meet.google.com/upy-nibq-wnd)
  - [agenda](https://www.google.com/url?q=https://docs.google.com/document/d/1rNoPNKcm1B4yGBtR85frXTKylZgBW3g0MZzVCAbeJ94/edit%23heading%3Dh.blgdisivf792&sa=D&source=calendar&ust=1707084037533033&usg=AOvVaw0V7Sd55NRFeQ_QzmiSVRGl)

## Pull Requests
Sonar is currently a mandatory step in the PR process. It has to pass in order for a PR to be allowed to merge.

If a PR is blocked by what we think is a trivial/nuisance issue, these can be marked as 'won't fix' (e.g. 'please define a string literal'). This issue should then be brought up at the next weekly meeting.

## Updating Rules
We can define what works best for us. If there are issues that we believe are not helping us we can remove these. We can go about that in the following way:
- add a topic to the weekly team meeting agenda
  - include the rule to be raised
  - points to be discussed
- we can discuss as a team and decide what to agree on

## Vulnerabilities
Vulnerabilities should be raised as priority issues at the weekly backend team meeting where a decision should be made on the action required for that issue. We should aim to have no outstanding vulnerabilities.

## Bugs
Developers have agreed to try and resolve 1 bug each per month.

## Code Smells
Opportunities when to tackle code smells
- no outstanding bugs or vulnerabilities
- take a break between longer development stints by taking on some smaller items
- easy place for new joiners to start to get comfortable with the code (bugs also)

## Severity
Always choose a higher-rated issue if possible (high, medium, low).
