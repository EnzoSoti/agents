# .NET API Standards (ASP.NET Core)

## Contents
1. Discover conventions first
2. Structure and layering
3. Endpoints and contracts
4. Validation and errors
5. Data access (EF Core / SQL)
6. Async, DI, config
7. Security
8. Logging and observability
9. Testing
10. Build and deployment
11. Backend review checklist

## 1. Discover conventions first
Check: target framework (`net8.0`/`net9.0`...), controllers vs minimal APIs, architecture (layered/Clean/vertical slice), MediatR or services, ORM (EF Core/Dapper), DB engine (likely SQL Server or PostgreSQL), mapping (AutoMapper/Mapster/manual), validation (FluentValidation/DataAnnotations), auth (JWT/Identity/OIDC), logging (Serilog), test stack (xUnit/NUnit + Moq/NSubstitute + WebApplicationFactory/Testcontainers), analyzers/`.editorconfig`, `Directory.Build.props`. **Follow existing patterns.**

## 2. Structure and layering
- Keep dependencies pointing inward: API -> Application/Services -> Domain; Infrastructure implements interfaces. Controllers/endpoints stay thin (bind, authorize, call, map result).
- Business rules live in services/handlers/domain, not in controllers or EF configuration callbacks.
- Don't leak EF entities across the API boundary: use request/response **DTOs** (records are fine).

## 3. Endpoints and contracts
- RESTful resources and verbs; correct status codes: 200/201 (+`Location`)/204, 400 validation, 401, 403, 404, 409 conflict, 422 if the repo uses it, 500 never intentionally.
- `[ApiController]`, `ActionResult<T>`/`TypedResults`, `[ProducesResponseType]` so Swagger/OpenAPI is accurate. **The OpenAPI document is the contract** shared with the frontend.
- Backward compatibility: additive changes only (new optional fields/endpoints). Renames/removals/type changes need a new API version (`Asp.Versioning`) and frontend coordination.
- Pagination, filtering, sorting on list endpoints (bounded page size). Use `CancellationToken` in handlers.
- Idempotency for retried unsafe operations where relevant.

## 4. Validation and errors
- Validate every input at the boundary (FluentValidation/DataAnnotations); never trust the client.
- Return **RFC 7807 ProblemDetails** consistently; use a global exception handler (`IExceptionHandler`/middleware). Don't leak stack traces or internals.
- Use exceptions for exceptional cases; use result types/typed errors for expected business failures (match repo style).

## 5. Data access (EF Core / SQL)
- Use `AsNoTracking()` for read-only queries; project to DTOs with `Select` instead of loading whole graphs.
- Avoid N+1: use `Include`/projection deliberately; inspect generated SQL (`ToQueryString()`, logging) for non-trivial queries.
- Never `FromSqlRaw` with concatenated input; use `FromSqlInterpolated`/parameters. Dapper: always parameters.
- Pagination must have deterministic `OrderBy`. Use transactions for multi-step writes (`SaveChanges` is atomic per call; use explicit transactions across calls). Handle concurrency with `rowversion`/concurrency tokens.
- **Migrations**: `dotnet ef migrations add <Name>`; review the generated SQL (`dotnet ef migrations script`); keep expand/contract compatibility (see `05-sql-and-database.md`); never edit an applied migration; never auto-apply to production from app startup unless the repo mandates it and it's safe. Test up and down locally.
- Index and constraint changes are configured in the model + migration and reviewed with EXPLAIN/execution plans on realistic data.
- DB-specific: SQL Server - `datetime2`, `decimal(18,2)`, `rowversion`, `OFFSET/FETCH`, filtered/included indexes, `ONLINE=ON` for index builds where licensed; PostgreSQL - `timestamptz`, `jsonb`, `CONCURRENTLY`.

## 6. Async, DI, config
- `async/await` all the way; no `.Result`/`.Wait()`; pass `CancellationToken`; don't use `async void`.
- Register services with correct lifetimes (Scoped for DbContext; Singleton only for stateless/thread-safe; beware captive dependencies). Use constructor injection; no service locator.
- Configuration via the Options pattern (`IOptions<T>`, validated on start); secrets from user-secrets/environment/Key Vault, never committed.
- Use `HttpClientFactory` for outbound calls with timeouts, retries (Polly/resilience handlers) and circuit breakers.
- Nullable reference types enabled; treat new warnings as problems.

## 7. Security
- `[Authorize]` by default (fallback policy), explicit `[AllowAnonymous]` only where intended. Policy-based authorization; **verify resource ownership/tenant on every access** (prevent IDOR).
- JWT: validate issuer, audience, lifetime, signing key; short-lived tokens; refresh handled securely.
- CORS: explicit allowed origins/methods/headers (never `AllowAnyOrigin` with credentials). HTTPS + HSTS. Anti-forgery if using cookie auth.
- Rate limiting for auth/expensive endpoints (`AddRateLimiter`). Request size limits. Security headers.
- Passwords via ASP.NET Identity hasher or vetted library. No sensitive data in logs. Mask PII.
- Keep packages updated and audited (`dotnet list package --vulnerable`).

## 8. Logging and observability
- Structured logging with message templates (`logger.LogInformation("Order {OrderId} created", id)`), correct levels, correlation IDs; no secrets/PII.
- Health checks (`/health/live`, `/health/ready`) including DB. Metrics/tracing via OpenTelemetry if the repo uses it.

## 9. Testing
- **Unit**: services/handlers with mocked boundaries; test business rules, edge cases, error paths.
- **Integration**: `WebApplicationFactory<Program>` + real DB (Testcontainers or a dedicated test DB; avoid EF InMemory for relational behavior). Cover auth (401/403/200), validation (400), not-found (404), conflict (409), happy path.
- Contract test: OpenAPI snapshot or generated-client compile check to detect accidental breaking changes.
- Bug fix: failing test first. Deterministic tests (fake clock via `TimeProvider`).

## 10. Build and deployment
- Verify: `dotnet restore`, `dotnet build -warnaserror` (if the repo does), `dotnet format --verify-no-changes` (if used), `dotnet test`.
- Publish with `dotnet publish -c Release`; multi-stage Dockerfile using SDK for build and ASP.NET runtime image for run, non-root user.
- Run migrations as a separate controlled step (migration bundle `dotnet ef migrations bundle` or SQL script) before/with deployment; backward compatible with the currently running version.
- Config per environment (`appsettings.{Env}.json` minus secrets, env vars, Key Vault). Health-check gate before routing traffic.

## 11. Backend review checklist
- [ ] Contract preserved (or versioned and coordinated with frontend)
- [ ] DTOs used; no entity leakage; input validated
- [ ] AuthZ on every endpoint incl. object-level checks
- [ ] ProblemDetails errors; correct status codes
- [ ] EF queries efficient (no N+1, projections, AsNoTracking, deterministic paging)
- [ ] Migration reviewed, safe, reversible; SQL generated inspected
- [ ] Async/CT correct; DI lifetimes correct; no blocking calls
- [ ] No secrets/PII in code/logs; config via Options
- [ ] Unit + integration tests cover success and failure paths
