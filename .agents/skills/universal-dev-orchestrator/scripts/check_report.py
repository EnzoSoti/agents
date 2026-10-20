#!/usr/bin/env python3
"""Reject change reports that claim success without evidence.
Usage: check_report.py .agent/reports/T-001.md [more.md ...]
Exit 0 = OK, 1 = problems found.
"""
import re, sys

REQUIRED = ["summary", "files changed", "verification", "not verified", "rollback"]
WEAK = re.compile(r"\b(should work|probably|i believe|looks correct|seems fine|i think it works)\b", re.I)


def check(path):
    t = open(path, encoding="utf-8").read()
    low = t.lower()
    errs = []
    m = re.search(r"^RESULT:\s*(.+)$", t, re.M | re.I)
    raw = m.group(1).strip().lower() if m else ""
    result = raw if raw in {"done", "partial", "blocked"} else None
    if result is None:
        errs.append("RESULT line missing or not chosen (must be exactly done, partial, or blocked)")
    if "pass/fail" in low or "<" in t and ">" in t and "t-xxx" in low:
        errs.append("template placeholders not filled in")
    for h in REQUIRED:
        if h not in low:
            errs.append(f"missing section: {h}")
    ver = re.search(r"verification.*?(?=\n## |\Z)", t, re.I | re.S)
    rows = [r for r in (ver.group(0).splitlines() if ver else []) if r.strip().startswith("|")]
    data = [r for r in rows if not re.match(r"^\|\s*(command|-+)", r.strip(), re.I) and not set(r.strip()) <= set("|-: ")]
    filled = [r for r in data if len([c for c in r.strip().strip("|").split("|") if c.strip()]) >= 2]
    if result == "done":
        if not filled:
            errs.append("RESULT is done but Verification table has no command/outcome rows")
        if any(re.search(r"\bfail", r, re.I) for r in filled):
            errs.append("RESULT is done but a verification row shows FAIL (report baseline separately or use partial)")
    if WEAK.search(t):
        errs.append("weak/unverified wording found: " + ", ".join(sorted({w.lower() for w in WEAK.findall(t)})))
    return errs


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    bad = 0
    for p in sys.argv[1:]:
        errs = check(p)
        print(("FAIL " if errs else "OK   ") + p)
        for e in errs: print("   - " + e)
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
