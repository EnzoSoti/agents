# Task Brief: T-XXX <title>

- **Owner/role**:        <agent name / implementer | sql-specialist | ...>
- **Branch / worktree**: agent/<name> / ../wt-<name>
- **Risk**:              low | medium | high
- **Depends on**:        T-... (or none)

## Goal
<one sentence user-visible outcome>

## Acceptance criteria
- [ ] Given ... when ... then ...
- [ ] ...

## Design source (UI tasks)
<Figma link/node, states, viewports; see templates/design-handoff.md>

## Context
<relevant files, links, contracts, prior decisions>

## Allowed paths (may edit)
- src/...
- tests/...

## Forbidden / owned by others
- <shared files, other agents' modules>

## Approach (plan, <=15 lines)
1.
2.

## Required checks
- scripts/verify.sh
- scripts/scope_check.py --allow ...
- <specific tests / EXPLAIN / migration up-down-up>

## Non-goals
-

## Risks & rollback
- Risk:
- Rollback:

## Deliverables
- Code + tests on branch
- `.agent/reports/T-XXX.md`
- Handoff to: <role>
