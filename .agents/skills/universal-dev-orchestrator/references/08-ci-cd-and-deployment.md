# CI/CD & Deployment

## Contents
1. Pipeline stages
2. Build and containers
3. Environments and config
4. Release strategies
5. Pre-deploy gate
6. Deploy runbook
7. Post-deploy and rollback
8. Infra-as-code rules

## 1. Pipeline stages
`checkout -> install (cached, locked) -> lint/format -> typecheck -> unit tests -> build -> integration tests -> security scans (deps, secrets, SAST, image) -> package/publish artifact -> deploy to staging -> smoke/e2e -> approval (prod) -> deploy prod -> verify`
- Fast feedback first; fail early. Build once, deploy the **same artifact** through all environments.
- Deterministic builds: lockfiles, pinned base images/actions (by digest/SHA when possible).
- Do not weaken or bypass CI checks to ship. Do not commit secrets to workflow files; use the platform's secret store with least privilege.

## 2. Build and containers
- Multi-stage Dockerfiles; minimal base image; non-root user; no secrets in layers; `.dockerignore`; HEALTHCHECK where appropriate; pinned tags/digests.
- Image scanning and SBOM when available.
- Small, cacheable layers: dependencies before source.

## 3. Environments and config
- dev -> staging (prod-like) -> production. Config via environment, not code. Same code, different config.
- Feature flags for risky changes; default off; remove after rollout.
- Migrations run as a separate, controlled step (see `05-sql-and-database.md`), compatible with both old and new app versions during rollout.

## 4. Release strategies (choose by risk)
- **Rolling**: default for stateless services.
- **Blue/green**: instant switch and rollback; needs 2x capacity.
- **Canary**: route 1-5% -> watch metrics -> ramp. Best for high risk.
- **Feature flag / dark launch**: decouple deploy from release.
- Versioning: semantic versioning; changelog entry; tag the release commit.

## 5. Pre-deploy gate (all must be true)
- [ ] CI green on the exact commit being deployed
- [ ] QA verdict PASS (or accepted known issues)
- [ ] Reviewer approval; high risk has second-agent review and human approval
- [ ] Migrations reviewed, backward compatible, backups verified
- [ ] Config/secrets present in target environment
- [ ] Rollback plan written and rehearsed or trivially safe
- [ ] Monitoring/alerts exist for new paths; on-call aware
- [ ] Change window / freeze rules respected

## 6. Deploy runbook (template in `templates/release-checklist.md`)
1. Announce start; confirm artifact version/commit.
2. Apply backward-compatible migrations (expand step).
3. Deploy app (rolling/canary).
4. Smoke tests: health endpoint, key user journey, DB connectivity, dependency calls.
5. Watch: error rate, latency p95/p99, saturation, business KPIs, logs, queue depth for the agreed window.
6. Ramp or complete; announce done.

## 7. Post-deploy and rollback
- **Rollback triggers** (define beforehand): error rate or latency above threshold, failed smoke test, data-integrity alarm.
- Rollback = redeploy previous artifact / flip flag / switch traffic back. Because migrations are backward compatible, app rollback should not require DB rollback. Never drop data as part of rollback.
- After incident or rollback: write a short postmortem (impact, timeline, root cause, fix, prevention).

## 8. Infra-as-code rules
- Run `plan`/`diff` and review before `apply`. Never apply to prod without approval.
- Small, reversible changes; separate state per environment; no manual console drift.
- Tag resources, restrict network/IAM, encrypt at rest, enable backups and verify restores.
- Destructive plan output (destroy/replace of stateful resources) = high risk, stop and escalate.
