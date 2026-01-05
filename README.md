# Praxis AI

**A governance framework that makes human intent durable enough to survive AI's speed.**

Praxis provides deterministic behavior resolution for AI-assisted work:

```
Domain + Stage + Privacy + Environment → Behavior
```

This means: given your project's domain (Code/Create/Write/Learn/Observe), current lifecycle stage, privacy level, and environment context, Praxis validates governance rules. It also provides domain-specific guidance to keep AI collaboration aligned with your intent.

Whether you're building software, creating art, writing documents, or learning skills—Praxis gives you lifecycle governance, domain-specific guidance, and the structure to maintain coherent intent as AI accelerates your output.

---

## The Problem

AI amplifies throughput, not coherence. You can now generate 10x faster—but you can't govern 10x faster. The bottleneck moved from production to intent-maintenance.

Without structure, AI collaboration becomes chasing your own tail at higher speed: rediscovering rejected ideas, drifting scope mid-stream, refining things that aren't defined yet.

## What Praxis Does

Praxis makes human intent durable enough to survive AI's speed.

Your capacity for intent-maintenance is fixed. AI volume is not. Praxis provides leverage—canonical decisions, explicit scope boundaries, and stage gates that let fixed human intent govern unbounded AI output.

---

## Core Concepts at a Glance

| Concept | What It Does |
|---------|--------------|
| **Lifecycle** | Nine stages from Capture to Close, with Formalize as the structural hinge |
| **Domains** | Five work types (Code, Create, Write, Learn, Observe) with specific artifacts |
| **Privacy** | Five levels that constrain how data flows, not just who sees it |
| **Opinions** | Domain-specific guidance that biases decisions without enforcing them |
| **Roles** | Twelve governance roles with clear decision rights and lifecycle responsibilities |
| **PKDP** | Risk-tiered pipeline for distilling raw input into validated knowledge |

---

## Philosophy

### Principles Guide — Contracts Bind — Formalize Arbitrates

No single artifact has universal authority.

- **Principles** are timeless and advisory; they bias decisions but are never enforced mechanically.
- **Formalization contracts** are context-specific and binding; they enable execution by freezing selected decisions.
- **Execution** is irreversible or costly to reverse; it must operate within the active contract.

Tension between principles and execution is intentional and necessary. Formalize is the explicit decision hinge where tradeoffs are made visible.

### The Three-Layer Model

Praxis separates what you believe from how you decide from how you execute.

```
Opinions  →  Governance  →  Execution
```

- **Opinions:** Domain-specific guidance that biases decisions. Advisory, never enforced mechanically.
- **Governance:** The mechanism by which conflicts are resolved. Procedural authority.
- **Execution:** The work itself. Governed by formalization contracts.

This separation prevents principles from becoming dogma, governance from collapsing into bureaucracy, and execution from drifting without intent.

### Formalize is the Structural Hinge

Formalize converts intent into a bounded, executable plan with explicit constraints, so work can proceed without inventing requirements.

At Formalize, the question is:

> "Given our principles, what constraints must we now accept to make progress?"

**Formalize also marks where the nature of iteration changes:**

- **Before Formalize (Discovery):** Iteration reshapes _what_ you're building. Cheap to change. Safe to abandon.
- **After Formalize (Refinement):** Iteration improves _how well_ you're building it. Scope is locked. Changes are costly.

Recognizing which mode you're in prevents wasted effort and expensive rework.

### Privacy is a Real Constraint

Privacy defines how information may be stored, shared, processed, and externalized. It is not a domain or stage—it is an overlay that constrains artifacts, tooling, collaboration, and AI usage.

- Declared at project inception
- Enforceable through deterministic rules
- Reclassifiable mid-project with explicit migration steps

### Sustain is Active Governance

Sustain is not a holding pattern—it's active governance of living work.

The question in Sustain: Does this change alter the contract I formalized, or does it extend/refine the implementation of that contract?

- **Contract change** → New iteration (regress to Formalize)
- **Implementation extension** → Sustain continues

---

## The Four Canonical Dimensions

### 1. Domain — What Kind of Work?

| Domain | Purpose | Formalize Artifact |
|--------|---------|-------------------|
| **Code** | Functional systems and tools | `docs/sod.md` (Solution Overview Document) |
| **Create** | Aesthetic and expressive output | `docs/brief.md` (Creative brief) |
| **Write** | Structured externalized thought | `docs/brief.md` (Writing brief) |
| **Learn** | Internal skill and model formation | `docs/plan.md` (Learning plan) |
| **Observe** | Raw capture without interpretation | (none required) |

