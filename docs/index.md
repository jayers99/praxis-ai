# Praxis Documentation

**A governance framework that makes human intent durable enough to survive AI's speed.**

Praxis provides deterministic behavior resolution for AI-assisted work:

```
Domain + Stage + Privacy + Environment → Behavior
```

---

## What is Praxis?

Praxis is a policy-driven AI workflow system that governs how ideas evolve into maintained outcomes. Whether you're building software, creating art, writing documents, or learning skills—Praxis gives you lifecycle governance, domain-specific guidance, and the structure to maintain coherent intent as AI accelerates your output.

---

## Quick Links

<div class="grid cards" markdown>

- :material-rocket-launch: **[Getting Started](guides/user-guide.md)**

    ---
    
    Step-by-step walkthrough to create your first Praxis project

- :material-book-open-variant: **[Philosophy](core/spec/sod.md)**

    ---
    
    Understand the core concepts and governance model

- :material-console: **[CLI Reference](reference/cli.md)**

    ---
    
    Complete command reference for the Praxis CLI

- :material-brain: **[AI Setup](guides/ai-setup.md)**

    ---
    
    Configure AI assistants to work with Praxis

</div>

---

## Core Concepts

### Lifecycle Stages

Nine stages form the canonical lifecycle:

```
Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain → Close
```

**Formalize is the structural hinge** — the hard boundary between discovery and execution. No execution without formalization artifacts.

[Learn more about Lifecycle →](core/spec/lifecycle.md){ .md-button }

---

### Domains

Five work types, each with specific artifacts and governance:

| Domain | Purpose | Formalize Artifact |
|--------|---------|-------------------|
| **Code** | Functional systems and tools | `docs/sod.md` |
| **Create** | Aesthetic and expressive output | `docs/brief.md` |
| **Write** | Structured externalized thought | `docs/brief.md` |
| **Learn** | Internal skill and model formation | `docs/plan.md` |
| **Observe** | Raw capture without interpretation | (none required) |

[Learn more about Domains →](core/spec/domains.md){ .md-button }

---

### Privacy Levels

Five levels that constrain how data flows, not just who sees it:

1. **Public** — Open sharing, public AI allowed
2. **Public–Trusted** — Collaborators only, vetted AI tools
3. **Personal** — Individual use, local AI preferred
4. **Confidential** — Need-to-know, air-gapped AI only
5. **Restricted** — Maximum control, no AI processing

[Learn more about Privacy →](core/spec/privacy.md){ .md-button }

---

## Key Features

### Project Lifecycle Management

```bash
praxis new my-project --domain code --privacy personal
cd my-project
praxis status              # Check current stage and next steps
praxis stage formalize     # Advance to Formalize stage
praxis validate --strict   # Validate governance rules
```

### Opinions Framework

Domain-specific guidance organized hierarchically:

```
_shared/ → {domain}/principles.md → {domain}/{stage}.md → subtypes/
```

Opinions are advisory—they bias decisions without mechanical enforcement.

### Stage Templates

Automatic generation of lifecycle documentation:

```bash
praxis templates render --stage formalize  # Create stage docs
```

### Knowledge Distillation Pipeline (PKDP)

Risk-tiered pipeline for turning raw inputs into validated knowledge:

```
RTC → IDAS → SAD → CCR → ASR → HVA
```

---

## Installation

### Quick Start

```bash
# Clone the framework
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai

# Install dependencies
poetry install

# Configure shell
export PRAXIS_HOME="$HOME/praxis-workspace"
export PATH="$HOME/bin:$PATH"

# Initialize workspace
praxis workspace init

# Create a project
praxis new my-project --domain code --privacy personal
```

[Full installation guide →](guides/installation.md){ .md-button }

---

## Philosophy

### Principles Guide — Contracts Bind — Formalize Arbitrates

No single artifact has universal authority.

- **Principles** are timeless and advisory; they bias decisions but are never enforced mechanically.
- **Formalization contracts** are context-specific and binding; they enable execution by freezing selected decisions.
- **Execution** is irreversible or costly to reverse; it must operate within the active contract.

Tension between principles and execution is intentional and necessary. Formalize is the explicit decision hinge where tradeoffs are made visible.

[Read the full philosophy →](core/spec/sod.md){ .md-button }

---

## Contributing

We welcome contributions! See the [Contributing Guide](CONTRIBUTING.md) for details on:

- Issue workflow and labels
- Testing requirements (BDD with Gherkin)
- Code standards and review process

---

## License

GNU General Public License v3.0

---

## Status

Core CLI is functional with project lifecycle management, workspace management, opinions framework, stage templates, and knowledge distillation pipeline.

**Version:** 0.1.0  
**Python:** 3.12+  
**Last Updated:** 2026-01-05
