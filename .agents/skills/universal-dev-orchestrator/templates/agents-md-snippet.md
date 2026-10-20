## Engineering workflow (add to your repo's AGENTS.md)

- Use the `universal-dev-orchestrator` skill for all code, SQL, QA, and deployment work.
- Make the smallest correct change; follow existing conventions; do not reformat or refactor unrelated code.
- Before finishing: run `scripts/verify.sh` and `scripts/scope_check.py`; include evidence in the report.
- Never delete/skip tests to pass, run destructive SQL, force-push, or deploy to production without explicit approval.
- Multi-agent runs: work only in your assigned worktree and allowed paths; coordinate via `.agent/`.
- UI tasks with a Figma link: read design data via the Figma MCP, reuse existing components and tokens, implement all states, and attach design-vs-app screenshots.
- Final response format: RESULT / SUMMARY / FILES / VERIFIED / NOT VERIFIED / RISKS / ROLLBACK.
