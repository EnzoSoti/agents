# Ship: finishing a branch and pre-launch

## Finishing a development branch
1. Re-run full verification on the final commit.
2. Rebase/merge main; resolve conflicts by intent; re-verify.
3. Clean history per repo convention (small logical commits, clear messages).
4. Choose one: **open PR** (default), merge locally (only if allowed), keep the branch, or discard (explicit confirmation).
5. Remove the worktree and branch after merge: `git worktree remove ../wt-<agent> && git branch -d agent/<agent>`.

## Git workflow
Short-lived branches, small PRs, trunk-based when the team does it, feature flags for incomplete work, no direct pushes to main, protected branches with required checks.

## Pre-launch checklist
**Functionality**: acceptance criteria demonstrated; E2E smoke green; error and empty states checked; browser/device matrix agreed.
**Quality**: reviews done; no open BLOCKER/MAJOR; tech-debt items ticketed.
**Security**: dependency audit clean or accepted; secrets managed; authZ tests pass; CORS/headers reviewed; PII handling checked.
**Performance**: API p95 and error-rate targets met under realistic load; DB plans reviewed; frontend bundle size and key web vitals acceptable.
**Accessibility**: keyboard flow and labels verified.
**Data**: migrations backward compatible, backups verified, rollback plan tested.
**Infra**: config and secrets present in the target; health checks; resource limits.
**Observability**: logs, metrics, alerts, dashboards for the new paths; on-call aware.
**Docs/comms**: changelog, runbook, user-facing notes.
**Rollout**: strategy chosen (rolling/canary/blue-green/flag); rollback trigger thresholds written down.

## After launch
Watch error rate, latency, saturation, and business metrics for the agreed window; be ready to roll back; run a short retrospective and capture lessons in the skill/AGENTS.md.

Deeper deployment procedure: `references/08-ci-cd-and-deployment.md`.
