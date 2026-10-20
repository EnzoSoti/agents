# Release Checklist: <service> <version> -> <environment>

## Gate
- [ ] CI green on commit <sha>; artifact <id/digest>
- [ ] Reviewer approved; QA verdict: PASS / PASS WITH KNOWN ISSUES
- [ ] High risk: second review + human approval recorded by <name>
- [ ] Migrations reviewed, backward compatible; backup verified
- [ ] Config/secrets present in target
- [ ] Rollback plan: <steps>; trigger thresholds: <error rate/latency/etc.>
- [ ] Monitoring/alerts in place; on-call notified
- [ ] Within change window

## Execute
- [ ] Apply expand-phase migrations
- [ ] Deploy (strategy: rolling | blue-green | canary %)
- [ ] Smoke tests: health, key journey, DB, dependencies
- [ ] Observe for <N> minutes: errors, p95/p99, saturation, KPIs, logs
- [ ] Ramp/complete OR roll back

## Close
- [ ] Tag/changelog updated
- [ ] Status announced
- [ ] Follow-ups (contract-phase migration, flag removal) ticketed