Each domain supports **subtypes** for specialized guidance:

| Domain | Subtypes |
|--------|----------|
| Code | cli, library, api, webapp, infrastructure, script |
| Create | visual, audio, video, interactive, generative, design |
| Write | technical, business, narrative, academic, journalistic |
| Learn | skill, concept, practice, course, exploration |
| Observe | notes, bookmarks, clips, logs, captures |

### 2. Lifecycle Stage — Where is the Work?

Nine stages form the canonical lifecycle:

```
Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain → Close
```

| Stage | Purpose |
|-------|---------|
| **Capture** | Collect raw inputs without judgment |
| **Sense** | Synthesize meaning from captured material |
| **Explore** | Investigate options and alternatives |
| **Shape** | Define structure and boundaries |
| **Formalize** | Lock scope, create binding artifacts |
| **Commit** | Explicitly decide to proceed |
| **Execute** | Build the thing |
| **Sustain** | Maintain and evolve living work |
| **Close** | Archive or sunset |

**Critical Rule:** Formalize is a hard boundary. No execution without formalization artifacts.

**Allowed Regressions:**

| From | Can Regress To |
|------|----------------|
| Execute | Commit, Formalize |
| Sustain | Execute, Commit |
| Close | Capture |

**Regression UX:** Non-standard regressions that cross the Formalize boundary (e.g., Execute → Explore) display enhanced warnings showing which contract will be voided and the implications of moving from execution back to discovery mode.

### 3. Privacy Level — How Restricted?

Five levels from least to most restrictive:

1. **Public** — Open sharing, public AI allowed
2. **Public–Trusted** — Collaborators only, vetted AI tools
3. **Personal** — Individual use, local AI preferred
4. **Confidential** — Need-to-know, air-gapped AI only
5. **Restricted** — Maximum control, no AI processing

Privacy is mutable: upgrades require sanitization, downgrades are discouraged.

### 4. Environment — What Context?

- **Home** — Personal context, informal tone
- **Work** — Professional context, formal tone

Environment affects presentation and formality, not data handling.

---

## Key Features

### CLI Commands

```bash
# Project lifecycle
praxis new my-project --domain code --privacy personal
praxis init                           # Initialize existing directory
praxis stage formalize                # Transition stages
praxis status                         # Current state, next steps, history
praxis status --json                  # Machine-readable output
praxis context                        # Generate AI context bundle
praxis context --json                 # Machine-readable context
praxis validate                       # Check governance configuration
praxis validate --check-all           # Include tests, lint, types
praxis audit                          # Domain best practices check
praxis audit --strict                 # Fail on warnings

# In-terminal documentation
praxis guide lifecycle                # Lifecycle stages and hinge concept
praxis guide privacy                  # Privacy levels and constraints
praxis guide domain code              # Domain-specific guidance

# Workspace management
praxis workspace init                 # Initialize workspace
praxis extensions add render-run      # Install extensions
praxis examples add uat-praxis-code   # Install examples

# Opinions and templates
praxis opinions                       # Show applicable opinions
praxis opinions --prompt              # Generate AI context
praxis templates render               # Scaffold stage documentation

# Knowledge distillation pipeline
praxis pipeline init --tier 2         # Initialize pipeline
praxis pipeline run                   # Execute pipeline stage
praxis pipeline accept                # Accept output (HVA gate)
```

### Opinions Framework

Domain-specific guidance organized hierarchically with inheritance:

```
_shared/ → {domain}/principles.md → {domain}/{stage}.md → subtypes/
```

Opinions are advisory—they bias decisions without mechanical enforcement. Use `praxis opinions --prompt` to generate AI-ready context for your project.

Key opinions include:
- **Testing methodology** (`opinions/code/testing.md`) — TDD/BDD guidance for Code domain
- **Stage quality gates** — What "done" means at each stage
- **AI permissions** — What AI operations are allowed per domain

### Praxis Knowledge Distillation Pipeline (PKDP)

A risk-tiered pipeline for turning raw inputs into validated, decision-grade knowledge:

