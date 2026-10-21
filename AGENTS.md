# AI Agents Operating Rules & Guidelines

Welcome to the codebase. When working on this repository, every AI agent must strictly follow the operational rules, quality gates, and folder landing policies outlined below.

---

## Rule 1: Prime Directives
1. **Understand Before Editing**: Read the relevant code, tests, and documentation before editing. Never change code you have not inspected.
2. **Smallest Correct Change**: Focus strictly on the assigned task without unsolicited refactoring or out-of-scope adjustments.
3. **Evidence Over Assumption**: Back every claim with test outputs, compiler checks, or file/line references.
4. **Follow Repository Conventions**: Align with existing style, formatting, naming conventions, and design tokens.

---

## Rule 2: Technical Skills Inventory
Agent capabilities and operational playbooks are maintained in `.agents/skills/`. Key skills include:
- `universal-dev-orchestrator`: End-to-end engineering pipeline, TDD, two-stage review, and verification gates.
- `fct-app-v4`: Authoritative architecture map, routing, state synchronization, and permission hierarchy.
- `codebase-audit-pre-push`: Pre-push hygiene, secret screening, and dead file removal.
- `poka-yoke`: Mistake-proofing conventions and defensive assertions.
- `ui-ux-pro-max` & `ui-styling`: Design systems, token conventions, and responsive components.

---

## Rule 3: Verification & Quality Gates
Before declaring any task complete:
1. Verify TypeScript types and compilation: `npm run build` or `npx tsc --noEmit`.
2. Run test suites associated with modified modules.
3. Run `npm run docs` if documentation or instructions were updated.

---

## Rule 4: Strict Document & Markdown Landing Policy

Every AI agent working in this project is explicitly instructed to **consult the directory taxonomy map first** whenever creating, generating, or updating any `.md` or `.docx`/`.doc` file.

### 🗺️ The Mandatory Landing Lookup Table

Whenever an agent creates or modifies a file, it must strictly land in its assigned location:

| Target File Type | Mandatory Landing Directory |
|---|---|
| **End-User Manuals & SOP Guides (.docx)** | `docs/01-user-manuals/` |
| **UAT Test Matrices & Acceptance Sign-Offs (.docx, .md)** | `docs/02-testing-and-uat/` |
| **System & Module Architecture Specs (.docx)** | `docs/03-system-specifications/` |
| **Workflow & Return/Disapproval Guides (.md)** | `docs/04-workflow-and-feature-guides/` |
| **SharePoint & External Integration Contracts (.md)** | `docs/05-integration-and-api-specs/` |
| **Developer Handbooks, Tokens & Screenshot Guides (.md)** | `docs/06-developer-guides/` |
| **Release Notes & Sprint Deployment Logs (.md)** | `docs/07-sprints-and-releases/` |
| **Formal Backend Change Requests (BR-xxx-*.md)** | `backend-requests/` |
| **Design System Specs & Component Catalogs (.md)** | `design-system/fct-app-v4/` |
| **Dev Server, Proxy & Middleware Scripts** | `scripts/01-dev-server/` |
| **Automated Test Runners & E2E Validation Scripts** | `scripts/02-testing/` |
| **Doc Builders & Word Generator Scripts** | `scripts/03-doc-generators/` |
| **Screenshot Capture & Annotation Automation Scripts** | `scripts/04-screenshot-automation/` |

### 🚫 Non-Negotiable Rules Enforced on Agents:
1. **Never Save Loose Files in Project Root**: Only `AGENTS.md` and standard project configs (`package.json`, `README.md`, `.gitignore`) are permitted in root. No loose `.md` or `.docx` files.
2. **Never Save Loose Files in `docs/` Root**: Only `docs/README.md` and `docs/instructions.pdf` are permitted directly under `docs/`.
3. **Mandatory Indexing**: Any newly created or renamed document must immediately be indexed and linked in `docs/README.md` or `scripts/README.md`.
