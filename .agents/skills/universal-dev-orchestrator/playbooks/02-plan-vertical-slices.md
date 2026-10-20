# Plan in small vertical slices

**Principle**: build thin end-to-end increments that each work and are verifiable, not big horizontal layers that only work when everything is finished.

## Rules
- A slice delivers one user-visible behavior (UI -> API -> DB) or one contract/schema step. Target: reviewable in one sitting (roughly <= 5 files, <= 300 changed lines).
- Order by **risk and dependency**: walking skeleton -> riskiest unknown -> core flow -> edge cases -> polish.
- Every slice states: goal, exact file paths, the **test to write first**, the command that proves it, and rollback.
- Mark slices that are file-disjoint so they can run on parallel agents; serialize anything touching shared files.
- Re-plan when reality contradicts the plan; don't push through a broken assumption.

## Slice card (add to the brief)
```
Slice: S-03 "User can reset password"
Files: backend/src/Auth/ResetPassword*.cs, frontend/src/features/auth/ResetPassword*.tsx
Test first: ResetPasswordEndpoint returns 204 and invalidates old token; UI shows success state
Verify: dotnet test --filter ResetPassword ; npm test -- ResetPassword ; E2E: auth/reset.spec.ts
Depends on: S-01 (email service contract)
Risk: medium (auth)   Rollback: revert commit; feature flag reset_password=off
```

## Anti-patterns
"Phase 1: all DB, Phase 2: all API, Phase 3: all UI"; slices with no verification command; plans that name no files; hidden dependencies between parallel slices.
