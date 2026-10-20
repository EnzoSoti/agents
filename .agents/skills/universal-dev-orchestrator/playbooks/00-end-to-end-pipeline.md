# End-to-End Pipeline: idea -> production (React + .NET API)

Each stage has an **entry gate**, **exit gate**, **owner role**, and **artifact**. Do not skip a gate; if you must, log the waiver (who, why, risk) in `.agent/status.md`.

| # | Stage | Owner | Entry gate | Exit gate (evidence required) | Artifact |
|---|---|---|---|---|---|
| 0 | **Spec** | orchestrator/planner | request exists | acceptance criteria + non-goals confirmed (`01-spec-interview.md`) | `.agent/spec.md` |
| 1 | **Plan** | planner | spec confirmed | vertical slices with files, tests, verify cmds (`02-plan-vertical-slices.md`) | `.agent/briefs/T-*.md` |
| 2 | **Contract, data & design** | backend-eng + sql-specialist + frontend-eng | plan approved | OpenAPI + DTOs + schema reviewed; Figma frames/states/tokens confirmed (`09-figma-design-to-code.md`) | `openapi.yaml`, migration plan, design handoff |
| 3 | **Build** | frontend-eng, backend-eng (parallel worktrees) | contract committed | each slice: failing test first (`03-tdd.md`), then green, then refactor; `verify.sh` pass | commits + change reports |
| 4 | **Verify** | implementers + qa | slice green | unit + integration + E2E journey pass with fresh output (`04-verification-gate.md`, `05-browser-e2e-testing.md`) | test output, traces |
| 5 | **Review** | reviewer + security-auditor | verify evidence attached | stage 1 spec compliance, stage 2 quality, security checklist (`06-two-stage-review.md`) | review findings, verdict |
| 6 | **Integrate** | orchestrator | all slices approved | integration branch: full suite + E2E green | `integration/<run-id>` |
| 7 | **QA** | qa-tester | integration green | QA verdict PASS on staging with realistic data | QA sign-off |
| 8 | **Release** | deploy-engineer | gate in `08` + `08-ship-checklist.md` | staged rollout, smoke OK, metrics healthy for the agreed window | release checklist |
| 9 | **Observe & learn** | orchestrator | released | post-release review: what broke, what to automate | follow-ups, updated skill notes |

## Stop-the-line rules
Stop all stages and fix before continuing if: the build or main-branch tests are red; a security finding is BLOCKER; the contract and implementation disagree; a migration is not backward compatible; an agent reports "done" without evidence.

## Suggested repo layout
```
repo/
  AGENTS.md
  openapi/openapi.yaml          # contract (owner: backend)
  backend/  (src/, tests/, *.sln, Migrations/)
  frontend/ (src/, e2e/, package.json)
  .github/workflows/ci.yml
  .agent/   (spec.md, briefs/, claims/, handoffs/, reports/, status.md)
```

## Walking skeleton first
Before feature work, get one trivial slice (a page that calls one endpoint that reads one DB row) running end-to-end through CI and a staging deploy. This proves the pipeline early and exposes environment problems while they are cheap.
