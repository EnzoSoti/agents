# Architecture & Design

## Principles
- **Prefer boring technology** already used in the repo. New dependency = justify: what it replaces, maintenance status, license, size, security record.
- **Design for change at boundaries**: stable interfaces, replaceable internals.
- **Single responsibility** per module; high cohesion, low coupling; dependencies point inward (domain does not import framework/UI/DB drivers).
- **Make illegal states unrepresentable** with types/enums/constraints.
- **Fail fast and loudly** at boundaries; validate at the edges, trust inside.
- **YAGNI**: build for today's requirement; leave seams, not speculative features.

## When designing an API
- Version it or keep it backward compatible. Additive changes are safe; removals/renames are breaking.
- Consistent naming, pagination, error shape, idempotency for unsafe retries (PUT/DELETE; POST with idempotency key).
- Document status codes and error bodies. Validate input; never trust client-side checks.
- Define timeouts, retries (with backoff + jitter), rate limits.

## When designing data models
- Start from access patterns and invariants. Normalize by default (3NF); denormalize deliberately with a measured reason.
- Every table: primary key, NOT NULL where required, foreign keys, appropriate unique constraints, created/updated timestamps.
- Store money as integer minor units or DECIMAL, never float. Store time as UTC (timestamptz).
- Plan for soft-delete vs hard-delete and retention/PII rules up front.
- See `05-sql-and-database.md` for migration rules.

## Cross-cutting concerns checklist
Config & secrets, logging (structured, no PII/secrets), metrics, tracing, error handling, authN/authZ, caching (and invalidation), concurrency/transactions, i18n, accessibility, backward compatibility, observability of new code paths.

## Design record (for medium/high risk)
Write 10-20 lines: Context, Decision, Alternatives considered, Consequences, Rollback. Save as `docs/decisions/NNNN-title.md` if the repo uses ADRs, otherwise in the change report.

## Anti-patterns to avoid
Premature abstraction, god objects, shared mutable globals, hidden coupling via shared DB tables across services, boolean-flag parameters that change behavior, copy-paste of divergent logic, configuration that changes semantics silently.
