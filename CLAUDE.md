# Praxis AI - Claude Code Instructions

## Project Overview

Praxis is a policy-driven AI workflow system that governs how ideas evolve into maintained outcomes. It provides deterministic behavior resolution based on Domain + Stage + Privacy + Environment.

**Current Phase:** CLI foundation complete (`validate`, `init`). Ready to extend with additional commands and domain support.

## Tech Stack

- **Language:** Python 3.12+
- **CLI Framework:** Typer
- **Validation:** Pydantic v2
- **Testing:** pytest + pytest-bdd (BDD with Gherkin)
- **Package Manager:** Poetry
- **Linting:** ruff
- **Type Checking:** mypy

## CLI Commands

```bash
# Initialize a new project
praxis init --domain code --privacy personal

# Validate governance configuration
praxis validate .
praxis validate --strict  # Treat warnings as errors
```

## Key Concepts

### Lifecycle Stages (in order)

1. Capture → 2. Sense → 3. Explore → 4. Shape → 5. Formalize → 6. Commit → 7. Execute → 8. Sustain → 9. Close

**Critical Rule:** Formalize is a hard boundary. No execution without formalization artifacts.

**Iteration Mode:** Formalize is where iteration changes meaning. Before: _discovery_ (what is this?). After: _refinement_ (how good can it be?). Detecting scope change during Execute means regression to Formalize.

**Allowed Regressions (from `lifecycle.md`):**

| From | Allowed To |
|------|------------|
| Execute | Commit, Formalize |
| Sustain | Execute, Commit |
| Close | Capture |

### Domains

| Domain | Purpose | Formalize Artifact |
|--------|---------|-------------------|
| Code | Functional systems | `docs/sod.md` |
| Create | Aesthetic output | `docs/brief.md` |
| Write | Structured thought | `docs/brief.md` |
| Learn | Skill formation | `docs/plan.md` |
| Observe | Raw capture | (none required) |

### Privacy Levels (least to most restrictive)

1. Public
2. Public–Trusted Collaborators
3. Personal
4. Confidential
5. Restricted

### Validation Model (ADR-002)

| Rule | Severity | Trigger |
|------|----------|---------|
| Unknown domain/stage/privacy | Error | Value not in allowed list |
| Missing formalize artifact | Error | stage ≥ commit AND artifact not found |
| Invalid stage regression | Warning | Transition not in allowed table |
| Privacy downgrade | Warning | privacy_level decreased from prior commit |

## Project Structure

```
src/praxis/              # Main CLI package
  cli.py                 # Typer CLI entry point
  domain/                # Domain models and enums
    models.py            # Pydantic models (PraxisConfig, ValidationResult, etc.)
    stages.py            # Stage enum with comparison operators
    domains.py           # Domain enum
    privacy.py           # PrivacyLevel enum
  application/           # Application services
    validate_service.py  # Validation orchestration
    init_service.py      # Project initialization
  infrastructure/        # External concerns
    yaml_loader.py       # YAML parsing
    artifact_checker.py  # File existence checks
    git_history.py       # Git operations (regression detection)
    env_resolver.py      # Environment variable handling
    templates.py         # CLAUDE.md and capture.md templates
    file_writer.py       # Safe file writes

tests/
  features/              # Gherkin feature files
  step_defs/             # pytest-bdd step definitions
  conftest.py            # Shared fixtures

docs/                    # Specifications and guides
  sod.md                 # Solution Overview Document
  lifecycle.md           # Stage definitions
  user-guide.md          # Step-by-step walkthrough
  ai-setup.md            # AI assistant configuration
  adr/                   # Architecture Decision Records

projects/                # Worked examples
  code/uat-praxis-code/  # Hello world CLI (full lifecycle)
  code/template-python-cli/  # Production template (Sustain)
```

## Development Rules

### Architecture

This project follows **hexagonal architecture**:
- **Domain:** Pure business logic, no external dependencies
- **Application:** Orchestration, coordinates domain + infrastructure
- **Infrastructure:** External concerns (files, git, env vars)
- **CLI:** Thin Typer layer, delegates to application services

### When Implementing

- All work must respect the lifecycle model
- Policy validation is deterministic: Domain + Stage + Privacy + Environment → Behavior
- No skipping required artifacts (e.g., SOD required before Execute in Code domain)
- Use BDD tests (Gherkin features + pytest-bdd step definitions)
- Run `poetry run pytest && poetry run ruff check . && poetry run mypy .` before committing

### praxis.yaml Schema

```yaml
domain: code|create|write|observe|learn
stage: capture|sense|explore|shape|formalize|commit|execute|sustain|close
privacy_level: public|public-trusted|personal|confidential|restricted
environment: Home|Work
```

## Commands

```bash
# Run tests
poetry run pytest

# Run linting
poetry run ruff check .

# Run type checking
poetry run mypy .

# Run the CLI
poetry run praxis --help
poetry run praxis init --help
poetry run praxis validate --help
```

## Potential Next Features

- `praxis stage [new-stage]` — Update stage with validation
- `praxis status` — Show current state and next steps
- Privacy enforcement — Check for violations (e.g., .env in public projects)
- Additional domain templates — Create, Write, Learn

## References

**User-facing:**
- [User Guide](docs/user-guide.md) — Step-by-step walkthrough
- [AI Setup](docs/ai-setup.md) — CLAUDE.md templates and integration

**Specification:**
- [SOD](docs/sod.md) — Solution Overview Document
- [Lifecycle](docs/lifecycle.md) — Stage definitions and regressions
- [Domains](docs/domains.md) — Domain → artifact mappings
- [Privacy](docs/privacy.md) — Privacy levels and enforcement

**Architecture:**
- [ADR-001](docs/adr/001-policy-engine.md) — Policy engine decision
- [ADR-002](docs/adr/002-validation-model.md) — Validation model specification

**Examples:**
- [uat-praxis-code](projects/code/uat-praxis-code/) — Hello world with full lifecycle docs
- [template-python-cli](projects/code/template-python-cli/) — Production CLI template
