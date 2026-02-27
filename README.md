# Praxis AI

**A governance framework that makes human intent durable enough to survive AI's speed.**

For solo creators and small teams who use AI to build, write, create, and learn — Praxis gives you lifecycle governance, domain-specific guidance, and deterministic policy resolution so your intent stays coherent as AI accelerates your output.

> **Early-stage (v0.1.0)** · [GNU GPLv3](LICENSE) · Python 3.12+

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai
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

### 3. Create a project and go

```bash
praxis workspace init
praxis new my-project --domain code --privacy personal
cd $PRAXIS_HOME/projects/code/my-project

praxis status          # See where you are and what to do next
praxis stage sense     # Advance through the lifecycle
praxis validate        # Check governance rules
```

See the [User Guide](docs/guides/user-guide.md) for the full walkthrough.

---

## The Problem

AI amplifies throughput, not coherence. You can generate 10x faster — but you can't govern 10x faster. Without structure, AI collaboration becomes chasing your own tail at higher speed: rediscovering rejected ideas, drifting scope mid-stream, refining things that aren't defined yet.

Your capacity for intent-maintenance is fixed. AI volume is not. Praxis provides the leverage — canonical decisions, explicit scope boundaries, and stage gates that let fixed human intent govern unbounded AI output.

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

## The Four Dimensions

Praxis resolves behavior deterministically from four inputs:

```
Domain + Stage + Privacy + Environment → Behavior
```

### 1. Domain — What Kind of Work?

| Domain | Purpose | Formalize Artifact |
|--------|---------|-------------------|
| **Code** | Functional systems and tools | `docs/sod.md` |
| **Create** | Aesthetic and expressive output | `docs/brief.md` |
| **Write** | Structured externalized thought | `docs/brief.md` |
| **Learn** | Internal skill and model formation | `docs/plan.md` |
| **Observe** | Raw capture without interpretation | (none required) |

Each domain supports subtypes for specialized guidance (e.g., Code → cli, library, api, webapp, infrastructure, script).

### 2. Lifecycle Stage — Where is the Work?

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

**Formalize is a hard boundary** — no execution without formalization artifacts. Allowed regressions: Execute → Commit/Formalize, Sustain → Execute/Commit, Close → Capture.

### 3. Privacy Level — How Restricted?

Five levels from least to most restrictive:

1. **Public** — Open sharing, public AI allowed
2. **Public–Trusted** — Collaborators only, vetted AI tools
3. **Personal** — Individual use, local AI preferred
4. **Confidential** — Need-to-know, air-gapped AI only
5. **Restricted** — Maximum control, no AI processing

### 4. Environment — What Context?

- **Home** — Personal context, informal tone
- **Work** — Professional context, formal tone

---

## Philosophy

### Principles Guide — Contracts Bind — Formalize Arbitrates

- **Principles** are timeless and advisory; they bias decisions but are never enforced mechanically.
- **Formalization contracts** are context-specific and binding; they enable execution by freezing selected decisions.
- **Execution** is irreversible or costly to reverse; it must operate within the active contract.

Tension between principles and execution is intentional. Formalize is the decision hinge where tradeoffs are made visible.

### The Three-Layer Model

Praxis separates what you believe from how you decide from how you execute:

```
Opinions  →  Governance  →  Execution
```

- **Opinions:** Domain-specific guidance that biases decisions. Advisory, never enforced mechanically.
- **Governance:** The mechanism by which conflicts are resolved. Procedural authority.
- **Execution:** The work itself. Governed by formalization contracts.

### Formalize is the Structural Hinge

At Formalize, the question is: *"Given our principles, what constraints must we now accept to make progress?"*

- **Before Formalize (Discovery):** Iteration reshapes *what* you're building. Cheap to change. Safe to abandon.
- **After Formalize (Refinement):** Iteration improves *how well* you're building it. Scope is locked. Changes are costly.

See [lifecycle.md](core/spec/lifecycle.md) for full stage definitions and [layer-model.md](core/governance/layer-model.md) for the complete three-layer model.

---

## Key Features

### CLI Commands

```bash
# Project lifecycle
praxis new my-project --domain code --privacy personal
praxis init                           # Initialize existing directory
praxis stage formalize                # Transition stages
praxis status                         # Current state and guided next steps
praxis validate                       # Check governance configuration
praxis validate --check-all           # Include tests, lint, types
praxis audit                          # Domain best practices check

# Context and opinions
praxis context                        # Generate AI context bundle
praxis opinions --prompt              # AI-ready domain guidance

# Workspace management
praxis workspace init                 # Initialize workspace
praxis extensions add render-run      # Install extensions
praxis examples add uat-praxis-code   # Install examples

# Stage templates and knowledge pipeline
praxis templates render               # Scaffold stage documentation
praxis pipeline init --tier 2         # Initialize knowledge pipeline
praxis pipeline run                   # Execute pipeline stage

# In-terminal documentation
praxis guide lifecycle                # Lifecycle stages
praxis guide domain code              # Domain-specific guidance
```

### Opinions Framework

Domain-specific guidance organized hierarchically with inheritance:

