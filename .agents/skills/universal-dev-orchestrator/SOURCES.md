# Sources and attribution

The playbooks in `playbooks/` are **original write-ups** of widely shared agent-skill methods. No third-party skill text was copied. Install the originals if you want their exact wording, scripts, or slash commands. Verify each project's current license before redistributing.

| Playbook | Method (what top-ranked skills do) | Where it is popular | License noted by their READMEs |
|---|---|---|---|
| 01 spec-interview | design/spec before code, one question at a time | obra/superpowers (brainstorming), addyosmani/agent-skills (spec-driven-development, interview-me), "grill me"-style skills | MIT |
| 02 plan-vertical-slices | small verifiable tasks with exact files and checks | superpowers (writing-plans), addyosmani/agent-skills (planning-and-task-breakdown, incremental-implementation) | MIT |
| 03 tdd | red-green-refactor, tests first, anti-patterns | superpowers (test-driven-development), mattpocock/skills (tdd), Hermes agent | MIT (superpowers, Hermes) |
| 04 verification-gate | evidence before completion claims | superpowers (verification-before-completion), truth-first style skills | MIT |
| 05 browser-e2e | verify real user flows in a browser | addyosmani/agent-skills (browser-testing-with-devtools), vercel-labs/agent-browser, Playwright-based skills | varies |
| 06 two-stage-review | spec compliance then quality; five-axis review | superpowers (subagent-driven-development, requesting-code-review), addyosmani/agent-skills (code-review-and-quality) | MIT |
| 07 context-engineering | right context, fresh agent per task | addyosmani/agent-skills (context-engineering), superpowers | MIT |
| 08 ship-checklist | git workflow, finishing a branch, pre-launch | addyosmani/agent-skills (git workflow, CI/CD, pre-launch), superpowers (finishing-a-development-branch) | MIT |
| 09 figma-design-to-code | read real design data (hierarchy, variables, Code Connect), reuse components/tokens, verify against the frame | Figma's official MCP server docs (developers.figma.com), Figma/OpenAI Codex integration write-ups, the OpenAI `figma` skill listing, community plugins (e.g. Anima MCP, figma-bridge-mcp) | per project; check each license before reuse |
| orchestration additions | parallel dispatch, worktrees, subagent loops | superpowers (dispatching-parallel-agents, using-git-worktrees) | MIT |

## Why these were chosen
Independent 2026 roundups and install-count leaderboards (e.g. skills.sh-based rankings, aiskill.market, composio, pinggy, claudeskills.info) repeatedly place the same families at the top: TDD, systematic debugging, code review, browser testing, plan-before-code, and subagent/worktree workflows. Install counts are a popularity signal, not proof of quality, and the figures differ between sites.

## Figma notes
Setup commands (`codex mcp add figma --url https://mcp.figma.com/mcp`, optional desktop server at `127.0.0.1:3845/mcp`) come from Figma's docs and third-party guides found in search; the desktop server was reported to need a paid Dev/Full seat. Tool names, rate limits and plan requirements may have changed; confirm in Figma's current docs. Third-party Figma MCP servers (Anima, figma-bridge) were seen but not evaluated or included.

## Not included (and why)
Vendor-specific skills (Azure, Convex, Clerk, GSAP, etc.), Obsidian/Notion/e-commerce skills, and the OpenAI `openai/skills` catalog items: not relevant to a React + .NET build, or the catalog is marked deprecated in favor of the OpenAI plugins repo. Add any you need as separate skills.

## Honest limits
No skill set guarantees success. These raise the odds by forcing specs, tests, evidence, review, and safe release. Outcomes still depend on the quality of your requirements, tests, environment, and human approvals.
