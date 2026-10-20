# React Frontend Standards

## Contents
1. Discover conventions first
2. Components and structure
3. State and data fetching
4. Forms and validation
5. TypeScript
6. Performance
7. Accessibility and UX states
8. Security
9. Testing
10. Build/deploy notes
11. Frontend review checklist

## 1. Discover conventions first
Check before coding: React version, TypeScript vs JS, bundler (Vite/CRA/Next), router, state library (Redux Toolkit/Zustand/Context), data layer (TanStack Query/RTK Query/axios/fetch wrapper), UI kit (MUI/Ant/Tailwind/shadcn), form library, test stack (Jest or Vitest + React Testing Library, Playwright/Cypress), lint/format rules. **Follow what exists**; don't introduce a second way of doing the same thing.

## 2. Components and structure
- Function components + hooks. Small, single-purpose components; presentational vs container separation where the repo does it.
- Co-locate component, styles, tests, and types per the repo's structure (feature folders preferred).
- Props typed explicitly; avoid prop drilling beyond ~2-3 levels (use context or composition).
- Stable `key`s (ids, not array index for dynamic lists). No logic in JSX that deserves a named variable/function.
- Extract reusable logic into custom hooks (`useXxx`); hooks follow the Rules of Hooks and have complete dependency arrays.

## 3. State and data fetching
- Server state (API data) belongs in the data-fetching layer (e.g. TanStack Query): caching, retries, invalidation after mutations. Don't copy server data into local state without reason.
- Local UI state stays local; lift only as needed. Derive values instead of storing them.
- Always handle **loading, empty, error, and success** states. Show actionable errors; never swallow failed requests.
- Cancel/ignore stale requests (AbortController or library support); avoid race conditions on fast input changes (debounce search).
- Centralize the API client: base URL from env, auth header/interceptor, consistent error mapping (map ProblemDetails from .NET to UI messages).
- Use **typed API clients generated from OpenAPI** where available (e.g. NSwag/openapi-typescript) instead of hand-written types that drift.

## 4. Forms and validation
- Use the repo's form library (React Hook Form/Formik). Client validation is for UX only; the server remains the source of truth.
- Map server validation errors (400 ProblemDetails/`errors` dictionary) to fields.
- Disable submit while pending; prevent double-submit; show success/failure feedback.

## 5. TypeScript
- `strict` mode assumptions. No `any` to bypass errors; prefer `unknown` + narrowing. Model API shapes with types/zod schemas at the boundary.
- Discriminated unions for state machines (`{status:'loading'} | {status:'error', error} | ...`).

## 6. Performance
- Measure first (React Profiler, Lighthouse, bundle analyzer). Fix real problems only.
- Avoid unnecessary re-renders: stable references only where it matters (`useMemo`/`useCallback`/`React.memo` are tools, not defaults).
- Code-split routes (`React.lazy`/Suspense); virtualize long lists; lazy-load heavy libs and images; paginate server-side.
- Don't create objects/functions in render when passed to memoized children in hot paths.

## 7. Accessibility and UX states
- Semantic HTML first; labels for inputs; buttons are `<button>`; links are `<a>`.
- Keyboard operability, visible focus, ARIA only when native semantics are insufficient, sufficient contrast, alt text, announce async updates when needed.
- Responsive layouts; handle slow networks and long text; i18n via the existing mechanism (no hardcoded user-facing strings if the repo uses i18n).

## 8. Security
- React escapes by default; avoid `dangerouslySetInnerHTML` (sanitize with a vetted library if unavoidable). Validate/encode URLs (no `javascript:`).
- Never put secrets in client code or `VITE_`/`REACT_APP_` env vars (they are public). Only public config belongs there.
- Follow the repo's token strategy (prefer httpOnly cookies over localStorage when the backend supports it). Handle 401/403 centrally (redirect/refresh).
- CORS is configured on the API, not "fixed" by proxy hacks in production code.
- Audit dependencies (`npm audit`); don't add packages casually.

## 9. Testing
- React Testing Library: test behavior via roles/labels/text, not implementation or class names. Mock the network at the boundary (MSW), not internal modules.
- Cover: renders correctly, user interactions, loading/error/empty states, validation messages, permission-dependent UI.
- E2E (Playwright/Cypress) for critical journeys only; keep deterministic (no fixed sleeps).
- Bug fix: failing test first.

## 10. Build/deploy notes
- Build once; configuration injected at deploy (runtime config or env at build per repo practice). Hashed asset filenames + caching headers; SPA fallback routing on the server/CDN.
- Verify: `lint`, `typecheck` (`tsc --noEmit`), `test`, `build` all pass.

## 11. Frontend review checklist
- [ ] Matches contract; no guessed fields
- [ ] Loading/empty/error/success handled
- [ ] No `any`, no disabled lint rules, no console logs
- [ ] Accessible (keyboard, labels, semantics)
- [ ] No secrets/PII in client; no unsafe HTML
- [ ] Reuses existing components/patterns; no unneeded deps
- [ ] Tests added and behavior-focused
- [ ] No performance regressions (bundle size, re-renders, list sizes)
