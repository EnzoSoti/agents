# Requirements & Planning

## Contents
1. Clarify the request
2. Preflight checklist
3. Write the plan
4. Break down work
5. Estimation and risk

## 1. Clarify the request
Extract, in this order:
- **Goal**: the user-visible outcome, in one sentence.
- **Acceptance criteria**: testable statements ("given X, when Y, then Z"). Write them down; you will verify each.
- **Constraints**: language/framework versions, performance budgets, compatibility, deadlines, forbidden areas.
- **Non-goals**: what you will explicitly not do.
- **Unknowns**: list them. Resolve by reading code first; ask only if still blocking and costly.

If the request is vague ("make it faster", "clean this up"), convert it to a measurable target (e.g. "p95 of /search < 300ms measured by X") and state your interpretation before coding.

## 2. Preflight checklist
Run `scripts/preflight.sh`, then confirm:
- [ ] Working tree state is known (clean or you know why not)
- [ ] You know the exact commands for: install, build, lint, typecheck, unit test, integration test, run locally
- [ ] You located the entry points and the code closest to the change
- [ ] You found existing tests covering the area
- [ ] You read `AGENTS.md` / `CONTRIBUTING` / lint config
- [ ] Baseline: tests/lint pass BEFORE your change (record failures that already exist)

## 3. Write the plan (use `templates/task-brief.md`)
A plan is 5-15 lines: goal, approach, files to touch, files NOT to touch, tests to add, risks, rollback. Prefer the approach that:
1. reuses existing code/patterns,
2. changes the fewest files,
3. is easiest to revert,
4. keeps public contracts stable.

For medium/high risk, list 2 alternatives and why you rejected them.

## 4. Break down work
- Slices should be **independently verifiable** (each ends with passing tests).
- Order: contracts/schema -> core logic -> integration -> UI/API surface -> tests/docs -> deploy config. (Tests are written alongside, not last.)
- For parallel agents, split along **file/module boundaries**, never along "same file, different function".
- Identify shared choke points (lockfiles, route tables, DB schema, global config, generated code). Assign each to exactly one owner.

## 5. Estimation and risk
- Size: S (<1 file group, <1h), M (one module), L (cross-module), XL (split it).
- XL requests must be decomposed before any agent starts.
- Mark high-risk items early (auth, money, data loss, migrations, concurrency, public API). They trigger the extra gates in `SKILL.md` section 3.
