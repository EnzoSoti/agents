# Debugging & Incidents

## Method (scientific, not guess-and-patch)
1. **Reproduce** reliably; capture exact input, environment, version, logs, stack trace.
2. **Narrow**: bisect by commit (`git bisect`), by input, by layer (UI/API/service/DB), by config.
3. **Hypothesize** 1-3 causes; for each, define an observation that would confirm or refute it.
4. **Test hypotheses** cheaply (logging, debugger, minimal repro, query the DB, read the code path). Change one variable at a time.
5. **Root cause** = the earliest incorrect decision/state, not the place the error surfaced. Ask "why" until the fix prevents the class of bug.
6. **Fix + regression test** (see `06-testing-and-qa.md`).
7. **Verify** original repro is gone and nothing nearby regressed.
8. **Remove** temporary debug code.

## Common culprits to check
Off-by-one/boundaries, null/undefined, async/await and race conditions, shared mutable state, time zones/DST, locale/encoding, integer overflow/float precision, caching/stale data, config/env mismatch, dependency version drift, N+1 queries, transactions not committed/rolled back, retries causing duplicates, resource leaks.

## Anti-looping rule
After 3 failed attempts on the same hypothesis: stop, list what is KNOWN (evidence) vs ASSUMED, re-read the code path end to end, and pick a different approach or escalate with your findings.

## Flaky or intermittent failures
Loop the test (e.g. 50-200x), vary order/parallelism, log timing and state, look for shared state/time/network/race. Fix the root cause; never add blind retries or sleeps as the fix.

## Production incident protocol
1. **Stabilize first**: mitigate impact (rollback, flag off, scale, failover) before deep diagnosis.
2. Communicate status and ETA; assign roles (incident lead, comms, investigator).
3. Preserve evidence (logs, metrics, timelines) before they roll off.
4. Diagnose with read-only access by default.
5. Fix forward only with review; avoid hot-patching untested code.
6. **Postmortem** (blameless): summary, impact, timeline, root cause, what went well/poorly, action items with owners.

## Report format for a bug investigation
```
SYMPTOM: ...
REPRO: steps + environment
ROOT CAUSE: file:line + explanation + evidence
FIX: what changed and why this addresses the cause
REGRESSION TEST: path::name
OTHER OCCURRENCES: list
```
