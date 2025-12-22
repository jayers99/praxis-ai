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

### Run Commands

```bash
# Show help
poetry run template-python-cli --help

# Run helloworld command (default)
poetry run template-python-cli helloworld
# Output: Hello, World!

# Run helloworld with a name
poetry run template-python-cli helloworld Praxis
# Output: Hello, Praxis!
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
│   ├── CAPTURE.md
│   └── SENSE.md
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

**Stage:** Sense

See [praxis/SENSE.md](praxis/SENSE.md) for current stage artifact.

## Related

- [Issue #4](https://github.com/jayers99/praxis-ai/issues/4) — Parent issue
- [Praxis](https://github.com/jayers99/praxis-ai) — Policy-driven AI workflow system
