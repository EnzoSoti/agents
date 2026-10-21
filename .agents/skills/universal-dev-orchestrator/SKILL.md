---
name: universal-dev-orchestrator
description: Universal software-engineering operating system for AI coding agents, covering the full idea-to-production pipeline (spec, plan, TDD, build, E2E/browser verification, two-stage review, QA, release). Use this skill for ANY code change, bug fix, feature, refactor, review, SQL/database work, migration, test/QA task, CI/CD or deployment task, and whenever work is split across multiple agents running in parallel (orchestrator/worker setups, worktrees, handoffs). Handles Figma design-to-code handoff for React UI. Use it even if the user does not say "skill" - trigger on requests like "implement", "fix", "change", "optimize", "review", "write a query", "add tests", "deploy", "release", "run agents in parallel", or "orchestrate". Enforces accurate, minimal, verified changes and defines roles, scope locks, and handoff protocols for multi-agent runs.
---

# Universal Dev Orchestrator

Goal: make every change **accurate, minimal, verified, and reversible**, whether you work alone or as one of several parallel agents.

## 0. Prime directives (always on)

1. **Understand before editing.** Read the code, tests, and conventions around the target. Never change what you have not read.
2. **Smallest correct change.** Fix the stated problem. No drive-by refactors, renames, formatting sweeps, or dependency bumps unless asked.
3. **Evidence over assumption.** Every claim ("this works", "this is unused", "this is the cause") needs a command output, test result, or file/line reference. If you cannot verify, say so.
4. **Match the repo.** Follow existing style, patterns, naming, and tooling. Check `AGENTS.md`, `README`, `CONTRIBUTING`, lint/format config first.
5. **Stay in scope.** Touch only files your task brief allows. Out-of-scope needs are reported, not done.
6. **Never destroy silently.** No deleting data, force-push, dropping tables, rewriting history, or disabling tests/checks without explicit approval.
7. **Secrets never enter code, logs, or commits.**
8. **Ask only when blocked.** If the ambiguity is small, choose the safest reasonable default, state the assumption, and proceed. Ask only when a wrong guess is costly or irreversible.
9. **File Landing Taxonomy.** Always consult `AGENTS.md` before creating any documentation or scripts during feature planning and delivery. Strictly land files into designated subdirectories (`docs/01-*` through `docs/07-*`, `backend-requests/`, `design-system/`, `scripts/01-*` through `scripts/04-*`). Never place loose markdown or docx files in project root or `docs/` root.

> **Paths**: `scripts/`, `references/`, `roles/`, `templates/` are relative to THIS skill's folder. Run scripts from the target repo root, e.g. `bash <skill-dir>/scripts/verify.sh`.

## 1. Standard loop (every task)

```
CLASSIFY -> SPEC -> PREFLIGHT -> PLAN -> CLAIM -> CHANGE (TDD) -> VERIFY -> REVIEW -> REPORT
```
Hard gates (from the top-ranked community skills, see `SOURCES.md`): **no code before confirmed acceptance criteria** (`playbooks/01`), **no production code before a failing test** (`playbooks/03`), **no success claim without fresh evidence** (`playbooks/04`), **spec-compliance review before quality review** (`playbooks/06`). Whole-project flow: `playbooks/00-end-to-end-pipeline.md`.

| Step | What to do | Detail |
|---|---|---|
| CLASSIFY | Pick task type (below) and risk level | this file |
| SPEC | Acceptance criteria + non-goals (skip only for trivial, fully specified tasks) | `playbooks/01-spec-interview.md` |
| PREFLIGHT | Run `scripts/preflight.sh`; learn stack, test cmds, git state | `references/01-requirements-and-planning.md` |
| PLAN | Thin vertical slices: files, test-first, verify cmd, rollback | `playbooks/02-plan-vertical-slices.md`, `templates/task-brief.md` |
| CLAIM | In multi-agent runs, claim files via `scripts/claim.py` | `references/10-orchestration-protocol.md` |
| CHANGE | Red -> green -> refactor in small steps | `playbooks/03-tdd.md`, `references/03-implementation-standards.md` |
| VERIFY | `scripts/verify.sh` + targeted tests + E2E for user-facing work; `scripts/scope_check.py` | `playbooks/04`, `playbooks/05`, `references/06-testing-and-qa.md` |
| REVIEW | Stage 1 spec compliance, stage 2 five-axis quality | `playbooks/06-two-stage-review.md`, `references/04-code-review-and-refactoring.md` |
| REPORT | Fill `templates/change-report.md` honestly; run `python scripts/check_report.py <report>` | `playbooks/04-verification-gate.md` |

