# Guidelines for GitHub

The following guidelines have agreed upon in the backend team to formalize how we work with GitHub, and the expectations we have between us as developers.

A quick summary of the guidelines, followed by sections with more information for each point:

**Draft PRs**
1. Draft PRs can and should be used when you want to run the GitHub checks on your branch, receive review from specific people, or to easily share and discuss code.
2. Draft PRs should not be reviewed unless it has been requested by the author.
3. Draft PRs should be used over normal PRs marked "WIP", to avoid premature or accidental merging of incomplete code.
4. Draft PRs can be left for longer periods of time, but after 1 month of no change, action should be taken by the author

**PR life / age**
1. PRs should receive some feedback within 2 days, and within 5 days it should have 2 reviews. Exceptions for bigger or complicated PRs that require more effort to review.
2. The author is responsible to resolve any comment, fix any failing checks and requesting reviewers as needed.
3. The author is responsible for the PR from its creation, to its resolution, be it either merging or closing the PR.

**Reviews**
1. PRs against master should always have a minimum of 2 approvals.
2. PRs against previous versions only require 1 approval, but the author should require more approvals if a backport contains significantly different code than the original PR against master.

**Merging PRs**
1. The author is primarily responsible for merging their own PRs
2. Merging should only happen when all comments have been resolved
3. Auto-merging PRs should be used when the author is confident no further work is required
4. Other developers may only merge PRs they have not authored when all checks are OK, two approvals exist and no comment lies unresolved.


**GitHub conventions**
1. PR titles must follow the naming convention, prepending the title with "fix|feat|chore|test|ci|", based on the content of their PR.
2. All PRs (omitting Draft PRs) must have a description explaining the content of the PR.
3. All branches should be named on the format: "<Jira-issue-number>[_<version>]". Example DHIS2-123 and DHIS2-123_2.40.
4. PRs should be assigned to at least 2 reviewers, or a team of reviewers
5. Reviewers should primarily be in the same product team as the code is for, but exceptions are ok.


## Draft and Work-In-Progress (WIP) Progress
PRs that are not ready for, or meant for review or merging, can be created as DRAFT type PRs. These PRs can not be merged, meaning we avoid any premature or accidental additional to our main branches.

Draft PRs does not require reviews, so unless requested by the author, draft PRs can be ignored when looking through the list of PRs.

Common use-cases for draft PRs include running GitHub checks, getting feedback on code or ideas, long-lasting issues that require repeated feedback, or GitHub checks before it is ready, etc.

Instead of naming PRs "WIP" and such, PRs should be of the DRAFT type.

Due to the use-cases of drafts, leaving them hanging around for longer periods of time is fine, but after 1 month since creation, the author should consider some action to resolve it. Exceptions will of course happen in some cases, the core idea is to make sure no PRs, even drafts, are forgotten.

## PR Lifecycle
The author, who created the PR, is responsible for fixing any failing checks, resolving any comments made by reviewers and merging their own PRs. they are also responsible for picking people or team(s) to review the PR.
If a PR has seen no response at all after 2 days, the author should follow up with other developers to get reviews, or understand why it's not moving forward.
If a PR does not have 2 reviews after 5 days, or has no unresolved comments after 5 days, action should be taken by the author to resolve any outstanding issues that are blocking the PR.

The overall goal is to get your code merged in reasonable time, avoiding the challenge of working on too many issues/PRs at the same time.

Exceptions will happen in cases of big or complicated PRs that require more effort when reviewing.

## Reviews
Reviewers are expected to understand the code in the PR to at least a basic degree, and provide feedback or raise questions regarding the correctness of the code, as well as the quality of the code, tests and documentation. 

PRs against master should have at least 2 approvals before merging, while backports (PRs that already have been reviewed for master) only require a single approval. Depending on whether the backport has a significant difference in the code than the original PR, the author should request additional reviews if they think its appropriate.

## Merging
The author of the PR is the main person responsible for merging the PR. A PR should only be merged if all comments are resolved, all checks are OK, and 2 approval has been given. If the author is confident the PR needs no further work, they should use the auto-merge feature to avoid having to follow up later just to merge it manually.

Other people may merge PRs if its appropriate, as long as all checks are OK, approvals are OK and no comments are unresolved. However, they should give the author the time to merge it themselves, just in case there is some outstanding feedback not in the PR.

## GitHub conventions
Developers must follow the common conventions for naming and interacting with GitHub to facilitate good collaboration between eachother.

When creating a new branch, it should be named based on the issue you are working on. For example, if you are working on issue DHIS2-123, the branch name would be `DHIS2-123`. If DHIS2-123 would be subject to backporting, the branches for each backport should be post-fixed with the version it will be backported to: `DHIS2-123_2.40` and `DHIS2-123_2.39.4`.

Currently, some work does not warrant it's own issue, and there is no "simple" way to create a minimal issue. Those are currently the only exception to the naming-conventions, but this will change in the future to make sure all PRs and commits can be linked back to Jira.

All non-draft PRs requires some description. The description should explain the purpose of the PR at the very least, but can also include information about specific changes made, decisions made, how to use it and more. The more detailed big PRs are, the easier it will be to review them.

PR titles have to follow the semantic naming conventions, which means pre-pending the PR titles with the appropriate keyword for your PR:
- feat: new feature
- fix: bug fix
- chore: refactors, etc
- ci: ci-related work
- test: adding tests

Each PR should initially have at least 2 reviewers. At least one of these should be familiar with the product of the PR (Tracker, Platform, Analytics). The reviewers can be specific people, or a team. Exceptions can be made, depending on the content of the PR.

