# Praxis-AI

A policy-driven AI workflow system that governs how ideas evolve into maintained, durable outcomes.

## Quick Start

From any project directory, start an agentic AI session (Claude Code, Copilot, etc.) and prompt:

```
Start a new Praxis project for building a Python CLI tool.
```

The AI will:

1. **Initialize** — Create `praxis.yaml` with domain, privacy, and stage
2. **Capture** — Ask what you're trying to build and why
3. **Guide** — Walk you through each lifecycle stage
4. **Validate** — Ensure you don't skip required artifacts (like an SOD before execution)

### Example Session

```
You: Start a new Praxis project for building a Python CLI tool.

AI: I'll initialize a Praxis project for you.

    Created praxis.yaml:
      domain: code
      stage: capture
      privacy_level: personal

    We're now in the Capture stage. What problem does this CLI solve?
    Who will use it? What prior art or references should I know about?

You: It's a CLI for validating markdown files against a style guide...

AI: Got it. I've captured:
    - Problem: Markdown files drift from style conventions
    - Users: Technical writers, docs teams
    - References: markdownlint, vale

    Ready to move to Sense? I'll organize these inputs and identify patterns.
```

### What Praxis Prevents

- Starting to code before you've defined intent (Execute without Formalize)
- Accidentally exposing sensitive material (Privacy enforcement)
- Forgetting why you built something (Capture → Close lifecycle)
- AI acting without constraints (Policy-driven behavior)

## The Problem

AI-assisted work is structurally fragile. Current tools optimize for speed without providing coherent governance across the full lifecycle—from raw idea capture through sustained maintenance. This leads to:

- Premature execution without clear intent
- Privacy violations from unsafe AI defaults
- Work that can't be maintained or handed off
- No systematic way to know when to stop

## The Solution

Praxis provides **deterministic behavior resolution** based on four dimensions:

```
Domain + Stage + Privacy + Environment → Behavior
```

A single `praxis.yaml` file declares your project's configuration. The policy engine validates that your work respects lifecycle constraints, privacy requirements, and domain-specific formalization rules.

## Core Concepts

### Lifecycle Stages

Every piece of work moves through nine stages:

1. **Capture** — Raw input collection
2. **Sense** — Light organization and tagging
3. **Explore** — Divergent ideation
4. **Shape** — Convergence and refinement
5. **Formalize** — Durable intent via artifacts
6. **Commit** — Explicit decision to proceed
7. **Execute** — Implementation (governed by formalization)
8. **Sustain** — Ongoing maintenance
9. **Close** — Archival and learning capture

**Key rule:** Formalize is a hard boundary. No execution without formalization artifacts.

### Domains

| Domain  | Purpose            | Formalize Artifact         |
| ------- | ------------------ | -------------------------- |
| Code    | Functional systems | Solution Overview Document |
| Create  | Aesthetic output   | Creative Brief             |
| Write   | Structured thought | Writing Brief              |
| Observe | Raw capture        | (none required)            |
| Learn   | Skill formation    | Learning Plan              |

### Privacy Levels

From least to most restrictive:

1. **Public** — Open to all
2. **Public–Trusted** — Open with known collaborators
3. **Personal** — Private, single user or trusted collaborators
4. **Confidential** — Sensitive, controlled access
5. **Restricted** — Highly sensitive, air-gapped AI only

Privacy is declared at Explore, enforced at Shape/Formalize, and honored at Execute.

## Status

**Current:** First worked example complete. The [template-python-cli](examples/code/template-python-cli/) demonstrates the full Praxis lifecycle from Capture through Sustain.

**Next:** Implement `praxis validate` CLI tool to operationalize the governance model.

## Documentation

- [Solution Overview Document](docs/sod.md) — Complete specification
- [Lifecycle Model](docs/lifecycle.md) — Stage definitions and regression rules
- [Privacy Model](docs/privacy.md) — Privacy levels and enforcement
- [Domain Definitions](docs/domains.md) — Domain → artifact mappings
- [ADR-001](docs/adr/001-policy-engine.md) — Policy engine selection (exploratory)

## License

MIT
