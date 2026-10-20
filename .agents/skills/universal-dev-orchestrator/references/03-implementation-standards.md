# Implementation Standards (accurate, minimal changes)

## Contents
1. Before you type
2. How to change code
3. Quality rules
4. Language-agnostic hygiene
5. Performance optimization protocol
6. Git hygiene

## 1. Before you type
- Open the target file AND its callers, callees, tests, and types. Use search to find all usages (`rg`) before changing any signature, name, or behavior.
- Identify the invariants the existing code relies on. Preserve them or update every dependent.
- Prefer extending existing helpers over adding new ones. Search for an existing utility first.

## 2. How to change code
- **Small steps, each compiling/passing.** Don't leave the tree broken between steps.
- **Edit surgically.** Modify the minimal lines; keep unrelated formatting untouched. Never reformat whole files.
- **Keep public contracts stable** (function signatures, REST shapes, CLI flags, DB columns). If you must break one: update all callers, add migration notes, flag as high risk.
- **Add tests with the change**, not after. Bug fix = failing test first, then the fix.
- **One logical change per commit.** Message: imperative summary + why.

## 3. Quality rules
- **Correctness first, then clarity, then performance.**
- Handle edge cases explicitly: null/empty, boundaries (0, 1, max), unicode, time zones/DST, concurrency, partial failure, large inputs.
- Error handling: never swallow exceptions; add context; distinguish expected (return/typed error) from unexpected (raise/log).
- No magic numbers/strings; name constants. No dead code, no commented-out code, no stray `console.log`/`print`/TODO without issue link.
- Resource safety: close files/connections/cursors; use context managers/`defer`/`using`/try-finally.
- Immutability and pure functions where practical; isolate side effects.
- Names describe intent. Comments explain *why*, not *what*.
- Complexity guardrails: functions that fit on a screen, shallow nesting, early returns.
- Types: use the project's type system fully; avoid `any`/untyped escapes unless justified.

## 4. Language-agnostic hygiene
- Run formatter + linter + type checker the repo already uses. Do not introduce new tools.
- Pin versions as the repo does; do not upgrade dependencies as a side effect. Lockfile changes must be explained.
- Configuration via env/config files; no hardcoded hosts, credentials, or paths.
- Backward-compatible defaults for any new config or flag.
- Logs: structured, leveled, no secrets/PII, include correlation IDs if the codebase has them.

## 5. Performance optimization protocol
Never optimize on intuition.
1. **Define** the metric and target (latency p95, memory, throughput, query time).
2. **Measure baseline** with a repeatable benchmark/profile. Record numbers.
3. **Find the bottleneck** (profiler, EXPLAIN, flame graph, tracing). Fix the top one only.
4. **Change one thing**, re-measure, keep only if it helps beyond noise.
5. **Guard correctness**: tests must still pass; compare outputs old vs. new on sample data.
6. **Record** before/after numbers in the change report.
Common wins in order: remove unnecessary work -> fix algorithmic complexity -> batch/avoid N+1 -> cache with clear invalidation -> add index -> parallelize -> micro-optimize (last).

## 6. Git hygiene
- Work on a branch/worktree, never directly on main/master.
- `git status` and `git diff` before and after you work; review your own diff line by line.
- Do not commit generated files, build artifacts, `.env`, or large binaries unless the repo already does.
- Never `git push --force`, `reset --hard` shared work, or rewrite published history without explicit approval.
