# SQL & Database

## Contents
1. Golden rules
2. Writing queries
3. Schema design
4. Migrations (expand/contract)
5. Indexing and tuning
6. Transactions and concurrency
7. Safe data changes
8. Dialect notes
9. DB review checklist

## 1. Golden rules
1. **Identify the engine and version first** (PostgreSQL, MySQL/MariaDB, SQL Server, SQLite, Oracle). Syntax and behavior differ; check dialect notes below.
2. **Never run destructive SQL against a shared/prod DB without approval.** Default to read-only. Use a local/dev/test database.
3. **Parameterize all values.** Never concatenate user input into SQL (SQL injection).
4. **Every write is wrapped and reversible**: transaction + backup/rollback script, or a dry-run SELECT first.
5. **Look at the data shape** (counts, nulls, duplicates) before writing a migration or constraint.
6. **Prove performance with EXPLAIN**, not guesses.

## 2. Writing queries
- Select explicit columns; avoid `SELECT *` in application code.
- Always `ORDER BY` with a deterministic tiebreaker when using LIMIT/pagination. Prefer keyset (seek) pagination over large OFFSET.
- Use explicit `JOIN ... ON`; never implicit comma joins. Pick the right join type; watch for row multiplication on 1-to-many joins.
- Use `EXISTS` for existence checks; be careful with `NOT IN` and NULLs (use `NOT EXISTS`).
- NULL logic: `= NULL` is never true; use `IS NULL`, `IS DISTINCT FROM` (where supported), `COALESCE`.
- Keep predicates **sargable**: no functions on indexed columns (`WHERE DATE(created_at)=...` -> use range `created_at >= ... AND < ...`). Match data types to avoid implicit casts.
- Use CTEs for readability; know your engine's CTE materialization behavior before assuming performance.
- Window functions for ranking/running totals instead of self-joins.
- Aggregates: every non-aggregated SELECT column must be in GROUP BY (or functionally dependent).
- Be explicit with time zones; store/compare in UTC.
- Format: uppercase keywords, one clause per line, aliases meaningful, comment non-obvious logic.

## 3. Schema design
- PK on every table (surrogate bigint/identity or natural where stable). FK constraints with deliberate `ON DELETE` behavior.
- `NOT NULL` by default; `UNIQUE`/`CHECK` constraints encode invariants in the DB, not only in app code.
- Correct types: DECIMAL for money, timestamptz/datetime in UTC, boolean for flags, enums/lookup tables for closed sets, UUID/ULID where distributed IDs matter.
- Name consistently (snake_case, singular or plural per repo convention). Index FK columns used in joins.
- Avoid EAV, comma-separated lists in a column, and polymorphic FKs unless the repo already accepts them.
- Plan retention, PII (encrypt/mask), and audit columns.

## 4. Migrations (expand -> migrate -> contract)
Rules:
- Every migration has an **up** and a tested **down** (or an explicit "irreversible, backup required" note).
- Migrations are **immutable once merged/applied**; fix forward with a new migration.
- Zero-downtime pattern for breaking changes:
  1. **Expand**: add new nullable column/table/index (backward compatible). Deploy.
  2. **Dual-write / backfill** in batches (chunked, throttled, resumable, idempotent). Verify counts.
  3. **Switch reads** to new structure. Deploy. Observe.
  4. **Contract**: add NOT NULL/constraints, then drop old columns in a **later** release.
- Large tables: add indexes concurrently/online (`CREATE INDEX CONCURRENTLY` in PostgreSQL; `ALGORITHM=INPLACE/INSTANT`, `LOCK=NONE` where supported in MySQL; `ONLINE=ON` in SQL Server). Avoid long exclusive locks; set lock/statement timeouts.
- Adding NOT NULL with default or a constraint on a big table: use the engine's safe path (e.g. add as NOT VALID then VALIDATE in PostgreSQL).
- Never rename/drop a column used by running code in the same release.
- Test: run migration on a copy with realistic volume; run up -> down -> up.
- High risk by default: require human approval before applying outside local/dev.

## 5. Indexing and tuning
Workflow:
1. Get the slow query + parameters + row counts.
2. `EXPLAIN` (`EXPLAIN (ANALYZE, BUFFERS)` in PostgreSQL on a safe environment; `EXPLAIN ANALYZE` in MySQL 8; Actual Execution Plan in SQL Server).
3. Look for: full scans on big tables, bad row estimates (stale stats -> `ANALYZE`/update statistics), sorts spilling to disk, nested loops over large sets, N+1 patterns from the app.
4. Fix in this order: rewrite query/remove work -> add/adjust index -> fix stats -> schema change -> cache.
- Index design: equality columns first, then range, then sort; covering/INCLUDE columns when useful; partial/filtered indexes for skewed data; don't index low-cardinality columns alone; every index costs writes and storage.
- Drop unused/duplicate indexes only after verifying usage stats over a full cycle.
- Re-run EXPLAIN after the change and record before/after timing and plan.

## 6. Transactions and concurrency
- Keep transactions short; no network calls or user waits inside them.
- Know the isolation level; use `SELECT ... FOR UPDATE` / optimistic version columns for read-modify-write.
- Prevent deadlocks: consistent lock ordering across code paths. Retry on deadlock/serialization failure with backoff.
- Idempotent writes: unique constraints + `INSERT ... ON CONFLICT` / `MERGE` / `ON DUPLICATE KEY UPDATE`.

## 7. Safe data changes (UPDATE/DELETE/backfill)
1. Write the matching `SELECT` first; check the row count and sample rows.
2. Take a backup or copy affected rows to a temp/archive table.
3. Run inside a transaction; assert expected row count (`ROW_COUNT`/`@@ROWCOUNT`); commit only if it matches.
4. Batch large changes (e.g. 1k-10k rows per batch) to limit locks and replication lag.
5. Always include a `WHERE`; refuse statements without one.
6. Verify after: counts, spot checks, constraints still valid.
7. Keep the script in version control with a rollback script.

## 8. Dialect notes
| Topic | PostgreSQL | MySQL | SQL Server | SQLite |
|---|---|---|---|---|
| Limit rows | `LIMIT n` | `LIMIT n` | `TOP n` / `OFFSET FETCH` | `LIMIT n` |
| Upsert | `ON CONFLICT` | `ON DUPLICATE KEY UPDATE` | `MERGE` | `ON CONFLICT` |
| Auto ID | `GENERATED ... AS IDENTITY` | `AUTO_INCREMENT` | `IDENTITY` | `INTEGER PRIMARY KEY` |
| String concat | `||` / `concat()` | `CONCAT()` | `+` / `CONCAT()` | `||` |
| Case-insens. match | `ILIKE` | collation-based | collation-based | `LIKE` (ASCII) |
| Online index | `CONCURRENTLY` | INPLACE/INSTANT | `ONLINE=ON` | n/a |
| Boolean | native | TINYINT(1) | BIT | 0/1 |
| JSON | `jsonb` | `JSON` | `JSON` funcs / NVARCHAR | JSON1 |

## 9. DB review checklist
- [ ] Parameterized; no string-built SQL
- [ ] Correct dialect/version syntax
- [ ] Deterministic ordering with pagination
- [ ] NULL handling verified
- [ ] EXPLAIN reviewed; indexes justified
- [ ] Migration has up/down, is online-safe, tested on realistic data
- [ ] Constraints/FKs/types appropriate; money/time handled correctly
- [ ] Destructive ops: backup + row-count assertion + approval
- [ ] ORM-generated SQL inspected (N+1, missing joins, over-fetching)
- [ ] Permissions: least privilege for app DB user
