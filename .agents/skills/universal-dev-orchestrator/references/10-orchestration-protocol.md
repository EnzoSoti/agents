# Multi-Agent Orchestration Protocol

Designed for running several Codex agents at the same time on one repository, safely and with predictable merges.

## Contents
1. Topology and roles
2. Workspace isolation (worktrees)
3. Task decomposition and file ownership
4. The `.agent/` coordination directory
5. Lifecycle and handoffs
6. Merge and integration
7. Gates by risk level
8. Failure handling
9. Prompting patterns / launch recipes
10. Anti-patterns

## 1. Topology and roles
Role prompts are in `roles/`. A typical run:

```
              +----------------+
              |  ORCHESTRATOR  |  plans, assigns, merges, decides
              +--------+-------+
      +-----------+----+-----+------------+
      v           v          v            v
  PLANNER   FRONTEND-ENG   BACKEND-ENG   SQL/DB    SECURITY
  (spec)    (React)        (.NET API)    SPECIALIST AUDITOR
            IMPLEMENTER(s) = any extra parallel workers, 1 per module
                  v
              REVIEWER -> QA TESTER -> DEPLOY ENGINEER
```
Scale down for small tasks: orchestrator + 1 implementer + reviewer is often enough. Do not spawn agents you do not need.

## 2. Workspace isolation (worktrees)
Each writing agent gets its own **git worktree and branch** so agents never overwrite each other's working files:

```bash
scripts/new_worktree.sh impl-auth main      # -> ../wt-impl-auth on branch agent/impl-auth
scripts/new_worktree.sh impl-billing main
scripts/new_worktree.sh sql-migrations main
```
Start one Codex session per worktree directory (separate terminals/tabs/processes). Read-only roles (planner, reviewer, auditor) can use the main checkout or a throwaway worktree.
Cleanup: `git worktree remove ../wt-impl-auth && git branch -d agent/impl-auth` after merge.

## 3. Decomposition and file ownership
- Split by **module/directory/layer**, never two agents in the same file.
- Every task gets: ID, goal, acceptance criteria, **allowed paths**, **forbidden paths**, dependencies, risk level, required checks (use `templates/task-brief.md`).
- **Single-owner files**: lockfiles, DB schema/migrations index, route registries, global config, generated code, CI workflows. Assign to one agent; others request changes via handoff.
- Define **contracts first** (API shapes, function signatures, DB schema, event formats) and commit them before parallel implementation starts. Workers code against the contract.
- Dependency order: contracts -> (parallel) implementations -> integration -> QA -> deploy.

### React + .NET split (recommended default)
1. **Contract first**: orchestrator (or backend-engineer) commits the OpenAPI spec / DTO definitions for new or changed endpoints. Frontend generates a typed client from it.
2. **Parallel**: backend-engineer owns `backend/**` (+ migrations via sql-specialist); frontend-engineer owns `frontend/**`. Neither edits the other's folder.
3. **Contract change mid-flight**: stop both, update the contract, re-brief.
4. **Integration**: run backend + frontend together on `integration/<run-id>`; QA runs end-to-end against the real API.
5. Single-owner files: OpenAPI spec (backend), generated API client (frontend, regenerated from spec), `*.sln`/`package.json` lockfiles (one owner each), DB migrations (sql-specialist).
Example scope flags: frontend `--allow "frontend/src/**"`; backend `--allow "backend/**"`.

## 4. The `.agent/` coordination directory
Keep at repo root; add `.agent/` to `.gitignore` for per-run state, or commit `.agent/briefs` if you want audit history.

```
.agent/
  briefs/      T-001.md ...      task briefs from the orchestrator
  claims/      <agent>.json      files each agent has claimed (see scripts/claim.py)
  handoffs/    T-001-to-qa.md    structured handoffs between roles
  reports/     T-001.md          final change reports
  status.md                      orchestrator's live board
```
Helpers:
- `python scripts/claim.py claim <agent> <path-or-glob>...` - fails if another agent holds an overlapping claim
- `python scripts/claim.py list` / `release <agent>`
- `python scripts/scope_check.py --allow "src/auth/**" --allow "tests/auth/**"` - fails if your diff leaves your scope

