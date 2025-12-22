# template-python-cli

A reusable Python CLI project template governed by Praxis.

## Quick Start

### Install

```bash
# Clone and navigate to the project
cd template-python-cli

# Install dependencies
poetry install
```

### Activate Virtual Environment

```bash
# Activate the Poetry virtual environment (Poetry 2.0+)
eval $(poetry env activate)

# Or add this alias to ~/.zshrc for convenience:
# alias penv='eval $(poetry env activate)'
```

### Run Commands

```bash
# With venv activated, run directly:
template-python-cli --help
template-python-cli helloworld
template-python-cli helloworld Praxis

# Or use poetry run (no activation needed):
poetry run template-python-cli helloworld
```

### Run Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run linting
poetry run ruff check .

# Run type checking
poetry run mypy src tests
```

## Project Structure

```
template-python-cli/
├── src/
│   └── template_python_cli/
│       ├── __init__.py
│       ├── __main__.py           # python -m entry
│       ├── cli.py                # Thin CLI (input adapter)
│       ├── domain/               # Core business logic
│       │   └── greeting.py
│       ├── application/          # Use cases (verbs)
│       │   └── helloworld_service.py
│       └── infrastructure/       # External integrations
├── tests/
│   ├── features/                 # Gherkin scenarios (BDD)
│   │   └── helloworld.feature
│   ├── step_defs/                # Step implementations
│   │   └── test_helloworld.py
│   ├── test_cli.py               # CLI integration tests
│   └── test_domain.py            # Domain unit tests
├── praxis/                       # Praxis governance
│   ├── praxis.yaml
│   ├── 01-capture.md
│   └── 02-sense.md
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

## Architecture

This template uses **Hexagonal Architecture** (Ports and Adapters):

- **cli.py** — Thin input adapter, delegates to application layer
- **application/** — Use cases, orchestrates domain logic
- **domain/** — Pure business logic, no external dependencies
- **infrastructure/** — External integrations (AWS, DB, APIs)

## Development Approach

- **BDD** — Behavior-Driven Development (Gherkin scenarios)
- **TDD** — Test-Driven Development (red-green-refactor)
- **DDD** — Domain-Driven Design (domain/application/infrastructure layers)

## Status

**Stage:** Sustain

See [praxis/08-sustain.md](praxis/08-sustain.md) for current stage artifact.

## Related

- [Issue #4](https://github.com/jayers99/praxis-ai/issues/4) — Parent issue
- [Praxis](https://github.com/jayers99/praxis-ai) — Policy-driven AI workflow system
- [praxis/README.md](praxis/README.md) — Governance files overview
