# Verification gate (evidence before claims)

**Rule**: never say "done", "fixed", "passing", or "works" unless you ran the proving command **in this session, after your last change**, and read the output.

## Claim -> required evidence
| Claim | Evidence |
|---|---|
| Tests pass | full relevant test command output, 0 failures |
| Build succeeds | build command output, exit 0 |
| Bug fixed | the original repro now passes AND a regression test fails without the fix |
| Lint/types clean | linter and typecheck output |
| Feature works in UI | E2E run or manual steps with observed result (screenshot/trace) |
| Migration safe | up/down/up run output + row-count checks |
| Performance improved | before/after measurements, same method |
| Delegated agent finished | you inspected their diff and re-ran the checks yourself |

## Red-flag wording (stop and verify instead)
"should work", "probably", "I believe", "looks correct", "seems fine", "the agent said it passed".

## Procedure before reporting
1. Re-run `scripts/verify.sh` (and targeted tests) on the final state.
2. Re-run `scripts/scope_check.py` for your allowed paths.
3. Fill the change report with real commands and outcomes. Put anything unverified under NOT VERIFIED.
4. Run `python scripts/check_report.py <report>`; fix what it flags.

## Partial success
Report exactly what passed and what did not. A failing check that pre-dates your change is reported as baseline, not hidden.

## Re-verify after
Merges/rebases, conflict resolutions, dependency changes, generated-code refreshes, and any "small last-minute edit".
