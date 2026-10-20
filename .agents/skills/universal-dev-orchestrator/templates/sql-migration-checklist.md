# SQL Migration Checklist

- Engine/version: ______   Tool: ______   Risk: HIGH (default)
- [ ] Purpose and affected tables/rows documented
- [ ] Data shape inspected (row counts, nulls, duplicates, size)
- [ ] Backward compatible with currently deployed app version (expand phase)
- [ ] Up AND down scripts (or "irreversible + backup required" noted)
- [ ] Online/non-blocking strategy for large tables; lock & statement timeouts set
- [ ] Backfill batched, throttled, idempotent, resumable
- [ ] Constraints/indexes added safely (concurrently / NOT VALID then VALIDATE / ONLINE)
- [ ] Tested on realistic-volume copy: up -> down -> up
- [ ] EXPLAIN reviewed for new/changed queries
- [ ] Row-count assertions and post-migration verification queries written
- [ ] Rollback script + backup location recorded
- [ ] Independent review done; human approval before any non-dev environment
- [ ] Contract-phase (drops/NOT NULL) scheduled for a LATER release
