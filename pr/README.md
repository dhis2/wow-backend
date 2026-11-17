# PR docs

This folder holds PR docs.
A PR doc is a full document about one very large PR.
Examples: a new feature, a big refactor, a large performance test with many reports.
If a PR is very large, you can write a PR doc. A PR doc is optional, never required.

File name: `<PR number>_<type>_<short_title>.md`. Use underscores between the words.
The type is the prefix of the PR title, for example `fix`, `feat` or `perf`.

Example: `23200_feat_API_ETag_cache.md`

A PR doc stays here permanently, as the record of the PR.
Do not update it after the code PR merges.

For the rules, see [Large PRs: the PR doc](../pr-templates/general.md#large-prs-the-pr-doc).
