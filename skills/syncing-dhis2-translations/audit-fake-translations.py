#!/usr/bin/env python3
"""Audit fake "English-as-translation" entries in DHIS2 i18n_global_*.properties files.

A "fake translation" is a key whose target-language value is byte-identical to the
English source value. Examples:
    # i18n_global_ru.properties
    verify_email_subject=Verify email address     # ← English, should be Cyrillic

Run from the dhis2-core repo root (the directory containing dhis-2/).

Usage:
    # All fakes per language
    python3 audit-fake-translations.py

    # Filter by specific keys (comma-separated)
    python3 audit-fake-translations.py --keys verify_email_subject,login_with_google

    # Filter by regex on key name
    python3 audit-fake-translations.py --regex 'email_(verify|2fa)|login_with'

    # Only certain languages
    python3 audit-fake-translations.py --langs ru,es,pt

    # Limit output to N fake examples per language
    python3 audit-fake-translations.py --limit 5
"""
import argparse
import glob
import os
import re
import sys

BASE_DIR = "dhis-2/dhis-services/dhis-service-core/src/main/resources"

# Keys whose source value is a brand/common word that may match across languages —
# the audit cannot tell whether these are fakes or legitimate.
FALSE_POSITIVES = {"openid"}


def parse_props(path):
    """Parse a .properties file into a dict of key -> raw value (escapes preserved)."""
    out = {}
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#") or line.startswith("!"):
                continue
            m = re.match(r"^([^=]+?)\s*=\s*(.*)$", line)
            if m:
                out[m.group(1).strip()] = m.group(2)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keys", help="Comma-separated list of keys to check")
    ap.add_argument("--regex", help="Regex on key name to filter (case-insensitive)")
    ap.add_argument("--langs", help="Comma-separated language codes to check (default: all)")
    ap.add_argument("--limit", type=int, default=0, help="Max fakes to print per language (0 = no limit)")
    ap.add_argument("--base", default=BASE_DIR, help=f"Base path to i18n files (default: {BASE_DIR})")
    args = ap.parse_args()

    src_path = f"{args.base}/i18n_global.properties"
    if not os.path.exists(src_path):
        print(f"Source file not found: {src_path}", file=sys.stderr)
        print("Run this from the dhis2-core repo root (the directory containing dhis-2/).", file=sys.stderr)
        sys.exit(1)

    src = parse_props(src_path)

    key_filter = None
    if args.keys:
        wanted = set(k.strip() for k in args.keys.split(","))
        key_filter = lambda k: k in wanted
    elif args.regex:
        rx = re.compile(args.regex, re.IGNORECASE)
        key_filter = lambda k: bool(rx.search(k))

    lang_filter = None
    if args.langs:
        wanted_langs = set(l.strip() for l in args.langs.split(","))
        lang_filter = lambda l: l in wanted_langs

    files = sorted(glob.glob(f"{args.base}/i18n_global_*.properties"))
    total = 0
    langs_affected = 0
    print(f"{'Lang':<14} {'Fake':>5}  Examples")
    print("-" * 60)
    for path in files:
        lang = os.path.basename(path)[len("i18n_global_"): -len(".properties")]
        if lang_filter and not lang_filter(lang):
            continue
        tr = parse_props(path)
        fakes = []
        for k, v in tr.items():
            if k in FALSE_POSITIVES:
                continue
            if k not in src:
                continue
            if src[k] != v:
                continue
            if not v.strip():
                continue
            if key_filter and not key_filter(k):
                continue
            fakes.append(k)
        if fakes:
            total += len(fakes)
            langs_affected += 1
            sample = fakes[: args.limit] if args.limit else fakes[:3]
            extra = "" if (args.limit and len(fakes) <= args.limit) or len(fakes) <= 3 else " …"
            print(f"{lang:<14} {len(fakes):>5}  {sample}{extra}")

    print(f"\nTotal fake translations: {total}")
    print(f"Languages affected: {langs_affected}")


if __name__ == "__main__":
    main()
