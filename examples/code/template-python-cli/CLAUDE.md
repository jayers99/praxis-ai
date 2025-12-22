# template-python-cli

## Current State

| Dimension | Value |
|-----------|-------|
| Domain | Code |
| Stage | Sustain |
| Privacy | Public |
| Environment | Home |

## Purpose

Build a reusable Python CLI project template that validates the Praxis lifecycle.

## Active Artifact

- [praxis/08-sustain.md](praxis/08-sustain.md) — Maintenance and governance

## Project Structure

```
template-python-cli/
├── src/
│   └── template_python_cli/
│       ├── __init__.py
│       ├── __main__.py           # python -m entry
│       ├── cli.py                # Thin CLI (Typer)
│       ├── domain/               # Pure business logic
│       ├── application/          # Use cases (verbs)
│       └── infrastructure/       # External integrations
├── tests/
│   ├── features/                 # Gherkin scenarios (BDD)
│   ├── step_defs/                # Step implementations
│   ├── test_cli.py               # CLI integration tests
│   └── test_domain.py            # Domain unit tests
├── praxis/                       # Praxis governance
│   ├── praxis.yaml
│   ├── 01-capture.md
│   ├── 02-sense.md
│   ├── 03-explore.md
│   ├── 04-shape.md
│   ├── 05-formalize.md
│   ├── 06-commit.md
│   ├── 07-execute.md
│   └── 08-sustain.md
├── pyproject.toml
├── CLAUDE.md                     # This file
└── README.md
```

## Development Approach

- **BDD** — Behavior-Driven Development (outer loop, Gherkin scenarios)
- **TDD** — Test-Driven Development (inner loop, red-green-refactor)
- **DDD** — Domain-Driven Design (structure code around domain concepts)
- **Hexagonal Architecture** — Ports and Adapters (domain at center, infrastructure at edges)

## Stage Rules

### Sustain
- Maintain and govern delivered work
- Updates, evaluation, optimization
- Policy enforcement over time

### Next Stage: Close
Advance when work is retired, superseded, or archived.

## Constraints

- Poetry for dependency management
- pytest + pytest-bdd for testing
- ruff for linting + formatting
- mypy for type checking

## Related

- [Issue #4](https://github.com/jayers99/praxis-ai/issues/4) — Parent issue
- [Praxis SOD](../../../docs/sod.md) — System specification
- [Lifecycle](../../../docs/lifecycle.md) — Stage definitions
