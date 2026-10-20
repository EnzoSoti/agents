# Agents & Skills Package

A modular collection of AI agent skills, rules, and engineering workflows that automatically installs into your project's `.agents` directory.

## Installation

### Option 1: Direct from GitHub

You can install this package directly into any project using npm:

```bash
npm install https://github.com/EnzoSoti/agents.git --save-dev
```

Or run via npx:

```bash
npx https://github.com/EnzoSoti/agents.git
```

### Option 2: From npm (if published)

```bash
npm install @enzosoti/agents --save-dev
```

## How It Works

When `npm install` runs, a `postinstall` script automatically detects your project root and copies the `.agents/` folder directly into your project:

```
your-project/
├── .agents/
│   └── skills/
│       ├── api-endpoint-builder/
│       ├── bug-hunter/
│       ├── design-system/
│       ├── ui-ux-pro-max/
│       ├── universal-dev-orchestrator/
│       └── ...
├── package.json
└── ...
```

You can also run the binary manually at any time to re-sync or update:

```bash
npx agents
```

## Included Skills

- **`universal-dev-orchestrator`**: Universal engineering operating system covering specification, planning, TDD, verification gates, two-stage review, and multi-agent coordination.
- **`codebase-audit-pre-push`**: Deep audit before GitHub push: eliminates junk files, dead code, secrets.
- **`poka-yoke`**: Mistake-proofing principles and defensive conventions.
- **`diagnosing-bugs`** & **`bug-hunter`**: Systematic root cause isolation and defect resolution.
- **`five-axis-code-review`**: Rigorous code review checklist.
- **`tdd`**: Test-driven development methodology.
- **`performance-optimizer`**: Bottleneck profiling, payload size reduction, bundle chunking.
- **`api-endpoint-builder`**: REST API endpoint design with validation, error formatting, RBAC.
- **`ui-ux-pro-max`** & **`ui-styling`**: Comprehensive UI/UX design intelligence and component styling.
- **`design-system`**, **`brand`**, **`banner-design`**, **`design`**, **`slides`**: Design assets and token management.
- **`fct-app-v4`**: FCT App architecture map and conventions.
- **`technical-change-tracker`**: Structured change tracking and cross-session bot handoffs.

## License

MIT
