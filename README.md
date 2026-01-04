# Praxis AI

**A governance framework that makes human intent durable enough to survive AI's speed.**

Praxis provides deterministic behavior resolution for AI-assisted work:

```
Domain + Stage + Privacy + Environment → Behavior
```

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

## Start Here

**New to Praxis:**
- [User Guide](docs/guides/user-guide.md) — Step-by-step walkthrough
- [AI Setup](docs/guides/ai-setup.md) — Configure AI assistants
- [Stage Templates](docs/guides/stage-templates.md) — Scaffold lifecycle docs

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
