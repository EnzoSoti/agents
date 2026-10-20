# Browser / End-to-End testing (React + .NET)

**Why**: compiling and unit tests do not prove a user can complete a journey. Verify through a real browser against the running stack.

## What to cover (few, critical journeys)
Sign in/out, the main create-read-update-delete flow, a permission-denied case, a validation error shown from a server 400, a server failure (500/timeout) state, and the primary revenue/critical path.

## Setup pattern (Playwright example - adapt to the repo's existing tool)
- Start backend + frontend (or point to staging) via the runner's `webServer`/compose config; seed a known test database/state per run.
- Reuse authenticated state (storage state) instead of logging in on every test.
- Locate by **role, label, text** (`getByRole`, `getByLabel`); avoid brittle CSS/XPath.
- Wait on conditions (`expect(...).toBeVisible()`), never fixed sleeps.
- Collect traces, screenshots, and videos on failure; fail on unexpected `console.error` and uncaught page errors.
- Isolate tests; create their own data; clean up.
- Run in CI headless; keep the suite small and fast; retries only to **detect** flakiness, never to hide it.

```ts
// frontend/e2e/orders.spec.ts (illustrative)
import { test, expect } from '@playwright/test';
test('user can create an order', async ({ page }) => {
  await page.goto('/orders/new');
  await page.getByLabel('Customer').fill('Acme');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByRole('status')).toHaveText(/order created/i);
});
```

## Smoke subset for deployment
Health endpoint 200, home page renders, login works, one read and one write through the API, no console errors. Run after every deploy (`08-ship-checklist.md`).

## Debugging E2E failures
Open the trace; check network calls and responses first (is it the API or the UI?); reproduce locally; fix root cause. Don't increase timeouts as the fix.
