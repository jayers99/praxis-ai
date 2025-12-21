# Praxis-AI

A policy-driven AI workflow system that governs how ideas evolve into maintained, durable outcomes.

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
| Build   | Functional systems | Solution Overview Document |
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

**Current:** Specification complete (v0.3), commit-ready for first executable increment.

**Next:** Validate the model with a worked example ([Issue #4](https://github.com/jayers99/praxis-ai/issues/4)).

## Documentation

- [Solution Overview Document](docs/sod.md) — Complete specification
- [Lifecycle Model](docs/lifecycle.md) — Stage definitions and regression rules
- [Privacy Model](docs/privacy.md) — Privacy levels and enforcement
- [Domain Definitions](docs/domains.md) — Domain → artifact mappings
- [ADR-001](docs/adr/001-policy-engine.md) — Policy engine selection (exploratory)

## License

MIT
