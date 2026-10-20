# Test-Driven Development (red -> green -> refactor)

**Iron rule**: no production code without a failing test that demands it. If code was written first, discard it and start from the test (keep it only as reference).

## Cycle
1. **RED** - write one small test for the next behavior. Run it. Confirm it fails **for the right reason** (missing behavior, not a typo or setup error).
2. **GREEN** - write the minimum code to pass. No extras, no "while I'm here".
3. **REFACTOR** - clean names/duplication with tests green. Re-run after each step.
4. Commit. Repeat.

## Bug fixes
Reproduce with a failing test first; the fix is done only when that test passes and the suite is green.

## Test quality rules
- Test behavior through the public surface; assert outcomes, not internals.
- One behavior per test; descriptive names; deterministic (control time, randomness, network).
- Mock only true boundaries. Never assert on a mock's own existence or add test-only methods to production classes.
- A test you never saw fail proves nothing; a test that can't fail is worthless.
- Avoid snapshot sprawl; avoid tests coupled to CSS classes, private methods, or call order.

## Stack notes
- **.NET**: xUnit; unit-test services/handlers; integration-test endpoints with `WebApplicationFactory` and a real DB (Testcontainers); fake time with `TimeProvider`.
- **React**: Vitest/Jest + Testing Library; query by role/label; mock the network with MSW; test loading, empty, error, success.

## Allowed exceptions (declare them in the report)
Throwaway spikes (delete afterward), generated code, pure configuration, trivial markup with no logic. Everything else follows the cycle.

## Red flags you are cheating
"I'll add tests after", tests written to match the code you already have, tests deleted or skipped to get green, coverage chasing with assertion-free tests.
