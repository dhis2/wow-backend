## Template

### Problem
1-2 paragraphs summarizing the bug linking it to key place or entry point in the code

### Solution
1-2 paragraphs summarizing the fix

**Changes/Caveats/...** (optional bullet list of changes for larger PRs)
* now handles X
* changed Y to throw when Z

1 indicator line on AI disclaimer/use 
1 indicator line qualifying test coverage


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
