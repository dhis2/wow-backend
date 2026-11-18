# PR description guide

Use this guide and the templates in this folder for each PR description.
The rules apply to humans and to AI agents.

## Why

PR descriptions are mainly for humans.
Two humans must review and approve each PR.
A reader must understand the PR from less than one page of text.
Thus the description must be small and compressed.

## Pick a template

The prefix of the PR title selects the template.
For the title rules, see [Git PR & commit messages](../guides/git_commit_messages.md).

| Prefix | Template | Use for |
|---|---|---|
| `fix:` | [fix.md](fix.md) | Bug fix |
| `feat:` | [feat.md](feat.md) | New feature or new behaviour |
| `perf:` | [perf.md](perf.md) | Faster or less memory, same behaviour |
| `refactor:` | [refactor.md](refactor.md) | New code structure, same behaviour |
| `chore:` | [chore.md](chore.md) | Clean-up and maintenance |
| `ci:` | [ci.md](ci.md) | CI workflows and pipelines |
| `test:` | [test.md](test.md) | Test code only |
| `docs:` | [docs.md](docs.md) | Documentation only |

Build changes (Maven, dependencies, packaging) use the `chore` type.

## Format

- Do not add other sections.
- Section headings are h3 (`###`), for example `### What`.
- Do not add a section with the name Test, Tests or Testing.
  In a fix, the Proof section can name the test that proves the fix, in one sentence.
- Use a bullet list when a section has several separate points.
  Examples: the components or steps in How, the items in Caveats, a list of changed items.
  Use sentences for one thought or a short narrative, typically in What and Why.
  Do not make a list from one or two sentences.
- Remove the hint text and the optional parts that you do not use.
- If AI wrote a large part of the PR, put "AI Assisted" on the last line.

## Size

- Maximum 250 words, headings included. Count with `wc -w`.
- Aim for 150 words or fewer.
- If the PR is very large, you can write a [PR doc](#large-prs-the-pr-doc).

## Content

- Tell what changes and why. Keep the how short. The code shows it.
- Keep it simple. Do not list each small detail.
- Name 1-3 key classes, methods or endpoints as the entry points to the code.
- Caveats is an optional section. Most PRs do not need it.
  Use it only if the template has it and a reviewer must know about a behaviour change, risk or limit.
- Put the Jira key in the title. Put related PRs in the link line.
- Link the Jira issue with its full URL, as the templates show. Most PRs have a Jira issue.

## Language

Write in [ASD-STE100](https://www.asd-ste100.org/) Simplified Technical English (STE):

- One sentence, one statement. Maximum 20 words in a sentence.
- Use the active voice. Write "The import rejects the row", not "The row is rejected".
- Use one word for one meaning. Use the same term for the same item in all of the text.
- Use common words. Do not use filler, for example "basically", "simply", "in order to".

Keep the load on the reader low:

- Put the subject, the verb and the object near each other.
- Do not put a clause inside a different clause. Write two sentences.
- Put a modifier immediately next to the word that it modifies.
- Start with the main statement. Keep introductions short.

## Large PRs: the PR doc

Some PRs need more text than the word limit allows.
Examples: a new feature, a big refactor, a large performance test with many reports.
For such a PR, you can write a PR doc.
A PR doc is a full document about the PR.
It has no word limit and no fixed sections.
It can contain reports, tables and diagrams.

- Put the PR doc in the [`pr/`](../pr/README.md) folder of dhis2/wow-backend.
- File name: `<PR number>_<type>_<short_title>.md`. Use underscores between the words.
  The type is the prefix of the PR title, for example `fix`, `feat` or `perf`.
  Example: `23200_feat_API_ETag_cache.md`. The PR number comes first, so the files sort in PR order.
- Open the code PR first. Then open the doc PR in dhis2/wow-backend, with the code PR number in the file name.
- Then put a link to the PR doc in the link line of the code PR description.
  Until the doc PR merges, the link points to the doc on its branch.
- The PR description still follows the template of its type and the word limit.
- The PR doc stays in `pr/` permanently, as the record of the PR.
  Do not update it after the code PR merges.
- The PR doc is optional, never required.

## Examples

Each template has examples. Most are short rewrites of real dhis2-core PRs.
