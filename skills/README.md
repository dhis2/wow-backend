# Skills

[Claude Code skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that capture DHIS2 backend workflows. A skill is a small directory containing a `SKILL.md` (with YAML frontmatter describing when to invoke it) and any supporting scripts or reference files. When a developer is working with Claude Code in any DHIS2 repo, an installed skill is auto-discovered and invoked when the description matches their task.

This directory exists so that team-wide workflows can live in one place and benefit everyone, rather than each developer reinventing them.

## Available skills

| Skill | When it applies |
|---|---|
| [`syncing-dhis2-translations`](./syncing-dhis2-translations/) | Fixing fake "English-as-translation" entries in `i18n_global_*.properties`, pushing translation cleanup to Transifex via `tx`, handling stuck `dhis2-bot` sync PRs, and coordinating cleanup across master + supported branches |

## Installing a skill locally

Pick one approach:

### Option A — symlink (recommended; gets updates via `git pull`)

```bash
# Assumes wow-backend is cloned at ~/src/dhis2/wow-backend (adjust as needed)
mkdir -p ~/.claude/skills
ln -s ~/src/dhis2/wow-backend/skills/syncing-dhis2-translations \
      ~/.claude/skills/syncing-dhis2-translations
```

Run `ls -la ~/.claude/skills/` to confirm. Next time you start Claude Code, the skill description appears in the available-skills list and Claude will invoke it when your task matches the description.

### Option B — copy (frozen at copy time)

```bash
cp -r ~/src/dhis2/wow-backend/skills/syncing-dhis2-translations \
      ~/.claude/skills/
```

### Verifying installation

Inside Claude Code, ask something like *"do we have a skill for fixing DHIS2 translations?"* — Claude should reference `syncing-dhis2-translations` from the available list.

## Contributing a new skill

1. Branch off `master`: `git checkout -b feat/skill-<name>`
2. Create `skills/<your-skill-name>/SKILL.md` with the YAML frontmatter:
   ```yaml
   ---
   name: <gerund-form-name>
   description: Use when <specific triggering conditions and symptoms>
   ---
   ```
3. Keep `SKILL.md` under ~500 lines. Use [Anthropic's skill-authoring guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices) for structure.
4. Put reusable scripts as separate files in the same directory (not inlined in `SKILL.md`).
5. Update the table above and open a PR.

### Naming conventions

- Use **gerund form** (verb + -ing): `syncing-dhis2-translations`, `migrating-postgres-schemas`, `debugging-tracker-imports`
- Hyphenated, lowercase, no spaces
- Specific enough that the description triggers cleanly without overlapping other skills

### Description field

The `description` is the single most important line for skill discovery. Start with **"Use when ..."** and list concrete triggers, not the workflow:

```yaml
# ✅ Good
description: Use when investigating Flyway migration conflicts during a backport — out-of-order versions across release branches, coordination doc out of sync, failed startup with "Detected resolved migration not applied to database".

# ❌ Bad — describes the workflow instead of the trigger
description: Walks through three steps to resolve Flyway conflicts.
```

See the [Claude Code skill best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices) for more detail.
