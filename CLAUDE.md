# Praxis AI - Claude Code Instructions

## Project Overview

Praxis is a policy-driven AI workflow system that governs how ideas evolve into maintained outcomes. It provides deterministic behavior resolution based on Domain + Stage + Privacy + Environment.

**Current Phase:** First worked example complete ([template-python-cli](examples/code/template-python-cli/)). Ready to implement `praxis validate` CLI.

## Tech Stack

- **Language:** Python
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
  domains.md    # Domain → artifact mappings
  formalize.md  # Formalize stage and artifact definitions
  adr/          # Architecture Decision Records
examples/       # Worked examples
  code/template-python-cli/  # Complete example in Sustain stage
```

## Development Rules

### When Implementing
- All work must respect the lifecycle model
- Policy validation is deterministic: Domain + Stage + Privacy + Environment → Behavior
- No skipping required artifacts (e.g., SOD required before Execute in Code domain)
- Privacy declared at Explore, enforced at Shape/Formalize, honored at Execute

### Completed: Worked Example (Issue #4)
The [template-python-cli](examples/code/template-python-cli/) demonstrates the full Praxis lifecycle and is currently in Sustain stage.

### Next: `praxis validate` CLI
Deliverable: CLI validator for praxis.yaml files

Acceptance tests:
1. Valid praxis.yaml passes (domain: code, stage: execute, privacy: confidential)
2. Missing SOD at Execute stage fails with explicit message
3. Public project with .env file triggers warning
4. Invalid stage transitions rejected

### praxis.yaml Schema
```yaml
domain: code|create|write|observe|learn
stage: capture|sense|explore|shape|formalize|commit|execute|sustain|close
privacy_level: public|public-trusted|personal|confidential|restricted
environment: Home|Work
```

## Commands

```bash
# Testing
poetry run pytest

# Linting
poetry run ruff check .

# Type checking
poetry run mypy .
```

## Opinions

Domain-specific quality goals live in `docs/opinions/{domain}/`. When working on a project:

1. Read `praxis.yaml` to determine the domain
2. Load `docs/opinions/{domain}/README.md` into context
3. If conversation matches any trigger keywords in the table, load the linked detail file(s)
4. If a detail file extends another (e.g., `cli-python` extends `cli`), load the base file too
5. Apply all loaded opinions to reasoning and suggestions

Opinions are advisory, not gates. They inform decisions without blocking progress.

## References

- [SOD v0.3](docs/sod.md) — Complete specification
- [Lifecycle](docs/lifecycle.md) — Stage definitions and regression rules
- [Privacy Model](docs/privacy.md) — Privacy levels and enforcement
- [Domains](docs/domains.md) — Domain → artifact mappings
- [Formalize](docs/formalize.md) — Formalize stage and artifact definitions
- [ADR-001](docs/adr/001-policy-engine.md) — Policy engine decision (exploratory)
- [ADR-002](docs/adr/002-validation-model.md) — Validation model positions
- [template-python-cli](examples/code/template-python-cli/) — Complete worked example
