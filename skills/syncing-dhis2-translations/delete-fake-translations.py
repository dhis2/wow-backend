#!/usr/bin/env python3
"""Delete fake "English-as-translation" entries from DHIS2 i18n_global_*.properties files.

ONLY deletes lines where the target value is byte-identical to the English source.
Real translations are preserved untouched.

Run from the dhis2-core repo root (the directory containing dhis-2/).

Usage:
    # Delete specific keys (comma-separated)
    python3 delete-fake-translations.py --keys verify_email_subject,login_with_google

    # Delete keys matching a regex
    python3 delete-fake-translations.py --regex 'email_(verify|2fa)|login_with'

    # Dry-run: print what would be deleted, don't modify files
    python3 delete-fake-translations.py --keys verify_email_subject --dry-run

    # Restrict to certain languages
    python3 delete-fake-translations.py --keys ... --langs ru,es,pt

Workflow after running:
    1. git diff to verify only fake lines were removed
    2. git add + commit + push the deletion
    3. Push the cleanup to Transifex too:
         ~/.local/bin/tx push -t -f -l <affected,langs>
       Otherwise the next `tx pull` reintroduces the bad strings.
    4. Round-trip verify: tx pull one or two languages and diff against your committed state.
"""
import argparse
import glob
import os
import re
import sys

BASE_DIR = "dhis-2/dhis-services/dhis-service-core/src/main/resources"


def get_source_values(src_path, keys):
    """Return {key: raw_value} from source file for the given keys."""
    vals = {k: None for k in keys}
    with open(src_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            for k in keys:
                if vals[k] is None and line.startswith(f"{k}="):
                    vals[k] = line[len(k) + 1:]
                    break
    return vals


def list_source_keys_matching(src_path, regex):
    rx = re.compile(regex, re.IGNORECASE)
    out = []
    with open(src_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([^=]+?)\s*=", line)
            if m and rx.search(m.group(1).strip()):
                out.append(m.group(1).strip())
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--keys", help="Comma-separated keys to delete")
    group.add_argument("--regex", help="Regex on key name to match keys to delete (case-insensitive)")
    ap.add_argument("--langs", help="Comma-separated language codes (default: all)")
    ap.add_argument("--dry-run", action="store_true", help="Print what would be deleted without modifying files")
    ap.add_argument("--base", default=BASE_DIR, help=f"Base path to i18n files (default: {BASE_DIR})")
    args = ap.parse_args()

    src_path = f"{args.base}/i18n_global.properties"
    if not os.path.exists(src_path):
        print(f"Source file not found: {src_path}", file=sys.stderr)
        print("Run this from the dhis2-core repo root (the directory containing dhis-2/).", file=sys.stderr)
        sys.exit(1)

    if args.keys:
        keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    else:
        keys = list_source_keys_matching(src_path, args.regex)
        print(f"Regex matched {len(keys)} key(s) in source: {keys}\n")
        if not keys:
            sys.exit(0)

    src_vals = get_source_values(src_path, keys)
    missing = [k for k, v in src_vals.items() if v is None]
    if missing:
        print(f"WARNING: keys NOT in this branch's source file (will be skipped): {missing}\n")

    lang_filter = None
    if args.langs:
        wanted = set(l.strip() for l in args.langs.split(","))
        lang_filter = lambda l: l in wanted

    total_files = total_lines = 0
    detail = {}

    for path in sorted(glob.glob(f"{args.base}/i18n_global_*.properties")):
        lang = os.path.basename(path)[len("i18n_global_"): -len(".properties")]
        if lang_filter and not lang_filter(lang):
            continue
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        new_lines = []
        deleted = []
        for line in lines:
            stripped = line.rstrip("\n")
            kept = True
            for k in keys:
                if stripped.startswith(f"{k}="):
                    raw_val = stripped[len(k) + 1:]
                    # Only delete if target value byte-equals source
                    if src_vals[k] is not None and raw_val == src_vals[k]:
                        kept = False
                        deleted.append(k)
                    break
            if kept:
                new_lines.append(line)
        if deleted:
            if not args.dry_run:
                with open(path, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
            total_files += 1
            total_lines += len(deleted)
            detail[lang] = deleted

    mode = "[DRY-RUN] " if args.dry_run else ""
    print(f"{mode}Modified {total_files} files, deleted {total_lines} fake lines.\n")
    for lang, dels in sorted(detail.items(), key=lambda x: (-len(x[1]), x[0])):
        print(f"  {lang:<14} -{len(dels)}  {dels[:3]}{'…' if len(dels) > 3 else ''}")

    if not args.dry_run and total_lines:
        affected_langs = ",".join(sorted(detail.keys()))
        print(f"\nNext steps:")
        print(f"  1. git diff   # verify only fake lines were removed")
        print(f"  2. git add + commit --signoff + push")
        print(f"  3. Push to Transifex (CRITICAL — otherwise next tx pull reintroduces them):")
        print(f"     ~/.local/bin/tx push -t -f -l {affected_langs}")
        print(f"  4. Round-trip verify: tx pull -l ru -f --skip; git diff")


if __name__ == "__main__":
    main()