```
_shared/ → {domain}/principles.md → {domain}/{stage}.md → subtypes/
```

Opinions are advisory — they bias decisions without mechanical enforcement. Use `praxis opinions --prompt` to generate AI-ready context.

### Knowledge Distillation Pipeline (PKDP)

Risk-tiered pipeline for turning raw inputs into validated knowledge:

| Tier | Pipeline |
|------|----------|
| 0 | RTC → IDAS (minimal validation) |
| 1 | RTC → IDAS → SAD → ASR |
| 2 | RTC → IDAS → SAD → CCR → ASR |
| 3 | Full pipeline including HVA gate |

### Roles Subsystem

Twelve governance roles with lifecycle-aware responsibilities including Product Owner, Developer, Research Librarian, Red Team, Synthesis, and Scrum Master — plus supporting roles (Stakeholder, Architect, Security, QA, FinOps, SRE). See [roles/index.md](core/roles/index.md) for complete definitions.

---

## Worked Examples

First-party examples demonstrating full lifecycle progression:

| Domain | Example | Demonstrates |
|--------|---------|--------------|
| **Write** | [Technical Article](examples/write/technical-article/) | Writing Brief, outline → drafts → final article |
| **Create** | [Design Exploration](examples/create/design-exploration/) | Creative Brief, visual explorations → iterations |
| **Learn** | [Python Testing](examples/learn/python-testing/) | Learning Plan, weekly notes + exercises |
| **Observe** | [Research Capture](examples/observe/research-capture/) | Raw capture, domain transition (Observe → Write) |

Each includes stage-by-stage progression, domain-specific formalize artifacts, and realistic artifacts showing what "done" looks like.

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

## Documentation

**Getting started:**
- [User Guide](docs/guides/user-guide.md) — Step-by-step walkthrough
- [AI Setup](docs/guides/ai-setup.md) — Configure AI assistants
- [Stage Templates](docs/guides/stage-templates.md) — Scaffold lifecycle docs
- [Worked Examples](examples/) — Full lifecycle examples for Write, Create, Learn, Observe

**Framework specs:**
- [SOD Specification](core/spec/sod.md) — Main specification
- [Lifecycle](core/spec/lifecycle.md) — Stage definitions and regressions
- [Domains](core/spec/domains.md) — Domain → artifact mappings
- [Privacy](core/spec/privacy.md) — Privacy levels and enforcement
- [Opinions Contract](core/governance/opinions-contract.md) — Opinions framework spec
- [Roles Index](core/roles/index.md) — Role definitions

**Knowledge distillation:**
- [PKDP Guide](docs/guides/pkdp.md) — Knowledge pipeline walkthrough

**Operations:**
- [CI/CD and Release Process](docs/CI-CD.md) — Build, test, and release documentation

---

## Implementation Status

| Feature | Status | Docs/Specs |
|---------|--------|------------|
| **Lifecycle Management** | ✅ Implemented | [lifecycle.md](core/spec/lifecycle.md) |
| **Project Initialization** | ✅ Implemented | [domains.md](core/spec/domains.md) |
| **Validation** | ✅ Implemented | [ADR-002](adr/002-validation-model.md) |
| **Opinions Framework** | ✅ Implemented | [opinions-contract.md](core/governance/opinions-contract.md) |
| **Stage Templates** | ✅ Implemented | [stage-templates.md](docs/guides/stage-templates.md) |
| **Workspace Management** | ✅ Implemented | — |
| **Audit System** | ✅ Implemented | — |
| **Context Generation** | ✅ Implemented | — |
| **Knowledge Pipeline (PKDP)** | ✅ Implemented | [pkdp.md](docs/guides/pkdp.md) |
| **Privacy Guardrails** | ✅ Implemented | [privacy.md](core/spec/privacy.md) |
| **Roles System** | 📋 Specified | [roles/index.md](core/roles/index.md) |
| **Policy Engine** | ⚠️ Partial | [ADR-001](adr/001-policy-engine.md) |
| **Multi-Domain Projects** | 📋 Planned | [ADR-002](adr/002-validation-model.md) |
| **AI Behavior Controls** | 📋 Specified | [ai-guards.md](core/ai/ai-guards.md) |

✅ Implemented · ⚠️ Partial · 📋 Specified/Planned

---

## Extensions

```bash
praxis extensions list
praxis extensions add template-python-cli   # Python CLI scaffolding
praxis extensions add render-run            # AI image generation
praxis examples add uat-praxis-code         # Hello-world CLI example
praxis examples add opinions-framework      # Opinions research (Write domain)
```

---

## Security

Praxis is a governance framework, not a security sandbox. It validates structural correctness and provides guidance but does not enforce runtime security boundaries. Privacy levels are intent declarations — users are responsible for selecting appropriate AI tools.

For the full security model, threat boundaries, and determinism guarantees, see [Security Model](docs/security-model.md). To report vulnerabilities, see [SECURITY.md](SECURITY.md).

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the issue workflow, labels, development guidelines, and CLA terms.

Run before committing:

```bash
poetry run pytest && poetry run ruff check . && poetry run mypy .
```

---

## License

GNU General Public License v3.0