| Stage | Purpose |
|-------|---------|
| **RTC** | Raw Thought Capture |
| **IDAS** | Inquiry-Driven Analytical Synthesis |
| **SAD** | Specialist Agent Dispatch |
| **CCR** | Critical Challenge Review |
| **ASR** | Adjudicated Synthesis & Resolution |
| **HVA** | Human Validation & Acceptance |

**Risk Tiers** determine validation depth:
- Tier 0: RTC → IDAS (minimal validation)
- Tier 1: RTC → IDAS → SAD → ASR
- Tier 2: RTC → IDAS → SAD → CCR → ASR
- Tier 3: Full pipeline including HVA gate

### Roles Subsystem

Twelve governance roles with lifecycle-aware responsibilities:

| Role | Responsibility |
|------|----------------|
| **Product Owner** | Value decisions, backlog priority |
| **Developer** | Produces "Done" increments |
| **Research Librarian** | Epistemic backbone, knowledge validation |
| **Red Team** | Constructive adversarial challenge |
| **Synthesis** | Resolve conflicting inputs into direction |
| **Scrum Master** | Cadence and flow management |

Plus supporting roles: Stakeholder, Architect, Security, QA, FinOps, SRE.

Each role has defined decision rights, lifecycle activity by stage, and success criteria. See `core/roles/` for complete definitions.

### Stage Templates

Automatic generation of lifecycle documentation:

```bash
praxis templates render                  # Render docs for current stage
praxis templates render --stage formalize  # Specific stage
praxis templates render --force          # Overwrite existing
```

Templates provide domain-appropriate scaffolding for each lifecycle stage.

---

## Worked Examples

Praxis includes first-party worked examples demonstrating full lifecycle progression for each non-Code domain:

| Domain | Example | Demonstrates |
|--------|---------|--------------|
| **Write** | [Technical Article](examples/write/technical-article/) | Writing Brief, outline → drafts → final article, post-publication sustain |
| **Create** | [Design Exploration](examples/create/design-exploration/) | Creative Brief, visual explorations → iterations → final deliverables |
| **Learn** | [Python Testing](examples/learn/python-testing/) | Learning Plan, weekly notes + exercises + reflections, skill evidence |
| **Observe** | [Research Capture](examples/observe/research-capture/) | Raw capture, no formalize artifact, domain transition (Observe → Write) |

Each example includes:
- Full stage-by-stage progression (Capture → Sustain or Close)
- Domain-specific formalize artifact (Brief, Plan, or none for Observe)
- Realistic artifacts showing what "done" looks like at each stage
- README with "how to follow along" guidance

**Use these as templates** when starting a new project in these domains.

---

## Start Here

**New to Praxis:**
- [User Guide](docs/guides/user-guide.md) — Step-by-step walkthrough
- [AI Setup](docs/guides/ai-setup.md) — Configure AI assistants
- [Stage Templates](docs/guides/stage-templates.md) — Scaffold lifecycle docs
- **[Worked Examples](examples/)** — Full lifecycle examples for Write, Create, Learn, Observe

**Understanding the framework:**
- [SOD Specification](core/spec/sod.md) — Main specification
- [Lifecycle](core/spec/lifecycle.md) — Stage definitions and regressions
- [Domains](core/spec/domains.md) — Domain → artifact mappings
- [Privacy](core/spec/privacy.md) — Privacy levels and enforcement
- [Opinions Contract](core/governance/opinions-contract.md) — Opinions framework spec
- [Roles Index](core/roles/index.md) — Role definitions

**Knowledge distillation:**
- [PKDP Guide](docs/guides/pkdp.md) — Knowledge pipeline walkthrough

**Security:**
- [SECURITY.md](SECURITY.md) — Reporting vulnerabilities

---

## Quick Start

### 1. Install

```bash
# Clone the framework
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai

# Install dependencies
poetry install
```

### 2. Configure shell

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export PRAXIS_HOME="$HOME/praxis-workspace"
export PATH="$HOME/bin:$PATH"
```

Create CLI wrapper:

```bash
mkdir -p ~/bin
cat > ~/bin/praxis << 'EOF'
#!/bin/bash
exec poetry -C "$PRAXIS_HOME/praxis-ai" run praxis "$@"
EOF
chmod +x ~/bin/praxis
```

### 3. Initialize workspace

```bash
praxis workspace init
# Creates: extensions/, examples/, projects/, workspace-config.yaml
```

### 4. Create a project

```bash
praxis new my-project --domain code --privacy personal
# Creates: $PRAXIS_HOME/projects/code/my-project/
```

### 5. Work through the lifecycle

```bash
cd $PRAXIS_HOME/projects/code/my-project

