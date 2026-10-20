# Two-stage review

Review in this order. Do not discuss style while the change still fails the spec.

## Stage 1 - Spec compliance
Compare diff to the brief/spec only:
- Every acceptance criterion implemented? (point to code/test for each)
- Anything built that was **not** requested (scope creep)? Anything requested but missing?
- Contract preserved? Allowed paths respected (`scope_check.py`)?
- UI work with a Figma source: run the design-fidelity check in `09-figma-design-to-code.md` section 4.
Verdict: COMPLIANT / GAPS (list). Fix gaps before Stage 2.

## Stage 2 - Code quality (five axes)
1. **Correctness**: logic, edge cases, error handling, concurrency, data integrity
2. **Readability**: naming, structure, comments explain why, consistent with repo
3. **Architecture**: layering, coupling, reuse, no premature abstraction
4. **Security**: authN/authZ, input validation, secrets, injection, data exposure
5. **Performance**: N+1, unbounded queries/lists, needless renders, blocking calls
Classify findings BLOCKER / MAJOR / MINOR / QUESTION (see `references/04`).

## Requesting a review (author)
Give the reviewer: the brief, the exact diff range, how to run the checks, what you are unsure about, and what is out of scope. A review without context is guesswork.

## Receiving a review (author)
- Verify each finding technically before changing code; the reviewer can be wrong.
- Fix BLOCKER/MAJOR; for disagreements, answer with evidence (test, benchmark, doc), not opinion.
- No performative agreement and no silent ignoring. Respond to every finding.
- Re-run verification after fixes; request re-review of changed areas.

## Change size
Prefer small PRs. If a diff is too large to review confidently, split it before reviewing.
