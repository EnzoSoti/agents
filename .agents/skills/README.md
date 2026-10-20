# FCT App V4 - AI Agent Skills Directory

This directory contains the operational skills and domain knowledge bases available to AI agents working on the FCT App V4 codebase.

---

## Skills Catalog

| Skill Name | Category | Primary Focus & Capabilities |
|---|---|---|
| **[`fct-app-v4`](fct-app-v4/SKILL.md)** | `domain-architecture` | **Authoritative system map** for FCT App V4: React 19 + TypeScript + Vite, Power Apps Code App, module routes, real-time sync, production gateway, and full file inventory. |
| **[`universal-dev-orchestrator`](universal-dev-orchestrator/SKILL.md)** | `orchestration` | Universal engineering operating system covering specification, planning, TDD, verification gates, two-stage review, and multi-agent coordination. |
| **[`codebase-audit-pre-push`](codebase-audit-pre-push/SKILL.md)** | `quality-assurance` | Deep audit before GitHub push: eliminates junk files, dead code, secrets, and prepares production release. |
| **[`poka-yoke`](poka-yoke/SKILL.md)** | `engineering-safety` | Mistake-proofing principles: URL de-duplication, defensive payload sanitization, self-announcing errors, and compile-time boundaries. |
| **[`diagnosing-bugs`](diagnosing-bugs/SKILL.md)** | `debugging` | Systematic root-cause isolation loop for complex regressions, race conditions, and network failures. |
| **[`bug-hunter`](bug-hunter/SKILL.md)** | `debugging` | Methodical defect identification, trace analysis, patch creation, and regression prevention. |
| **[`five-axis-code-review`](five-axis-code-review/SKILL.md)** | `code-review` | Rigorous five-axis checklist: Correctness, Security, Readability, Performance, and Test Coverage. |
| **[`tdd`](tdd/SKILL.md)** | `testing` | Test-driven development methodology: red-green-refactor cycles, unit tests, and integration coverage. |
| **[`performance-optimizer`](performance-optimizer/SKILL.md)** | `optimization` | Bottleneck profiling, payload size reduction, bundle chunking, and TanStack query cache tuning. |
| **[`api-endpoint-builder`](api-endpoint-builder/SKILL.md)** | `backend-integration` | REST API endpoint design with validation, error formatting, RBAC authentication, and OpenAPI/Swagger alignment. |
| **[`ui-ux-pro-max`](ui-ux-pro-max/SKILL.md)** | `ui-ux-design` | Comprehensive UI/UX design intelligence: 79 design styles, 192 product palettes, 74 typography pairings, and 119 usability heuristics. |
| **[`ui-styling`](ui-styling/SKILL.md)** | `styling` | Tailwind CSS utility patterns, Radix/shadcn-inspired components, responsive grid layouts, and dark mode theming. |
| **[`design-system`](design-system/SKILL.md)** | `design-system` | Three-layer design tokens (primitive → semantic → component), CSS custom properties, and GSDC brand adherence. |
| **[`brand`](brand/SKILL.md)** | `branding` | GSDC Fleet visual identity, brand voice, asset management, and corporate consistency. |
| **[`banner-design`](banner-design/SKILL.md)** | `creative-assets` | Social media banners, hero graphics, and creative marketing layout generation. |
| **[`design`](design/SKILL.md)** | `creative-assets` | Comprehensive design toolkit: logo generation, CIP assets, presentation slides, and vector graphics. |
| **[`slides`](slides/SKILL.md)** | `presentations` | Strategic HTML slide decks with Chart.js visualizations, responsive tables, and executive summaries. |
| **[`prototype`](prototype/SKILL.md)** | `prototyping` | Rapid throwaway prototyping for validating state logic in terminal apps or experimenting with UI variants. |
| **[`improve-codebase-architecture`](improve-codebase-architecture/SKILL.md)** | `architecture` | Codebase deepening opportunities, seam analysis, coupling reduction, and visual HTML architecture reports. |
| **[`technical-change-tracker`](technical-change-tracker/SKILL.md)** | `session-continuity` | Structured JSON change records, state machine tracking, and cross-session bot handoffs. |

---

## Operating Guidelines for Agents

1. **Always Consult `fct-app-v4` First**: For any feature addition, bug fix, or backend change, verify routing, permissions, API base URLs, and file inventory in [`fct-app-v4/SKILL.md`](fct-app-v4/SKILL.md).
2. **Apply Poka-Yoke Defaults**: Ensure all API requests route through normalized endpoint builders that prevent path duplication (`/api/api/*`).
3. **Verify Build After Modifying Code**: Always execute `npx tsc --noEmit` and `npm run build` before concluding a task.
4. **Preserve Design Integrity**: Maintain solid, opaque cards (zero glassmorphism/blur) and ensure the calibrated GSDC background watermark remains visible across light and dark themes.