## 5. Lifecycle and handoffs
1. Orchestrator writes briefs, creates worktrees, records claims, updates `status.md`.
2. Worker: read brief -> preflight -> plan (post to brief if deviating) -> implement -> `verify.sh` -> `scope_check.py` -> commit on its branch -> write report + handoff.
3. Reviewer: reads brief + diff + report; returns findings (BLOCKER/MAJOR/MINOR). Worker fixes; reviewer re-checks.
4. QA: runs test plan on the integrated branch; returns verdict.
5. Deploy engineer: executes release checklist only after required approvals.
Handoff content (see `templates/handoff.md`): what was done, where, how to verify, open issues, assumptions, next role's explicit ask. A handoff must be self-contained; the receiver should not need the sender's chat history.

## 6. Merge and integration
- Merge order: contracts/migrations -> core implementations -> consumers -> tests/docs -> deploy config.
- Integrate on an `integration/<run-id>` branch; run the full suite there, not just per-branch.
- Resolve conflicts by intent: the owner of the file wins; the other agent re-applies on top. Re-run verification after every merge.
- Rebase/merge only branches whose reports say VERIFIED. Squash or keep history per repo convention.

## 7. Gates by risk level
| Risk | Required before merge | Required before deploy |
|---|---|---|
| Low | verify.sh pass, scope check | CI green |
| Medium | + reviewer approval, full suite | + QA PASS |
| High | + second independent reviewer, security/DB specialist review, rollback plan | + human approval, staged/canary rollout |

## 8. Failure handling
- **Worker blocked**: write `BLOCKED` report with evidence and the exact question; stop editing. Orchestrator unblocks or reassigns.
- **Claim collision**: later claimant stops; orchestrator re-slices or serializes.
- **Contract change needed mid-flight**: pause dependents, update contract, re-brief them.
- **Verification fails at integration**: bisect per-branch merges; owner of the offending change fixes.
- **Agent drifting out of scope**: `scope_check.py` fails -> revert out-of-scope edits, report them as follow-ups.
- Timebox each task; unfinished work is reported as `partial` with exact state.

## 9. Prompting patterns / launch recipes
Give each Codex session a short, explicit prompt that points to the skill, role, and brief:

```
Use the universal-dev-orchestrator skill. Role: IMPLEMENTER (roles/implementer.md).
Task brief: .agent/briefs/T-002.md. Work only in this worktree and only in the allowed paths.
Run scripts/verify.sh and scripts/scope_check.py before finishing, then write .agent/reports/T-002.md.
```
Orchestrator prompt:
```
Use the universal-dev-orchestrator skill. Role: ORCHESTRATOR (roles/orchestrator.md).
Goal: <feature>. Decompose into briefs in .agent/briefs/, define contracts first, assign file ownership,
create worktrees, and maintain .agent/status.md. Do not implement; coordinate.
```
Reviewer prompt:
```
Use the universal-dev-orchestrator skill. Role: REVIEWER (roles/reviewer.md).
Review branch agent/impl-auth against .agent/briefs/T-002.md. Read-only. Output findings by severity and a verdict.
```
Tips: keep prompts short; put detail in briefs. Pin model/reasoning effort per role if your setup allows (higher for orchestrator/reviewer/security, lower for mechanical tasks).

### Parallel dispatch and subagent loop (patterns from top community skills)
- **Dispatch in parallel only when problems are independent**: different modules/failures, no shared state, no shared files. One agent per domain; give each a focused brief and a clear stop condition.
- **Per-task loop**: fresh implementer -> stage-1 spec review -> fix -> stage-2 quality review -> fix -> orchestrator re-verifies independently. Do not mark a task done on the implementer's say-so.
- **After parallel returns**: read every report, check for conflicts and overlapping edits, merge on the integration branch, run the full suite and E2E.
- Context packs and handoffs: `playbooks/07-context-engineering.md`. Pipeline gates: `playbooks/00-end-to-end-pipeline.md`.

## 10. Anti-patterns
Two agents editing the same file; no contract before parallel work; agents "helpfully" fixing out-of-scope issues; approvals based on summaries instead of diffs/tests; skipping integration testing because each branch passed alone; chat-only coordination with nothing written to `.agent/`; spawning more agents than independent work exists.
