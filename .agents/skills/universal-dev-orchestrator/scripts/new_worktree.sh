#!/usr/bin/env bash
# Create an isolated git worktree + branch for one agent.
# Usage: scripts/new_worktree.sh <agent-name> [base-branch]   (default base: current branch)
set -euo pipefail
agent="${1:?usage: new_worktree.sh <agent-name> [base-branch]}"
base="${2:-$(git rev-parse --abbrev-ref HEAD)}"
top="$(git rev-parse --show-toplevel)"
path="$(dirname "$top")/wt-$agent"
branch="agent/$agent"
[ -e "$path" ] && { echo "worktree path exists: $path" >&2; exit 1; }
git worktree add -b "$branch" "$path" "$base"
mkdir -p "$top/.agent"/{briefs,claims,handoffs,reports}
echo
echo "worktree: $path"
echo "branch:   $branch (from $base)"
echo "next:     cd $path && start a Codex session here with the role + brief prompt"
echo "cleanup:  git worktree remove $path && git branch -d $branch"
