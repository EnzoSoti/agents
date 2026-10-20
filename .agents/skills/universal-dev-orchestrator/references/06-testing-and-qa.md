# Testing & QA

## Contents
1. Test strategy
2. Writing good tests
3. Bug-fix protocol
4. QA test plan
5. Regression, flaky tests, coverage
6. API / UI / DB / performance testing
7. QA sign-off

## 1. Test strategy (pyramid)
- **Unit** (many, fast, isolated): pure logic, edge cases.
- **Integration** (some): modules + real DB/queue/HTTP stubs; contract tests between services.
- **End-to-end** (few, critical user journeys only): login, checkout, core workflow.
- Add the **lowest-level test that would catch the bug**. Mock only true external boundaries (network, clock, randomness, third parties), not your own logic.

## 2. Writing good tests
- Arrange-Act-Assert; one behavior per test; name states behavior ("rejects expired token").
- Deterministic: control time, randomness, ordering, and network. No sleeps; wait on conditions.
- Independent: no shared state or order dependence; clean up created data.
- Assert outcomes, not implementation details. Avoid over-mocking.
- Cover: happy path, boundaries (0/1/N/max), empty/null, invalid input, permissions, error paths, idempotency/retries, concurrency where relevant, time zones, unicode.
- Test data: minimal, builders/factories, no production data or PII.
- Never delete, skip, or loosen a failing test to get green. If a test is wrong, explain why and fix it explicitly.

## 3. Bug-fix protocol
1. Reproduce (exact steps, input, environment). Capture failing output.
2. Write a failing test that encodes the bug.
3. Find root cause (see `09-debugging-and-incidents.md`).
4. Fix the cause, not the symptom.
5. Test passes; run the surrounding suite for regressions.
6. Consider sibling code with the same flaw; list (don't silently mass-edit) other occurrences.

## 4. QA test plan (use for features/releases)
Include:
- Scope, out-of-scope, environments, test data needs
- Traceability: each acceptance criterion -> test case(s)
- Test cases: ID, preconditions, steps, expected result, priority
- Negative/boundary cases; permission matrix (roles x actions)
- Compatibility (browsers/devices/OS/DB versions) where relevant
- Accessibility (keyboard, screen reader, contrast) and i18n where relevant
- Data migration/backfill verification
- Rollback verification
- Exit criteria: all P0/P1 pass, no open blocker/critical, known issues documented

## 5. Regression, flaky tests, coverage
- Run the full suite for medium/high risk; targeted + smoke for low risk.
- Flaky test: reproduce by looping, find the race/time/order dependency, fix root cause. Quarantine only with an owner and ticket; never ignore.
- Coverage is a signal, not a goal. Prioritize branch coverage on changed code and risky paths; don't write meaningless tests to hit a number.
- Mutation/property-based testing for core algorithms when available.

## 6. Specialized testing
- **API**: status codes, schema/contract, auth/authZ, validation errors, pagination, idempotency, rate limits, backward compatibility.
- **UI**: user-visible behavior via role/label selectors; avoid brittle CSS selectors; check loading/error/empty states; visual regression only where valuable.
- **DB**: migrations up/down on realistic data; constraint behavior; query results and plans on representative volume; transaction/rollback behavior.
- **Performance**: define SLO; load/stress/soak test with realistic data; compare to baseline; watch p95/p99, error rate, CPU/memory, DB connections.
- **Security**: see `07-security.md` (authZ tests, injection inputs, secrets scanning, dependency audit).

## 7. QA sign-off format
```
QA VERDICT: PASS | PASS WITH KNOWN ISSUES | FAIL
Scope tested: ...
Evidence: commands/results/links
Failures & severity: ...
Not tested (and why): ...
Release risk: low | medium | high
```
