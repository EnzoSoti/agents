# `@enzosoti/agents`

A drop-in npm package for distributing and synchronizing AI agent skills, design tokens, workflows, and rules across repositories.

---

## 1. Overview

When you run `npm install` in any project, `@enzosoti/agents` automatically copies its `.agents/` folder into the root directory of that project.

### Target Project Structure After Install

```text
my-project/
├── .agents/
│   └── skills/
│       ├── api-endpoint-builder/
│       ├── bug-hunter/
│       ├── codebase-audit-pre-push/
│       ├── design-system/
│       ├── diagnosing-bugs/
│       ├── fct-app-v4/
│       ├── five-axis-code-review/
│       ├── performance-optimizer/
│       ├── poka-yoke/
│       ├── tdd/
│       ├── ui-styling/
│       ├── ui-ux-pro-max/
│       ├── universal-dev-orchestrator/
│       └── ...
├── node_modules/
├── package.json
└── ...
```

---

## 2. Installation Options

### Option A: Install Directly from GitHub (Ready Now)

In any target project:

```bash
npm install https://github.com/EnzoSoti/agents.git --save-dev
```

Or with `yarn` / `pnpm`:

```bash
yarn add https://github.com/EnzoSoti/agents.git --dev
# or
pnpm add -D https://github.com/EnzoSoti/agents.git
```

> **Note**: The `postinstall` hook runs automatically and copies `.agents/` directly into your host project root.

---

### Option B: Run via `npx` (No project dependency)

To sync or re-sync `.agents/` on demand:

```bash
npx https://github.com/EnzoSoti/agents.git
```

---

### Option C: Install from the npm Registry (After Publishing)

Once published to npm (see section 5):

```bash
npm install @enzosoti/agents --save-dev
```

You can also run it via binary command:

```bash
npx agents [command]
```

### CLI Commands & Selective Installation

You can use `npx agents` to manage, inspect, or selectively install skills:

```bash
# List all 20 available skills
npx agents list

# Install specific skill(s) only
npx agents add tdd bug-hunter
npx agents add ui-ux-pro-max ui-styling

# Install or sync all skills
npx agents install --all

# Generate IDE pointer files (.cursorrules, CLAUDE.md)
npx agents link
npx agents link --cursor
npx agents link --claude

# Force overwrite existing files if modified
npx agents install --force
```

---

## Safety & Non-Destructive Merging

- **Safe postinstall**: Automatic `npm install` respects existing project files and does not overwrite modifications unless `--force` is passed.
- **Root detection**: Accurately locates host project root via `INIT_CWD` and nested `node_modules` inspection.

---

## 3. How the Auto-Install Engine Works

The installation is driven by `bin/install.js` via the npm `postinstall` hook.

### Root Detection Hierarchy

1. **`process.env.INIT_CWD`**: Set by `npm`, `yarn`, and `pnpm` to point to the directory where the user ran the command.
2. **`node_modules` Resolution**: If executed from inside `node_modules/@enzosoti/agents/bin/`, it traverses up to the directory containing `node_modules/`.
3. **`process.cwd()`**: Fallback directory.
4. **Self-Copy Prevention**: If source and destination directories resolve to the exact same path (e.g. running inside the package's own repo), it safely skips copying.

---

## 4. Skills Catalog

| Skill | Category | Description |
|---|---|---|
| **`universal-dev-orchestrator`** | Orchestration | Universal software-engineering operating system: spec, vertical slicing, TDD, multi-agent coordination, verification gates. |
| **`codebase-audit-pre-push`** | QA & Security | Deep audit before push: eliminates junk files, dead code, exposed tokens, formatting anomalies. |
| **`poka-yoke`** | Engineering Safety | Mistake-proofing principles: deduplication of URLs, defensive payload sanitization, self-announcing errors. |
| **`diagnosing-bugs`** | Debugging | Systematic root-cause isolation loop for complex regressions and race conditions. |
| **`bug-hunter`** | Debugging | Defect identification, trace analysis, patch creation, and regression tests. |
| **`five-axis-code-review`** | Code Review | Five-axis checklist: Correctness, Security, Readability, Performance, Test Coverage. |
| **`tdd`** | Testing | Test-driven development methodology: red-green-refactor cycles, mocking, and coverage. |
| **`performance-optimizer`** | Performance | Bottleneck profiling, payload size reduction, bundle chunking, and cache optimization. |
| **`api-endpoint-builder`** | Backend | REST API design with validation, error handling, RBAC, and OpenAPI standards. |
| **`ui-ux-pro-max`** | UI/UX | 79 design styles, 192 product palettes, 74 font pairings, 119 UX guidelines. |
| **`ui-styling`** | UI/UX | Tailwind CSS patterns, accessible components (Radix/shadcn inspired), responsive layouts. |
| **`design-system`** | Design System | Three-layer design tokens (primitive → semantic → component), CSS variables, slide generation. |
| **`brand`** | Brand Identity | Brand voice, messaging frameworks, asset management, and style compliance. |
| **`banner-design`** | Creative Assets | Social media, web hero, and display ad banners across 22 styles. |
| **`design`** | Creative Assets | Logo generation, corporate identity programs (CIP), HTML slides, vector graphics. |
| **`slides`** | Presentations | Strategic HTML presentations with Chart.js, responsive layouts, and executive summaries. |
| **`prototype`** | Prototyping | Fast throwaway prototyping for validating state logic and experimental UI components. |
| **`improve-codebase-architecture`** | Architecture | Architecture seam analysis, decoupling, and visual HTML architecture reports. |
| **`technical-change-tracker`** | Session Continuity | Structured JSON change records and AI session handoffs for multi-bot continuity. |
| **`fct-app-v4`** | Domain Architecture | Complete architecture map, module routes, and real-time state conventions for FCT App. |

---

## 5. Publishing to npm (Optional)

If you wish to allow `npm install @enzosoti/agents` without requiring the GitHub URL:

1. **Log in to npm**:
   ```bash
   npm login
   ```

2. **Publish the package**:
   ```bash
   npm publish --access public
   ```

---

## 6. Updating Skills & Pushing Changes

### For Consumers / Target Projects
To pull the latest skills and prompt updates into your project, choose any of the following:

```bash
# Method 1: Standard npm update (automatically runs postinstall copy)
npm update https://github.com/EnzoSoti/agents.git

# Method 2: Via npx update command
npx https://github.com/EnzoSoti/agents.git update

# Method 3: Force overwrite with latest GitHub main branch
npx agents install --force
```

### For Maintainers
When you make changes or add new skills inside `.agents/`:

1. Update the documentation & PDF:
   ```bash
   npm run docs
   ```
2. Commit and push:
   ```bash
   git add .
   git commit -m "feat: describe updates"
   git push origin main
   ```