# Check status and get guided next steps
praxis status
# Output includes:
#   Next Steps:
#     + Create docs/capture.md (Capture document)
#     ▶ Run `praxis stage sense` (Advance to Sense stage)
#
#   Legend: + create  ~ edit  ▶ run  ? review  ! fix

# Move through stages
praxis stage sense
praxis stage explore
praxis stage shape
praxis stage formalize  # Creates docs/sod.md template

# Stage history is automatically tracked in praxis.yaml
praxis status  # Shows recent stage transitions
# Stage History:
#   2026-01-04 explore → formalize       [contract-20260104-214744]
#   2026-01-03 sense → explore

# Non-standard regressions require rationale
praxis stage explore --reason "Scope change discovered during implementation"

# Validate before execution
praxis validate --strict
praxis stage commit
praxis stage execute
```

---

## Project Configuration

Projects are governed by `praxis.yaml`:

```yaml
domain: code                    # code|create|write|learn|observe
stage: capture                  # Current lifecycle stage
privacy_level: personal         # public|public-trusted|personal|confidential|restricted
environment: Home               # Home|Work
subtype: cli                    # Optional: enables subtype opinions
coverage_threshold: 80          # Optional: minimum test coverage %
```

---

## Repo Layout

```
src/praxis/           CLI package (Typer + Pydantic, hexagonal architecture)
  domain/             Pure business logic (models, enums, validation rules)
  application/        Orchestration services
  infrastructure/     External concerns (files, git, env vars)

core/                 Normative specifications (binding)
  spec/               System specs (sod.md, lifecycle.md, domains.md, privacy.md)
  governance/         Decision surfaces (layer-model.md, opinions-contract.md)
  ai/                 AI behavior controls (ai-guards.md, model-selection-matrix.md)
  roles/              Praxis Roles subsystem (12 roles with lifecycle matrices)

opinions/             Domain-specific quality guidance (advisory, not binding)
  _shared/            Cross-domain principles
  code/               Code domain (fully specified with subtypes)
  create/, write/, learn/, observe/

research-library/     Cataloged research with structured metadata
  CATALOG.md          Master index (33+ artifacts)
  ai-guards/          AI instruction and memory research
  foundations/        Classical roots, epistemology
  patterns/           Git+AI, TDD/BDD, code verification
  roles/              Role definitions and DORA analysis
  subagents/          Multi-agent design patterns

docs/guides/          User-facing tutorials
adr/                  Architecture Decision Records
tests/                BDD tests (pytest-bdd + Gherkin)

extensions.yaml       Registry of available extensions
examples.yaml         Registry of available examples
```

**Workspace structure:** User projects live at `$PRAXIS_HOME/projects/`, not inside this repo.

---

## Tech Stack

- **Language:** Python 3.12+
- **CLI:** Typer
- **Validation:** Pydantic v2
- **Testing:** pytest + pytest-bdd (BDD with Gherkin)
- **Package Manager:** Poetry
- **Linting:** ruff
- **Type Checking:** mypy

---

## Extensions and Examples

```bash
# List available
praxis extensions list
praxis examples list

# Install
praxis extensions add template-python-cli   # Python CLI scaffolding
praxis extensions add render-run            # AI image generation
praxis examples add uat-praxis-code         # Hello-world CLI example
praxis examples add opinions-framework      # Opinions research (Write domain)
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the issue workflow, labels, and development guidelines.

Run before committing:

```bash
poetry run pytest && poetry run ruff check . && poetry run mypy .
```

---

## Current Capabilities & Roadmap

This section clarifies what is **implemented today** vs what is **planned or aspirational**.

### Implementation Status by Feature

