# Praxis AI - Claude Code Instructions

## Project Overview

Praxis is a policy-driven AI workflow system that governs how ideas evolve into maintained outcomes. It provides deterministic behavior resolution based on Domain + Stage + Privacy + Environment.

**Current Phase:** Specification complete (v0.3), ready for first executable increment.

## Tech Stack

- **Language:** Python (planned)
- **Policy Engine:** CUE (leading candidate, per ADR-001) or Pydantic fallback
- **Testing:** pytest
- **Package Manager:** Poetry
- **Linting:** ruff
- **Type Checking:** mypy

## Key Concepts

### Lifecycle Stages (in order)
1. Capture → 2. Sense → 3. Explore → 4. Shape → 5. Formalize → 6. Commit → 7. Execute → 8. Sustain → 9. Close

**Critical Rule:** Formalize is a hard boundary. No execution without formalization artifacts.

### Domains
- **Code** — Functional systems (formalize via SOD)
- **Create** — Aesthetic output (formalize via Creative Brief)
- **Write** — Structured thought (formalize via Writing Brief)
- **Observe** — Raw capture (default: Personal privacy)
- **Learn** — Skill formation (formalize via Learning Plan)

### Privacy Levels (least to most restrictive)
1. Public
2. Public–Trusted Collaborators
3. Personal
4. Confidential
5. Restricted

## Project Structure

```
docs/           # Specifications and design docs
  sod.md        # Solution Overview Document (main spec)
  lifecycle.md  # Canonical lifecycle stages
  privacy.md    # Privacy model
  adr/          # Architecture Decision Records
examples/       # Worked examples (Issue #4)
```

## Development Rules

### When Implementing
- All work must respect the lifecycle model
- Policy validation is deterministic: Domain + Stage + Privacy + Environment → Behavior
- No skipping required artifacts (e.g., SOD required before Execute in Code domain)
- Privacy declared at Explore, enforced at Shape/Formalize, honored at Execute

### First Increment (Issue #4)
Deliverable: Minimal policy schema + CLI validator for Code domain

Acceptance tests:
1. Valid praxis.yaml passes (domain: code, stage: execute, privacy: confidential)
2. Missing SOD at Execute stage fails with explicit message
3. Public project with .env file triggers warning
4. Invalid stage transitions rejected

### praxis.yaml Schema (planned)
```yaml
domain: code|create|write|observe|learn
stage: capture|sense|explore|shape|formalize|commit|execute|sustain|close
privacy_level: public|public-trusted|personal|confidential|restricted
environment: home|work
```

## Commands

```bash
# Testing (when implemented)
poetry run pytest

# Linting
poetry run ruff check .

# Type checking
poetry run mypy .
```

## References

- [SOD v0.3](docs/sod.md) — Complete specification
- [Lifecycle](docs/lifecycle.md) — Stage definitions and regression rules
- [Privacy Model](docs/privacy.md) — Privacy levels and enforcement
- [ADR-001](docs/adr/001-policy-engine.md) — Policy engine decision (exploratory)
- [Issue #4](https://github.com/jayers99/praxis-ai/issues/4) — First worked example
