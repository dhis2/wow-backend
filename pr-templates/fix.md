## Template

(optional: link to other GH PR that is replaced or otherwise relevant in context)

### Problem
1-2 paragraphs summarizing the bug linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the fix

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* now handles X
* changed Y to throw when Z

1 indicator line on AI disclaimer/use 


## Example 1

### Problem 
Users (even admins) could not delete existing data that would not pass validation in `DefaultDataEntryService.validate` because of not being consistent with the metadata.

### Solution
Deletions do no longer validate consistency with the metadata. 
This only excepts imports that are deletions only.

**Caveats**
- deletion counts in report reflect actual rows deleted
- ATM duplicate keys are undetected for default expressed as `null` one time and as default `UID` another time
- DS completion now skips lock-status check for admins to be symmetrical with data entry

Changes made by AI 🤖

New tests verify deletions of any data are possible.


## Example 2 (based on dhis2/dhis2-core#26246)

### Problem
Program rule ASSIGN actions failed with E1302 for NUMBER results of 10,000,000 or more with decimals.
The rule engine gives such values in scientific notation (`5.309339325E7`).
NUMBER validation rejects this notation after `AssignDataValueExecutor` writes it to the payload.

### Solution
The executors do not change a payload value that is equal to the assigned value.
They write all other assigned numbers in plain decimal notation (`53093393.25`).

Changes made by AI 🤖


## Example 3 (based on dhis2/dhis2-core#26039)

Follow-up to #26010.

### Problem
`/api/dataApprovals/openapi.json` (also `.yaml` and `.html`) returned an empty document.
#26010 mapped `DataApprovalController` at `/api`, so the controller lost its derived OpenAPI path classifier.

### Solution
Declare `path:/api/dataApprovals` in the `@OpenApi.Document` classifiers.
The document now also lists the `/api/dataAcceptances` endpoints of the same controller.

AI Assisted 🤖
