# PR docs

This folder holds PR docs.
A PR doc is a full document about one large PR.
Examples: a new feature, a big refactor, a large performance test with many reports.
Write a PR doc only when the PR description cannot stay inside the word limit.

File name: `<PR number>_<type>_<short_title>.md`. Use underscores between the words.
The type is the prefix of the PR title, for example `fix`, `feat` or `perf`.

Example: `23200_fix_embedded_WAR_startup_crash_from_duplicate_slf4j_bindings.md`

For the rules, see [Large PRs: the PR doc](../pr-templates/general.md#large-prs-the-pr-doc).
