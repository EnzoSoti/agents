# Figma design-to-code (React)

Goal: build UI that matches the design **and** fits the existing codebase, using real design data, not guesses from screenshots.

## 0. Connect Figma (one-time, per machine)
Figma publishes an official MCP server. As of the sources in `SOURCES.md`:
- **Remote (recommended)**: `codex mcp add figma --url https://mcp.figma.com/mcp`, then complete the OAuth sign-in when prompted.
- **Desktop app server** (alternative): runs locally, e.g. `http://127.0.0.1:3845/mcp`; reported to need a Dev or Full seat on a paid Figma plan.
- Verify: ask Codex to list the tools from the `figma` MCP server. **Tool names and limits change; trust that listing, not this file.**
- Access, rate limits, and Code Connect availability depend on your Figma plan and seat. Check your plan before relying on it.
- An official Figma skill for Codex also exists (see `SOURCES.md`); you can install it alongside this skill.
If MCP is unavailable, fall back to the **manual handoff** in section 6.

## 1. Inputs the brief must contain (see `templates/design-handoff.md`)
Figma file/frame link or node id; which screens and states; viewport targets; target route/component path; which existing components to reuse; any copy/i18n keys; the API endpoints each screen uses.

## 2. Procedure
1. **Read the design data** (hierarchy, auto-layout, variables, component instances, Code Connect mappings if present) and a **screenshot** of each frame for visual reference.
2. **Inventory what exists in code first**: design-system components, theme/tokens, icon set, layout primitives, existing similar screens. Search before creating.
3. **Map design -> code**:
   - Figma variables/styles -> the project's tokens/theme (CSS variables, Tailwind config, MUI theme...). Never hardcode hex values, px sizes, or fonts that a token already represents. If a needed token does not exist, propose adding it; don't scatter literals.
   - Figma component instances -> existing React components (via Code Connect mappings when available). Create a new component only if no existing one fits, and put it where the repo keeps shared components.
   - Auto-layout -> flex/grid with the repo's spacing scale; constraints -> responsive rules.
4. **Plan states**: default, hover, focus, active, disabled, loading, empty, error, success, long text, and each breakpoint. If the design omits a state, list it as a question; don't invent silently.
5. **Implement in slices** (one screen/section at a time) following `03-tdd.md` for logic; use component tests for behavior and E2E for the journey.
6. **Wire data to the API contract** (`openapi`): real field names and error shapes. Don't hardcode design-sample data into production code.
7. **Compare to the design** (section 4), fix differences, then `verify.sh frontend` and the E2E run.

## 3. Rules
- Treat tool-generated code as a **draft to adapt**, not final output: convert to the repo's framework, styling system, naming, and patterns.
- Reuse over reinvent; tokens over literals; semantic HTML over div soup; accessible names and keyboard behavior even if the design doesn't show them.
- Assets: use the project's asset pipeline; export from Figma through the tool's asset handling, not by hotlinking temporary URLs. Optimize images; prefer SVG for icons through the existing icon approach.
- Don't change the design silently. If code constraints, accessibility, or the API contradict the design, report it (handoff to the orchestrator/designer) with evidence.
- Pixel-perfect is not the target; **faithful to tokens, layout, hierarchy, and states** is. Document accepted deviations.

## 4. Design-fidelity check (add to review Stage 1)
Compare the running UI to the frame at each target viewport:
- [ ] Layout, spacing, alignment, and hierarchy match
- [ ] Typography (family, size, weight, line height) and colors come from tokens
- [ ] All specified states implemented and visually correct
- [ ] Responsive behavior at the agreed breakpoints
- [ ] Icons, images, and assets correct and optimized
- [ ] Contrast, focus visibility, keyboard flow, labels checked
- [ ] Uses existing components; no duplicated near-copies
- [ ] Deviations listed with reasons
Capture evidence: side-by-side screenshots (design frame vs. app) at each viewport, attached to the change report. Optional automation: Playwright screenshot assertions or visual-regression for stable, high-value screens only.

## 5. AGENTS.md block to add
```
## Figma
- When a task includes a Figma link, read design data via the Figma MCP server before coding.
- Reuse existing components and design tokens; do not hardcode colors, spacing, or fonts.
- Implement all states in the design; list missing states as questions.
- Attach design-vs-implementation screenshots to the change report.
```

## 6. Manual handoff (no MCP)
Ask for: exported frames (PNG) per state and breakpoint, the token list (colors, type scale, spacing, radii, shadows), component list with names, and redlines for tricky areas. Build from these, and state in the report that fidelity was checked against exports, not live design data.

## 7. Common failures
Guessing values from a screenshot; duplicating components that already exist; hardcoded colors; missing empty/error/loading states; desktop-only layout; leaving sample data in the UI; building the whole page in one giant component; skipping the visual comparison.
