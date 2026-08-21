---
name: syncing-dhis2-translations
description: Use when fixing DHIS2 core translations — English text showing in non-English UI, fake "English-as-translation" entries in i18n_global_*.properties, blocked dhis2-bot translation-sync PRs, coordinating cleanup across master + supported branches, or pushing translations to the hisp-uio Transifex project via tx CLI. Covers the dhis2/transifex-ci pipeline.
---

# Syncing DHIS2 Translations

## What this is

DHIS2 uses **Transifex** for translations (project `o:hisp-uio:p:app-server-side-resources`). The sync between Transifex and `dhis2/dhis2-core` is automated by `dhis2/transifex-ci`. This skill covers the four common tasks: detecting and cleaning fake "English-as-translation" entries, pushing fixes back to Transifex, unblocking the auto-sync PRs, and backporting cleanup to supported release branches.

## The official pipeline (from Phil, the translation owner)

```
1. Change source string → PR to dhis2-core → merge
2. Nightly dhis2/transifex-ci cron pushes new source strings to Transifex
3. Translators (humans, or AI via `tx push -t` CLI) provide translations in Transifex
4. Next nightly cron pulls translations and opens/updates a sync PR per branch in dhis2-core
5. Merge the sync PR when ready
```

Repo: https://github.com/dhis2/transifex-ci · Daily cron 23:11 UTC · Weekly Saturdays 22:41 UTC · Both support `workflow_dispatch` for manual triggering from the Actions UI.

## The "fake translation" pattern

The recurring bug: an entry in `i18n_global_<lang>.properties` has the same value as the English source. Examples:

```
# i18n_global_ru.properties
verify_email_subject=Verify email address        # ← English, not Russian
F_IMPERSONATE_USER=Impersonate user              # ← English
```

This happens when someone (or some sync) wrote the English source as a "translation". Transifex marks it translated, so it doesn't appear in translator queues, but users see English in the non-English UI.

**Detection:** byte-equal comparison between target value and English source. Run `audit-fake-translations.py` (this skill dir) to list them per language.

