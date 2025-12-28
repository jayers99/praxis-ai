# Praxis AI - Claude Code Instructions

> **Note:** This is currently a **static, manual** file. In the future, this will be generated dynamically from `docs/ai-guards/models/`.


## Project Overview

Praxis is a policy-driven AI workflow system that governs how ideas evolve into maintained outcomes. It provides deterministic behavior resolution based on Domain + Stage + Privacy + Environment.

**Current Phase:** First worked project complete ([template-python-cli](projects/code/template-python-cli/)). Ready to implement `praxis validate` CLI.

## Tech Stack

- **Language:** Python
- **Policy Engine:** Pydantic (active implementation), CUE (exploratory/deferred per #3)
- **Testing:** pytest
- **Package Manager:** Poetry
- **Linting:** ruff
- **Type Checking:** mypy

## Key Concepts

### Lifecycle Stages (in order)

1. Capture → 2. Sense → 3. Explore → 4. Shape → 5. Formalize → 6. Commit → 7. Execute → 8. Sustain → 9. Close

**Critical Rule:** Formalize is a hard boundary. No execution without formalization artifacts.

**Iteration Mode:** Formalize is where iteration changes meaning. Before: _discovery_ (what is this?). After: _refinement_ (how good can it be?). Detecting scope change during Execute means regression to Formalize.

**Allowed Regressions (from `lifecycle.md` lines 104-118):**

| From | Allowed To |
|------|------------|
| Execute | Commit, Formalize |
| Sustain | Execute, Commit |
| Close | Capture |

### Domains

- **Code** — Functional systems (formalize via SOD)
- **Create** — Aesthetic output (formalize via Creative Brief)
- **Write** — Structured thought (formalize via Writing Brief)
- **Observe** — Raw capture (default: Personal privacy)
- **Learn** — Skill formation (formalize via Competency Target)

### Privacy Levels (least to most restrictive)

1. Public
2. Public–Trusted Collaborators
3. Personal
4. Confidential
5. Restricted

### Validation Model (ADR-002) — Core Contract

The validation model governs what the Policy Engine checks:

| Rule | Severity | Trigger |
|------|----------|---------|
| Unknown domain/stage/privacy | Error | Value not in allowed list |
| Missing formalize artifact | Error | stage ≥ commit AND artifact not found |
| Invalid stage regression | Warning | Transition not in allowed table |
| Privacy downgrade | Warning | privacy_level decreased from prior commit |

**Artifact Path Conventions:**

| Domain | Artifact | Path |
|--------|----------|------|
| Code | SOD | `docs/sod.md` |
| Create | Creative Brief | `docs/brief.md` |
| Write | Writing Brief | `docs/brief.md` |
| Learn | Learning Plan | `docs/plan.md` |
| Observe | (none) | — |

## Project Structure

```
docs/           # Specifications and design docs
  sod.md        # Solution Overview Document (main spec)
  lifecycle.md  # Canonical lifecycle stages
  privacy.md    # Privacy model
  domains.md    # Domain → artifact mappings
  formalize.md  # Formalize stage and artifact definitions
  adr/          # Architecture Decision Records
projects/       # Example projects across domains for discovering how to use Praxis
  code/template-python-cli/  # Complete project in Sustain stage
```

## Development Rules

### When Implementing

- All work must respect the lifecycle model
- Policy validation is deterministic: Domain + Stage + Privacy + Environment → Behavior
- No skipping required artifacts (e.g., SOD required before Execute in Code domain)
- Privacy declared at Explore, enforced at Shape/Formalize, honored at Execute

### Completed: Worked Project (Issue #4)

The [template-python-cli](projects/code/template-python-cli/) demonstrates the full Praxis lifecycle and is currently in Sustain stage.

### Next: `praxis validate` CLI

Deliverable: CLI validator implementing ADR-002's validation rules.

**Core Features (v1):**

1. Schema validation (`praxis.yaml` → Pydantic model)
2. Artifact existence check (stage ≥ commit → required artifact exists?)
3. Regression validation (warn if transition not in allowed table)
4. Privacy-storage coupling (error if restricted + non-local storage)

**Deferred:**

- AI Guard compilation (`.cursorrules` / `CLAUDE.md` generation)
- External constraints overlay
- Multi-domain composition
- Deep artifact content parsing

**Acceptance Tests:**

1. Valid `praxis.yaml` passes validation
2. Missing SOD at Execute stage → Error with explicit message
3. Invalid regression (Execute → Explore) → Warning
4. Privacy downgrade detected → Warning

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

**Primary for Policy Engine work:**

- [ADR-002](docs/adr/002-validation-model.md) — Validation model specification (core contract)
- [Lifecycle](docs/lifecycle.md) — Stage definitions and regression rules (lines 104-118)

**Supporting:**

- [SOD v0.3](docs/sod.md) — Complete specification
- [Privacy Model](docs/privacy.md) — Privacy levels and enforcement
- [Domains](docs/domains.md) — Domain → artifact mappings
- [Formalize](docs/formalize.md) — Formalize stage and artifact definitions
- [ADR-001](docs/adr/001-policy-engine.md) — Policy engine decision (exploratory)
- [template-python-cli](projects/code/template-python-cli/) — Complete worked project
