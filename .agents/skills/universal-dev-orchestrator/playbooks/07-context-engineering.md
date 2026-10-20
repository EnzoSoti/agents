# Context engineering for agents

Quality of output tracks quality of context. Give each agent exactly what it needs, no more.

- **Keep `AGENTS.md` short and operational**: build/test commands, conventions, forbidden actions, where things live. Link to deeper docs instead of pasting them.
- **Per-task context pack** in the brief: goal, acceptance criteria, relevant file paths, contract excerpts, examples of the pattern to copy, constraints. Not the whole chat history.
- **Fresh agent per task** for implementation: avoids accumulated confusion; the handoff file is the memory.
- **Point, don't paste**: reference file paths and line ranges; let the agent read them.
- **Load skills progressively**: SKILL.md first, then only the playbook/reference the task needs.
- **Summarize long threads** into a decision log (`.agent/status.md`) before continuing; drop stale assumptions.
- **State what is true vs assumed**; when context conflicts with code, trust the code and report the discrepancy.
- **Checkpoint**: commit often, so a restarted agent resumes from a known state.
- **Prefer examples**: one real file showing the desired pattern beats a paragraph of description.
