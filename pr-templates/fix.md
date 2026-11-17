# Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

**Jira**: [full link to the Jira]

## Problem
1-3 sentences summarizing the bug linking it to key place or entry point in the code

## Solution
1-3 sentences summarizing the fix

## Proof
1 paragraph explaining how we prove it's fixed, ideally a test

## (optional) Caveats
max 1 paragraph


# Example 1

## Problem
Users (even admins) could not delete existing data that would not pass validation in `DefaultDataEntryService.validate`.
The data was not consistent with the metadata.

## Solution
Deletions do no longer validate consistency with the metadata.
This only excepts imports that are deletions only.

## Proof
New tests verify deletions of any data are possible.

## Caveats
Deletion counts in report reflect actual rows deleted.
ATM duplicate keys are undetected for default expressed as `null` one time and as default `UID` another time.
DS completion now skips lock-status check for admins to be symmetrical with data entry.

AI Assisted


# Example 2 (based on dhis2/dhis2-core#26246)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22482

## Problem
Program rule ASSIGN actions failed with E1302 for NUMBER results of 10,000,000 or more with decimals.
The rule engine gives such values in scientific notation (`5.309339325E7`).
NUMBER validation rejects this notation after `AssignDataValueExecutor` writes it to the payload.

## Solution
The executors do not change a payload value that is equal to the assigned value.
They write all other assigned numbers in plain decimal notation (`53093393.25`).

## Proof
In `AssignDataValueExecutorTest`, a rule assigns `5.309339325E7` to an empty data value.
The payload then holds `53093393.25`.


# Example 3 (based on dhis2/dhis2-core#26039)

Follow-up to #26010.

## Problem
`/api/dataApprovals/openapi.json` (also `.yaml` and `.html`) returned an empty document.
#26010 mapped `DataApprovalController` at `/api`, so the controller lost its derived OpenAPI path classifier.

## Solution
Declare `path:/api/dataApprovals` in the `@OpenApi.Document` classifiers.
The document now also lists the `/api/dataAcceptances` endpoints of the same controller.

## Proof
`OpenApiControllerTest#testGetPathOpenApiDocument_ControllerMappedAtApiRoot` fails without the fix and passes with it.

AI Assisted


# Example 4 (based on dhis2/dhis2-core#26256)

**Jira**: https://dhis2.atlassian.net/browse/DHIS2-22492

## Problem
`OUG{}` (the count of org unit group members) gives 0 in predictors and validation rules, with no error.
`ItemOrgUnitGroupCount` reads the count from `ExpressionParams.orgUnitCountMap`.
Only analytics fills this map, for indicators.

## Solution
A new store query counts the group members in the subtree of each org unit at one level.
Predictors and validation rules run this query when an expression uses `OUG{}`.
Indicators still use the analytics map.

## Proof
`PredictionServiceTest.testPredictOrgUnitGroupCount` checks the counts on a small hierarchy.
Without the fix, all counts are 0.

## Caveats
The query runs one time for each org unit level.
On a database with 276k org units, one query takes about 0.4 to 0.6 seconds.

AI Assisted
