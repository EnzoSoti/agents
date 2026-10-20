import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def create_pdf(output_path="docs/instructions.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F1F5F9'),
        spaceBefore=4,
        spaceAfter=6,
        leftIndent=8,
        rightIndent=8
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("@enzosoti/agents — Installation & Usage Guide", title_style))
    story.append(Paragraph("A drop-in modular AI agent framework & skills package for software engineering teams", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # Section 1: Overview
    story.append(Paragraph("1. Overview", h1_style))
    story.append(Paragraph(
        "<b>@enzosoti/agents</b> provides an automated distribution mechanism for engineering agent skills. "
        "When installed via npm, the embedded <code>.agents/</code> directory is automatically placed into the "
        "root of the target repository, allowing AI coding assistants (Antigravity, Cursor, Claude, Copilot) "
        "to immediately leverage architectural blueprints, review checklists, and TDD playbooks.",
        body_style
    ))

    # Section 2: Installation Options
    story.append(Paragraph("2. How to Install", h1_style))
    story.append(Paragraph("<b>Option A: Install Directly from GitHub (Recommended for Teams)</b>", body_style))
    story.append(Paragraph("<code>npm install https://github.com/EnzoSoti/agents.git --save-dev</code>", code_style))

    story.append(Paragraph("<b>Option B: Use via npx without adding to package.json</b>", body_style))
    story.append(Paragraph("<code>npx https://github.com/EnzoSoti/agents.git</code>", code_style))

    story.append(Paragraph("<b>Option C: Install from npm Registry</b>", body_style))
    story.append(Paragraph("<code>npm install @enzosoti/agents --save-dev</code>", code_style))

    # Section 3: CLI & Selective Installation
    story.append(Paragraph("3. CLI Commands & Selective Installation", h1_style))
    story.append(Paragraph(
        "You can manage, inspect, or install specific skills selectively rather than copying the entire library:",
        body_style
    ))

    cli_examples = """# List all 20 available skills with indexing
npx agents list

# Install specific skill(s) only
npx agents add tdd bug-hunter
npx agents add ui-ux-pro-max ui-styling

# Full synchronization of all skills
npx agents install --all

# Generate IDE pointer files (.cursorrules, CLAUDE.md)
npx agents link
npx agents link --cursor
npx agents link --claude

# Force overwrite modified files in target project
npx agents install --force"""
    story.append(Paragraph("<pre>" + cli_examples.replace('\n', '<br/>') + "</pre>", code_style))

    # Section 4: Architecture & Copy Engine
    story.append(Paragraph("4. How the Auto-Install Engine Works", h1_style))
    story.append(Paragraph(
        "Installation executes <code>bin/install.js</code> via the npm <code>postinstall</code> lifecycle hook:<br/>"
        "• <b>Host Discovery:</b> Checks <code>INIT_CWD</code> (populated by npm/yarn/pnpm) and parent directories to find project root.<br/>"
        "• <b>Safety Guard:</b> Non-destructive by default during automated npm installs to avoid erasing developer modifications.<br/>"
        "• <b>Self-Copy Prevention:</b> Detects when executed inside the source repository and prevents circular copies.",
        body_style
    ))

    story.append(PageBreak())

    # Section 5: Skills Catalog
    story.append(Paragraph("5. Complete Skills Catalog (20 Built-in Skills)", h1_style))
    story.append(Paragraph("The package includes 20 specialized skill engines covering the software lifecycle:", body_style))

    skills_data = [
        [
            Paragraph("Skill Name", table_header_style),
            Paragraph("Domain / Category", table_header_style),
            Paragraph("Core Functionality", table_header_style)
        ],
        [
            Paragraph("<b>universal-dev-orchestrator</b>", table_cell_style),
            Paragraph("Orchestration", table_cell_style),
            Paragraph("Idea-to-production operating system: spec, vertical slicing, TDD, review gates, multi-agent protocol.", table_cell_style)
        ],
        [
            Paragraph("<b>codebase-audit-pre-push</b>", table_cell_style),
            Paragraph("QA & Security", table_cell_style),
            Paragraph("Deep pre-push scan: removes junk files, dead code, secrets, and checks release health.", table_cell_style)
        ],
        [
            Paragraph("<b>poka-yoke</b>", table_cell_style),
            Paragraph("Engineering Safety", table_cell_style),
            Paragraph("Mistake-proofing patterns: self-announcing errors, URL deduplication, defensive contracts.", table_cell_style)
        ],
        [
            Paragraph("<b>diagnosing-bugs</b>", table_cell_style),
            Paragraph("Debugging", table_cell_style),
            Paragraph("Systematic root-cause isolation loop for complex regressions, race conditions, and faults.", table_cell_style)
        ],
        [
            Paragraph("<b>bug-hunter</b>", table_cell_style),
            Paragraph("Debugging", table_cell_style),
            Paragraph("Methodical defect discovery, stack trace inspection, patch construction, and regression guards.", table_cell_style)
        ],
        [
            Paragraph("<b>five-axis-code-review</b>", table_cell_style),
            Paragraph("Code Review", table_cell_style),
            Paragraph("Five dimensions: Correctness, Security, Readability, Performance, Test Coverage.", table_cell_style)
        ],
        [
            Paragraph("<b>tdd</b>", table_cell_style),
            Paragraph("Testing", table_cell_style),
            Paragraph("Test-Driven Development methodology: red-green-refactor, mocking strategies, unit & integration tests.", table_cell_style)
        ],
        [
            Paragraph("<b>performance-optimizer</b>", table_cell_style),
            Paragraph("Optimization", table_cell_style),
            Paragraph("Bottleneck profiling, payload compression, bundle chunking, query cache tuning.", table_cell_style)
        ],
        [
            Paragraph("<b>api-endpoint-builder</b>", table_cell_style),
            Paragraph("Backend", table_cell_style),
            Paragraph("Production REST endpoints with validation schemas, RBAC auth, structured error responses.", table_cell_style)
        ],
        [
            Paragraph("<b>ui-ux-pro-max</b>", table_cell_style),
            Paragraph("UI/UX Design", table_cell_style),
            Paragraph("79 searchable styles, 192 product palettes, 74 font pairings, 119 usability heuristics.", table_cell_style)
        ],
        [
            Paragraph("<b>ui-styling</b>", table_cell_style),
            Paragraph("UI Components", table_cell_style),
            Paragraph("Tailwind CSS utility patterns, Radix/shadcn inspired components, dark mode theming.", table_cell_style)
        ],
        [
            Paragraph("<b>design-system</b>", table_cell_style),
            Paragraph("Design System", table_cell_style),
            Paragraph("3-tier token architecture (primitive -> semantic -> component), CSS vars, slide generation.", table_cell_style)
        ],
        [
            Paragraph("<b>brand</b>", table_cell_style),
            Paragraph("Branding", table_cell_style),
            Paragraph("Visual identity compliance, tone of voice, messaging frameworks, asset governance.", table_cell_style)
        ],
        [
            Paragraph("<b>banner-design</b>", table_cell_style),
            Paragraph("Creative Assets", table_cell_style),
            Paragraph("Social media, marketing ads, and web hero graphics with 22 aesthetic styles.", table_cell_style)
        ],
        [
            Paragraph("<b>design</b>", table_cell_style),
            Paragraph("Creative Assets", table_cell_style),
            Paragraph("Logo generation, Corporate Identity Programs (CIP), slide decks, vector graphics.", table_cell_style)
        ],
        [
            Paragraph("<b>slides</b>", table_cell_style),
            Paragraph("Presentations", table_cell_style),
            Paragraph("Strategic executive HTML slide decks with embedded Chart.js and token styling.", table_cell_style)
        ],
        [
            Paragraph("<b>prototype</b>", table_cell_style),
            Paragraph("Prototyping", table_cell_style),
            Paragraph("Rapid throwaway prototyping for validating state logic and experimental interfaces.", table_cell_style)
        ],
        [
            Paragraph("<b>improve-codebase-architecture</b>", table_cell_style),
            Paragraph("Architecture", table_cell_style),
            Paragraph("Codebase deepening opportunities, seam analysis, coupling reduction, visual HTML reports.", table_cell_style)
        ],
        [
            Paragraph("<b>technical-change-tracker</b>", table_cell_style),
            Paragraph("Continuity", table_cell_style),
            Paragraph("Structured JSON change records, state machine tracking, cross-session AI handoffs.", table_cell_style)
        ],
        [
            Paragraph("<b>fct-app-v4</b>", table_cell_style),
            Paragraph("Architecture Map", table_cell_style),
            Paragraph("Full system map for FCT App: React 19, TypeScript, Power Apps Code App, module routes.", table_cell_style)
        ]
    ]

    t = Table(skills_data, colWidths=[1.8 * inch, 1.4 * inch, 4.0 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))

    story.append(t)
    story.append(Spacer(1, 14))

    # Section 6: Maintenance & Syncing
    story.append(Paragraph("6. Maintenance & Team Updates", h1_style))
    story.append(Paragraph(
        "To update the skills across any project consuming this package from GitHub, run:<br/>"
        "<code>npm update https://github.com/EnzoSoti/agents.git</code><br/>"
        "Or re-sync using npx:<br/>"
        "<code>npx https://github.com/EnzoSoti/agents.git install --force</code>",
        body_style
    ))

    doc.build(story)
    print(f"[SUCCESS] Generated instructions PDF: {output_path}")

if __name__ == '__main__':
    create_pdf()
