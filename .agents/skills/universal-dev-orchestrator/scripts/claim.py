#!/usr/bin/env python3
"""File-ownership claims so parallel agents never edit the same files.

  claim.py claim <agent> <glob>...   # fails if overlapping with another agent's claim
  claim.py release <agent>
  claim.py list
Claims live in .agent/claims/<agent>.json (relative to the git root or CWD).
"""
import fnmatch, json, os, subprocess, sys, time


def root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    base = r.stdout.strip() if r.returncode == 0 else os.getcwd()
    # In a worktree, claims must be shared: use the main worktree's path.
    r2 = subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True)
    if r2.returncode == 0:
        common = os.path.abspath(r2.stdout.strip())
        if common.endswith(".git"):
            base = os.path.dirname(common)
    return base


D = os.path.join(root(), ".agent", "claims")


def load():
    out = {}
    if os.path.isdir(D):
        for f in os.listdir(D):
            if f.endswith(".json"):
                out[f[:-5]] = json.load(open(os.path.join(D, f)))["paths"]
    return out


def overlap(a, b):
    a0, b0 = a.rstrip("*/"), b.rstrip("*/")
    return (fnmatch.fnmatch(a, b) or fnmatch.fnmatch(b, a) or
            a0.startswith(b0) or b0.startswith(a0))


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    cmd = sys.argv[1]
    os.makedirs(D, exist_ok=True)
    if cmd == "list":
        for ag, ps in sorted(load().items()):
            print(f"{ag}: {', '.join(ps)}")
        return 0
    if cmd == "release" and len(sys.argv) == 3:
        p = os.path.join(D, sys.argv[2] + ".json")
        if os.path.exists(p): os.remove(p); print("released", sys.argv[2])
        return 0
    if cmd == "claim" and len(sys.argv) >= 4:
        agent, paths = sys.argv[2], sys.argv[3:]
        conflicts = [(o, a, b) for o, ps in load().items() if o != agent
                     for a in paths for b in ps if overlap(a, b)]
        if conflicts:
            for o, a, b in conflicts:
                print(f"CONFLICT: '{a}' overlaps '{b}' claimed by {o}")
            print("Do not edit these paths. Report to the orchestrator."); return 1
        with open(os.path.join(D, agent + ".json"), "w") as f:
            json.dump({"agent": agent, "paths": paths, "ts": time.time()}, f, indent=2)
        print(f"claimed for {agent}: {', '.join(paths)}"); return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main())
