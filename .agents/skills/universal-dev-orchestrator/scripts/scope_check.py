#!/usr/bin/env python3
"""Fail if changed files fall outside allowed paths.

Usage:
  scope_check.py --allow "src/auth/**" --allow "tests/auth/**" [--base main] [--forbid "package-lock.json"]
Checks committed diff vs base (merge-base) plus staged, unstaged, and untracked files.
"""
import argparse, fnmatch, subprocess, sys


def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    return r.stdout.strip().splitlines() if r.returncode == 0 else []


def matches(path, pats):
    for p in pats:
        if fnmatch.fnmatch(path, p) or fnmatch.fnmatch(path, p.rstrip("/") + "/*"):
            return True
        if p.endswith("/**") and (path.startswith(p[:-3]) or path == p[:-3].rstrip("/")):
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow", action="append", default=[], help="glob(s) of editable paths")
    ap.add_argument("--forbid", action="append", default=[], help="glob(s) that must not change")
    ap.add_argument("--base", default=None, help="base branch/commit (default: working tree vs HEAD only)")
    a = ap.parse_args()
    if not a.allow:
        print("ERROR: provide at least one --allow", file=sys.stderr); return 2

    files = set()
    if a.base:
        mb = sh("git", "merge-base", a.base, "HEAD")
        if mb:
            files |= set(sh("git", "diff", "--name-only", mb[0], "HEAD"))
    files |= set(sh("git", "diff", "--name-only", "HEAD"))
    files |= set(sh("git", "diff", "--name-only", "--cached"))
    files |= set(sh("git", "ls-files", "--others", "--exclude-standard"))
    files = {f for f in files if not f.startswith(".agent/")}

    bad = sorted(f for f in files if matches(f, a.forbid) or not matches(f, a.allow))
    print(f"changed files: {len(files)}")
    for f in sorted(files):
        print(("  OUT " if f in bad else "  ok  ") + f)
    if bad:
        print(f"\nSCOPE VIOLATION: {len(bad)} file(s) outside allowed paths. Revert them or report as follow-ups.")
        return 1
    print("\nSCOPE OK"); return 0


if __name__ == "__main__":
    sys.exit(main())
