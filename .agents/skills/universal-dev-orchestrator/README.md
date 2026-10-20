# universal-dev-orchestrator

A Codex skill that makes AI agents accurate, minimal, and verifiable across the whole software lifecycle (planning -> design -> code -> review -> SQL -> QA -> deployment) and lets you run several agents in parallel safely.

## Layout
```
universal-dev-orchestrator/
  SKILL.md                  entry point (loaded when triggered)
  references/01..12-*.md    deep guidance (11 = React, 12 = .NET API), loaded on demand
  playbooks/00..09-*.md     stage gates + proven methods (spec, slices, TDD, evidence, E2E, 2-stage review, context, ship)
  SOURCES.md                what was learned from where, licenses, limits
  roles/*.md                orchestrator, planner, implementer, sql-specialist,
                            frontend-engineer (React), backend-engineer (.NET API),
                            reviewer, qa-tester, security-auditor, deploy-engineer
  templates/*.md            task brief, handoff, change report, release + SQL checklists, AGENTS.md snippet
  scripts/                  preflight.sh, verify.sh, scope_check.py, claim.py, new_worktree.sh, check_report.py
```

## Install
Copy the folder into a location your Codex version scans for skills, then restart/reload Codex:
- Per repo (recommended): `<repo>/.agents/skills/universal-dev-orchestrator/`
- Personal (all repos): `~/.agents/skills/universal-dev-orchestrator/`
- Older Codex versions used `.codex/skills/` and `~/.codex/skills/`; current OpenAI docs list `.agents/skills` for repo and user scopes.
(Skill discovery paths can differ between Codex versions/clients - check the Codex docs for yours, or explicitly tell Codex the path in your prompt.)

Optionally paste `templates/agents-md-snippet.md` into your repo's `AGENTS.md` so every session follows the workflow even without trigger matching.

## Single-agent use
Just ask normally ("fix the login bug", "write a migration to add X"). The skill triggers and enforces the loop: preflight -> plan -> change -> verify -> report.

## Multi-agent use (parallel Codex sessions)
1. Session A (orchestrator): "Use the universal-dev-orchestrator skill. Role: ORCHESTRATOR. Goal: <feature>."
   It writes briefs to `.agent/briefs/`, defines contracts, claims files, creates worktrees.
2. Open one Codex session per worktree (`../wt-<agent>`), each with:
   "Use the universal-dev-orchestrator skill. Role: IMPLEMENTER. Brief: .agent/briefs/T-00X.md."
3. Reviewer / QA / security / SQL sessions run read-only against branches.
4. Orchestrator merges on `integration/<run-id>`, runs full verification, then deploy role runs the release checklist (human approval for prod).

## Figma (optional)
Connect once: `codex mcp add figma --url https://mcp.figma.com/mcp` (OAuth sign-in), then give the frontend-engineer a Figma link via `templates/design-handoff.md`. Details and fallback: `playbooks/09-figma-design-to-code.md`. Verify the current setup in Figma's docs; plan/seat requirements apply.

## Notes
- Scripts are plain bash/python3, no dependencies. If the shell blocks direct execution, run `bash scripts/verify.sh`.
- `verify.sh` auto-detects Node, Python, Go, Rust, Maven, Gradle. For other stacks or custom commands, edit it or run your own and report the results.
- Customize: add your stack-specific rules as new files in `references/` and a row in the routing table in SKILL.md.
