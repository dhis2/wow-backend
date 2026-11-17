# PR description guide

Use this guide and the templates in this folder for each PR description.
The rules apply to humans and to AI agents.

## Why

PR descriptions are mainly for humans.
Two persons must review and approve each PR.
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

- All templates have the same sections in the same order:
  optional link line, **Problem**, **Solution**, optional **Changes/Caveats** list, AI line.
- Do not add other sections.
- A PR description has no test section and no test line.
  The tests are in the diff and in CI.
- AI line: one line. Tell which parts AI made.
- Remove the hint text and the optional parts that you do not use.

## Size

- Maximum 250 words, headings included. Count with `wc -w`.
- Aim for 150 words or fewer.
- Problem and Solution: maximum 2 short paragraphs each.
- Changes/Caveats: maximum 5 bullets, one line each.
- If you need more words, split the PR.
  If you cannot split it, write a [PR doc](#large-prs-the-pr-doc).

## Large PRs: the PR doc

Some PRs need more text than the word limit allows.
Examples: a new feature, a big refactor, a large performance test with many reports.
For such a PR, you can write a PR doc.
A PR doc is a full document about the feature or the PR.
It has no word limit and no fixed sections.
It can contain reports, tables and diagrams.

- Put the PR doc in the [`pr/`](../pr/README.md) folder of dhis2/wow-backend.
- File name: `<PR number>_<type>_<short_title>.md`. Use underscores between the words.
  The type is the prefix of the PR title, for example `fix`, `feat` or `perf`.
  Example: `23200_fix_embedded_WAR_startup_crash_from_duplicate_slf4j_bindings.md`.
- Open the PR first. Then you know the PR number for the file name.
- The PR description still follows the template of its type and the word limit.
- Put a link to the PR doc in the link line of the PR description.
- The PR doc is optional, never required.

## Content

- Tell what changes and why. Do not tell how, file by file. The code shows that.
- Keep it simple and generic. Do not list each small detail.
- Name one key class, method or endpoint as the entry point to the code.
- Use Caveats for items that a reviewer can miss: behaviour changes, risks, limits.
- Put the Jira key in the title. Put related PRs in the link line.

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

## Examples

Each template has examples. They are short rewrites of real dhis2-core PRs.
Their AI lines show the form, not the facts.