## 2. Task routing - read only what you need

| If the task involves... | Read |
|---|---|
| Unclear/large request, estimating, breaking down work | `references/01-requirements-and-planning.md` |
| New module, API design, data model, tech choices | `references/02-architecture-and-design.md` |
| Writing or modifying code in any language | `references/03-implementation-standards.md` |
| Reviewing a diff, refactoring, cleaning up | `references/04-code-review-and-refactoring.md` |
| SQL, schema, migrations, indexes, query tuning | `references/05-sql-and-database.md` |
| Tests, coverage, QA, regression, test plans | `references/06-testing-and-qa.md` |
| Auth, input handling, secrets, dependencies, OWASP | `references/07-security.md` |
| CI pipelines, Docker, releases, deploy, rollback | `references/08-ci-cd-and-deployment.md` |
| Bugs, crashes, flaky tests, production incidents | `references/09-debugging-and-incidents.md` |
| Figma links, design-to-code, UI matching a design, design tokens | `playbooks/09-figma-design-to-code.md`, `templates/design-handoff.md` |
| React UI, components, hooks, state, forms, frontend tests | `references/11-react-frontend.md` and `roles/frontend-engineer.md` |
| .NET / ASP.NET Core API, EF Core, endpoints, auth, backend tests | `references/12-dotnet-api.md` and `roles/backend-engineer.md` |
| Starting a new app/feature end to end, stage gates | `playbooks/00-end-to-end-pipeline.md` |
| Browser / E2E tests, deploy smoke tests | `playbooks/05-browser-e2e-testing.md` |
| Writing context packs/AGENTS.md for agents | `playbooks/07-context-engineering.md` |
| Merging a branch, pre-launch, go-live | `playbooks/08-ship-checklist.md` |
| More than one agent, parallel runs, handoffs | `references/10-orchestration-protocol.md` and `roles/` |

Multiple rows can apply. Load the minimum set; do not read everything.

## 3. Risk levels (decide in CLASSIFY)

- **Low**: docs, comments, tests-only, isolated small fix. Verify with targeted tests.
- **Medium**: feature logic, refactor within a module, new endpoint. Full test suite + lint + typecheck.
- **High**: auth/payments/permissions, DB migrations, data deletion, public API/contract change, infra/deploy config, concurrency. Requires: written plan, rollback plan, independent review by a second agent/role, and human approval before merge/deploy.

When unsure, round up one level.

## 4. Definition of Done

A change is done only when ALL hold:
- [ ] Behavior matches the request (acceptance criteria listed and checked)
- [ ] Build, lint, typecheck pass (or pre-existing failures are documented)
- [ ] Relevant tests added/updated and passing; bug fixes include a regression test that fails without the fix
- [ ] Diff contains only in-scope files; no debug code, stray files, or commented-out blocks
- [ ] No new secrets, no new warnings, no unexplained dependency changes
- [ ] Docs/config/migrations updated where needed
- [ ] Change report written, with known gaps and rollback steps, and `scripts/check_report.py` passes

## 5. Output contract

Final message to the user or orchestrator must be short and structured:

```
RESULT: done | partial | blocked
SUMMARY: 1-3 sentences
FILES: path (what changed) ...
VERIFIED: commands run + outcomes
NOT VERIFIED: honest gaps
RISKS/FOLLOW-UPS: ...
ROLLBACK: how to undo
```

## 6. Multi-agent quick rules

- Default stack split: **frontend-engineer** (React) and **backend-engineer** (.NET API) work in parallel against a shared **API contract** (OpenAPI) that the orchestrator defines first. SQL/migrations go to **sql-specialist**.
- One **orchestrator** plans and merges; **workers** implement in isolated git worktrees; **reviewer/QA/deploy** roles gate quality. Role prompts live in `roles/`.
- Workers never edit files claimed by another agent. Shared files (lockfiles, schemas, configs, routers) go to a single owner.
- Communicate through files in `.agent/` (briefs, claims, handoffs, reports) - not assumptions.
- Create isolated workspaces with `scripts/new_worktree.sh <agent-name> <base-branch>`.
- Merge order: contracts/migrations first, then implementation, then tests/docs, then deploy config.

Full protocol: `references/10-orchestration-protocol.md`.

## 7. When things go wrong

- Tests fail after your change: assume your change is the cause until proven otherwise. Do not weaken or delete tests to pass.
- Requirement conflicts with code reality: stop, report the conflict with evidence, propose options.
- Two agents collided: the later claimant stops, reports, and waits for the orchestrator.
- You are looping (3 failed attempts at the same fix): stop, re-read the code, write down what you know vs. assume, and change approach or escalate.
