# Praxis-AI

## The Problem

AI amplifies throughput, not coherence. You can now generate 10x faster—but you can't govern 10x faster. The bottleneck moved from production to intent-maintenance.

Without structure, AI collaboration becomes chasing your own tail at higher speed: rediscovering rejected ideas, drifting scope mid-stream, refining things that aren't defined yet.

## What Praxis Does

Praxis makes human intent durable enough to survive AI's speed.

Your capacity for intent-maintenance is fixed. AI volume is not. Praxis provides leverage—canonical decisions, explicit scope boundaries, and stage gates that let fixed human intent govern unbounded AI output.

---

Praxis is a governance framework for AI-assisted work—moving ideas through a structured lifecycle into durable, governed outcomes.

Behavior is resolved deterministically by:

```text
Domain + Stage + Privacy + Environment → Behavior
```

This repo contains the core design docs plus worked projects.

## Philosophy

### Principles Guide — Contracts Bind — Formalize Arbitrates

No single artifact has universal authority.

- **Principles** are timeless and advisory; they bias decisions but are never enforced mechanically.
- **Formalization contracts** are context-specific and binding; they enable execution by freezing selected decisions.
- **Execution** is irreversible or costly to reverse; it must operate within the active contract.

Tension between principles and execution is intentional and necessary. Formalize is the explicit decision hinge where tradeoffs are made visible.

### The Three-Layer Model

Praxis separates what you believe from how you decide from how you execute.

```text
Opinions  →  Governance  →  Execution
```

- **Opinions:** Timeless viewpoints that bias decisions. Advisory, never enforced.
- **Governance:** The mechanism by which conflicts are resolved. Procedural authority.
- **Execution:** The work itself. Governed by formalization contracts.

This separation prevents principles from becoming dogma, governance from collapsing into bureaucracy, and execution from drifting without intent.

### Formalize is the Structural Hinge

Formalize converts intent into a bounded, executable plan with explicit constraints, so work can proceed without inventing requirements.

At Formalize, the question is:

> "Given our principles, what constraints must we now accept to make progress?"

Formalize exists to reduce ambiguity, freeze selected decisions, and enable safe execution. It is not bureaucracy; it is intentional commitment.

**Formalize also marks where the nature of iteration changes:**

- **Before Formalize (Discovery):** Iteration reshapes _what_ you're building. Cheap to change. Safe to abandon.
- **After Formalize (Refinement):** Iteration improves _how well_ you're building it. Scope is locked. Changes are costly.

Recognizing which mode you're in prevents wasted effort (polishing undefined things) and expensive rework (discovering scope mid-execution).

### Privacy is a Real Constraint

Privacy defines how information may be stored, shared, processed, and externalized. It is not a domain or stage—it is an overlay that constrains artifacts, tooling, collaboration, and AI usage.

- Declared at project inception
- Enforceable through deterministic rules
- Reclassifiable mid-project with explicit migration steps

Higher privacy requires greater abstraction and tighter controls.

### Sustain is Active Governance

Sustain is not a holding pattern—it's active governance of living work.

The question in Sustain: Does this change alter the contract I formalized, or does it extend/refine the implementation of that contract?

- **Contract change** → New iteration
- **Implementation extension** → Sustain

## What Praxis Optimizes For

AI-assisted creation is fast, but it’s easy to lose what actually worked.

Praxis treats your work as a lightweight “memory engine”:

- Capture what you tried (prompts, constraints, artifacts, decisions)
- Keep what reliably produces the outcome you want
- Cut what doesn’t
- Make the workflow reusable across future projects in the same domain

## Start Here

If you're new to Praxis:

- [docs/user-guide.md](docs/user-guide.md) — step-by-step walkthrough with examples
- [docs/ai-setup.md](docs/ai-setup.md) — configure AI assistants (CLAUDE.md, .cursorrules)

If you want to understand the framework:

- [docs/sod.md](docs/sod.md) — main specification
- [docs/lifecycle.md](docs/lifecycle.md) — stage definitions + regressions
- [docs/domains.md](docs/domains.md) — domain → artifact types
- [docs/privacy.md](docs/privacy.md) — privacy levels + enforcement intent
- [docs/external-constraints.md](docs/external-constraints.md) — environmental authority
- [docs/ai-guards.md](docs/ai-guards.md) — AI behavior governance (draft)

If you want to see Praxis applied in real projects:

- [projects/code/uat-praxis-code](projects/code/uat-praxis-code/) — hello-world CLI with full lifecycle docs
- [projects/code/template-python-cli](projects/code/template-python-cli/) — production CLI template (in Sustain)

## How Praxis Works (Short Version)

### Lifecycle

All work progresses through nine stages:

1. Capture
2. Sense
3. Explore
4. Shape
5. Formalize
6. Commit
7. Execute
8. Sustain
9. Close

Formalize is the structural hinge: you don’t “execute” without durable intent.

### Domains

Domains tell Praxis what kinds of artifacts are valid and what “done” looks like.

| Domain  | Intent                       | Typical formalize artifact       |
| ------- | ---------------------------- | -------------------------------- |
| Code    | Functional systems and tools | SOD (Solution Overview Document) |
| Create  | Aesthetic output             | Creative brief / prompt set      |
| Write   | Structured thought           | Writing brief                    |
| Observe | Raw capture                  | (none required)                  |
| Learn   | Skill formation              | Learning plan                    |

### Privacy

Privacy is declared in `praxis.yaml` and should be treated as a real constraint (not a note).

## Quick Start (CLI)

Install the Praxis CLI:

```bash
cd praxis-ai
poetry install
```

Validate a project's governance configuration:

```bash
# Validate current directory
poetry run praxis validate

# Validate a specific project
poetry run praxis validate projects/code/my-project/

# Treat warnings as errors (for CI)
poetry run praxis validate --strict

# Override environment via ENV var
PRAXIS_ENV=Work poetry run praxis validate
```

The validator checks:
- Schema correctness (domain, stage, privacy_level, environment)
- Required artifacts exist (e.g., `docs/sod.md` for Code domain at Execute stage)
- Stage regressions are valid (warns on invalid transitions)
- Privacy level wasn't downgraded (warns if less restrictive)

## Quick Start (Using an Agent)

From a project directory, start an agentic session (Copilot, Claude Code, etc.) and prompt:

```text
Start a new Praxis project for building a Python CLI tool.
```

Expected flow:

- The agent initializes `praxis.yaml` (domain, stage, privacy, environment)
- You capture raw inputs
- The agent guides you through stages
- Formalize produces the durable artifact(s) required before Execute

## Repo Layout

```text
docs/                 Specifications (SOD, lifecycle, privacy, etc.)
docs/adr/             Architecture Decision Records
docs/opinions/        Domain-specific quality guidance (advisory)
projects/             Worked projects
  code/template-python-cli/     Code-domain project
```

## Status

- Worked projects exist for the Code domain.
- The docs are the current source of truth; the system is being proven out through projects.

## License

MIT