**False positives to skip:**
- Brand names that don't translate: `openid=OpenID`
- Common short words that legitimately match: `two_factor_code=Code` (in `fr`/`nl`/`da` "Code" is the real translation; in non-Latin-script langs it's English left as-is — needs human judgment)

## The cleanup workflow

For one or more keys / a domain (e.g. all security-related strings):

1. **Audit per language** — run `audit-fake-translations.py --keys <key1,key2,…>` (or with a regex) to confirm scope.
2. **Delete fakes in repo** — run `delete-fake-translations.py` with the same keys. Script ONLY deletes lines where target value byte-equals English source. Real translations preserved. Never use a blind `sed -i` that doesn't check the value.
3. **Push to Transifex** — `~/.local/bin/tx push -t -f -l <comma,sep,langs>` from the dhis2-core repo. This retires the bad translations in Transifex's database. **Round-trip verify** by re-pulling one or two languages and diffing.
4. **(Optional) Add AI placeholders** — for major/widely-spoken languages, generate AI-translated placeholders to avoid English-in-UI while translators catch up. Mark them in-file with a `#-- AI-assisted, pending translator review --#` comment. Push the same way.
5. **Commit and PR to core** — open PR against `master`. Deletions only — Transifex push is separate.
6. **Backport** — re-run the deletion script on each supported branch (`2.43`, `2.42`, `2.41`, `2.40`). The script handles per-branch source differences automatically (skips keys not in that branch's source).

## Watch out for

- **`.tx/config` has a non-existent resource ID** (`r:i18n-global-properties` without branch prefix). The CLI tolerates it via branch heuristics, but the REST API returns 404 for that exact ID. Real resources are `r:master--i18n-global-properties`, `r:2-43--i18n-global-properties`, etc.
- **One push covers all branches** — Transifex resources are version-tagged (`master--`, `2-43--` etc.) but the project is shared. After the master-branch push, the same translations are available for ALL branch sync runs.
- **Stale bot PRs reintroduce fakes** — if a bot sync PR's head is older than your `tx push`, merging it brings the old (bad) translations back. Always check the bot PR's `updatedAt` vs your push date.

## The bot-PR signing problem

The `dhis2-bot` opens sync PRs but the commits are **unsigned + missing DCO Signed-off-by**. They sit at `MERGEABLE/BLOCKED`. Two approaches:

- **Permanent fix:** PR https://github.com/dhis2/transifex-ci/pull/12 adds `--signoff` + SSH signing to `transyncosaurus_ALL.sh`. Once merged + admin sets the `DHIS2_BOT_SSH_SIGNING_KEY` secret, future bot PRs are mergeable.
- **Per-PR workaround** (until the permanent fix lands):
  ```bash
  PR=23981; BASE=master; HEAD_BRANCH=master-transifex-ALL-<timestamp>
  git fetch origin $BASE $HEAD_BRANCH
  git worktree add /tmp/tx-amend origin/$HEAD_BRANCH
  cd /tmp/tx-amend
  git checkout -B local-amend-$PR
  git rebase --signoff origin/$BASE     # adds Signed-off-by + GPG-signs if gpg-agent unlocked
  git push --force-with-lease origin local-amend-$PR:$HEAD_BRANCH
  cd - && git worktree remove /tmp/tx-amend --force
  ```
  Needs gpg-agent unlocked. Warm with `git commit --allow-empty -S -m "warm gpg-agent"` in your interactive shell.

## tx CLI setup (one-time)

```bash
# Install
curl -fsSL https://api.github.com/repos/transifex/cli/releases/latest | grep tx-linux-amd64.tar.gz | grep browser_download_url | cut -d'"' -f4 | xargs curl -fsSL -o /tmp/tx.tar.gz
cd /tmp && tar -xzf tx.tar.gz && mv tx ~/.local/bin/tx && chmod +x ~/.local/bin/tx

# Credentials — generate token at https://app.transifex.com/user/settings/api/
# Then write ~/.transifexrc IN YOUR TERMINAL, never paste tokens in chat:
umask 077 && cat > ~/.transifexrc <<EOF
[https://www.transifex.com]
rest_hostname = https://rest.api.transifex.com
token = PASTE_TOKEN_HERE
EOF
chmod 600 ~/.transifexrc
```

## Common mistakes

| Mistake | What goes wrong |
|---|---|
| Delete in repo, forget `tx push -t` | Next `tx pull` reintroduces the bad strings |
| Blind `sed -i` to remove keys | Removes real translations too — always compare to source value first |
| Push translations as English (looks like a translator did it) | Creates more fake translations — the original bug |
| Merge a stale bot PR after your push | Reverts your work to the bot's older snapshot |
| Auto-translate low-resource languages with AI | Quality is unreliable for `ckb`/`km`/`my`/`or`/`prs`/`ps`/`si`/`tet`/`tg` — skip them, let native speakers handle |
| Commit to dhis2-core PR but skip Transifex push | Only fixes one branch's repo, not the source of truth |
| Run `tx push -s` (source) to "fix" translations | Source push is the bot's job; doing it manually is redundant and risks pushing partially-staged source. **Only push `-t` (translations) for cleanup.** |
| Use `--dry-run` on `tx push` | The modern tx CLI's `--dry-run` flag does not work reliably on `push`. Verify by re-pulling one language after push and diffing — that's the canonical sanity check. |
| Try to "mark strings as unreviewed in Transifex UI" | There is no clean per-string "unreviewed" toggle. The actual retirement workflow is: delete from `.properties` file, `tx push -t -f`, post a Transifex Announcement asking translators to retranslate. |
| Cherry-pick from an open (unmerged) backport PR's head SHA | Will conflict when those PRs eventually merge. Cherry-pick only from `master` commits that have actually landed. If a backport PR is already open, ADD to it instead. |
| Notify translators via guessed Slack channels | Use the **Transifex Announcements** feature on the project (Settings → Announcements). It's the official channel — translators get notified in-app and via email. Phil owns the Transifex project; ping him if you don't have Maintainer rights. |
| Declare ticket done at PR-merge time | The bot's next nightly sync will open a follow-up PR pulling translator updates. That PR **may be blocked by missing signatures** (see "bot-PR signing problem" above). Confirm the resync PR merges before closing the JIRA. |

## Stakeholders

- **Phil** — translation/Transifex owner. Ping him for: Maintainer-level Transifex tasks, posting announcements to translators, transifex-ci CI changes, bot account access.
- **QA reporters** (e.g. Lina for Russian) — file the JIRA ticket and verify the fix.
- **Repo write access on dhis2-core** — assumed; backport PRs push branches directly to origin.

## Reference docs in dhis2-core repo

When working in dhis2-core, look at:
- `dhis-2/TRANSLATIONS_SECURITY_ANALYSIS.md` — example deep-dive for one cleanup (DHIS2-19912)
- `dhis-2/TRANSLATIONS_ACTION_PLAN.md` — step-by-step playbook
- `dhis-2/TRANSLATION_TODO.md` — current handoff state (if mid-flight)

## Tools in this skill dir

- `audit-fake-translations.py` — list fake translations per language, with key/regex filtering
- `delete-fake-translations.py` — remove fakes from translation files (only deletes lines where value byte-equals English source)