| Feature | Status | What Works | What's Planned | Docs/Specs |
|---------|--------|------------|----------------|------------|
| **Lifecycle Management** | ✅ Implemented | `stage`, `status`, stage transitions, regression warnings, stage history via git | Enhanced UX for cross-Formalize regressions | [lifecycle.md](core/spec/lifecycle.md) |
| **Project Initialization** | ✅ Implemented | `init`, `new` with domain/privacy/environment selection | Multi-domain projects | [domains.md](core/spec/domains.md) |
| **Validation** | ✅ Implemented | Schema validation, artifact existence checks, regression detection, privacy downgrade warnings | Deep artifact content validation | [ADR-002](adr/002-validation-model.md) |
| **Opinions Framework** | ✅ Implemented | Hierarchical resolution, inheritance (_shared → domain → stage → subtype), `opinions` command, AI context generation | More domain-specific opinions for Create, Write, Learn | [opinions-contract.md](core/governance/opinions-contract.md) |
| **Stage Templates** | ✅ Implemented | `templates render` for lifecycle docs, domain-specific scaffolding, extension template contributions | More templates per domain/subtype | [stage-templates.md](docs/guides/stage-templates.md) |
| **Workspace Management** | ✅ Implemented | `workspace init`, extension/example installation and management | Extension marketplace, remote registries | — |
| **Audit System** | ✅ Implemented | `audit` command with domain best practices checks, `--strict` mode | More comprehensive audit rules per domain | — |
| **Context Generation** | ✅ Implemented | `context` command with deterministic AI context bundles, JSON output | — | — |
| **Knowledge Pipeline (PKDP)** | ✅ Implemented | `pipeline` commands (init, run, accept, reject, refine), risk tiers 0-3, stage orchestration | Integration with research library, automated quality gates | [pkdp.md](docs/guides/pkdp.md) |
| **Privacy Guardrails** | ✅ Implemented | Privacy level declaration, downgrade warnings, validation | AI tool restrictions per privacy level, automated sanitization | [privacy.md](core/spec/privacy.md) |
| **Roles System** | 📋 Specified | 12 roles defined with lifecycle matrices, decision rights, success criteria | CLI integration, role-aware guidance and prompts | [roles/index.md](core/roles/index.md) |
| **Policy Engine** | ⚠️ Partial | Pydantic-based validation (domain + stage + privacy + environment → behavior), deterministic rules | Not a separate declarative engine (see ADR-001); may add CUE for complex composition | [ADR-001](adr/001-policy-engine.md) |
| **Multi-Domain Projects** | 📋 Planned | None | Support multiple domains in one repo via subdirectories | [ADR-002](adr/002-validation-model.md) |
| **AI Behavior Controls** | 📋 Specified | Permission matrices defined, guardrails documented | Enforcement integration with AI tools | [ai-guards.md](core/ai/ai-guards.md) |

**Legend:**
- ✅ **Implemented** — Fully functional and tested
- ⚠️ **Partial** — Core functionality works, but not all aspects are complete
- 📋 **Specified** — Documented and designed, but not yet implemented
- 📋 **Planned** — Identified for future development

### What "Policy Engine" Actually Means

The README and specs reference a "policy engine" for deterministic behavior resolution. **Clarification:**

- ✅ **What's implemented:** Python validation logic using Pydantic models that enforce rules based on `Domain + Stage + Privacy + Environment`
- ✅ **What works:** Schema validation, artifact checks, regression warnings, privacy guardrails
- ❌ **What's NOT implemented:** A separate declarative policy language or runtime engine (e.g., CUE, OPA)

Per [ADR-001](adr/001-policy-engine.md), Pydantic was chosen over CUE for pragmatism. The "engine" is just structured validation code, not a separate system. CUE may be added later if complex policy composition is needed.

### Opinions vs Enforcement

**Opinions are advisory guidance, not mechanically enforced rules.**

- ✅ Opinions **are** resolved hierarchically and provided to AI assistants via `praxis opinions --prompt`
- ✅ Opinions **do** influence quality gates and best practices
- ❌ Opinions are **NOT** enforced by the CLI (by design per [opinions-contract.md](core/governance/opinions-contract.md))
- ✅ Validation **does** enforce structural requirements (e.g., SOD required before Execute stage)

Think of it as: **Validation enforces structure; Opinions guide quality.**

---

## Status

Core CLI is functional with:
- Project commands: `init`, `new`, `validate`, `stage`, `status`, `audit`
- Workspace management: `workspace`, `extensions`, `examples`
- Opinions framework: `opinions` with inheritance and AI context generation
- Stage templates: `templates render` for lifecycle documentation
- Knowledge pipeline: `pipeline` for risk-tiered distillation

Code domain is fully specified. Other domains have foundational opinions in place.

## License

PolyForm Noncommercial License 1.0.0
