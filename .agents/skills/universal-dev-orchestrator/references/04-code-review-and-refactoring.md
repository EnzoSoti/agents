# Code Review & Refactoring

## Self-review protocol (run on every diff)
Read your diff as a hostile reviewer. Answer each:
1. **Correct?** Does it satisfy every acceptance criterion? Trace one happy path and two edge paths by hand.
2. **Minimal?** Any line not required by the task? Revert it.
3. **Safe?** Inputs validated, errors handled, resources closed, concurrency considered, auth checks intact?
4. **Compatible?** Callers, serialization formats, DB schema, public API unaffected (or all updated)?
5. **Tested?** Do tests fail without the change? Do they assert behavior, not implementation?
6. **Readable?** Would a new teammate understand it in one pass?
7. **Observable?** Failures diagnosable from logs/metrics?
8. **Clean?** No debug output, secrets, dead code, unrelated formatting.

## Reviewer-role output format (when acting as reviewer)
Classify each finding:
- **BLOCKER**: wrong behavior, security hole, data loss, broken contract, missing test for risky path
- **MAJOR**: likely bug, poor error handling, perf trap, maintainability hazard
- **MINOR**: style, naming, small clarity
- **QUESTION**: need intent clarified
Each finding: `file:line` - problem - why it matters - suggested fix. End with verdict: APPROVE / APPROVE WITH NITS / CHANGES REQUESTED. Do not approve unless you ran or read the test evidence.

## Refactoring rules
- Refactor only with a safety net: tests that pin current behavior. If none exist, write characterization tests first.
- **Behavior must not change.** Separate refactor commits from feature/bug commits.
- Small mechanical steps (extract function, rename, move, inline). Run tests after each.
- Use tooling (IDE/AST refactors, codemods) for renames/moves; verify with search that no stale references remain.
- Stop when the goal is met. "While I'm here" cleanups go in a follow-up list.

## Technical-debt handling
Do not fix unrelated debt inside a feature change. Record it in the report: location, impact, suggested fix, effort.
