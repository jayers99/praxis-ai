# Opinion: Python CLI Tool

> Extends [cli.md](cli.md) with Python-specific patterns

## Base Opinion

See [cli.md](cli.md) for general CLI ideals. This file adds Python-specific constraints.

## Architecture

- **Hexagonal Architecture** — Domain at center, infrastructure at edges
  - `domain/` — Pure business logic, no external dependencies
  - `application/` — Use cases, orchestration (verb-based services)
  - `infrastructure/` — External integrations (APIs, databases, file I/O)
- **Thin CLI layer** — CLI adapter contains no business logic, just argument parsing and delegation

## Tooling

- **Poetry** for dependency management
- **Console script entry point** via `[tool.poetry.scripts]`
- **Typer** for CLI framework
- **ruff** for linting and formatting
- **mypy** for type checking

## Testing

- **BDD** — Behavior-Driven Development with pytest-bdd and Gherkin scenarios
- **TDD** — Test-Driven Development (red-green-refactor inner loop)
- **pytest** as test runner
- Feature files in `tests/features/`, step definitions in `tests/step_defs/`

## Structure

```
src/
└── package_name/
    ├── __init__.py
    ├── __main__.py           # python -m entry
    ├── cli.py                # Thin CLI (Typer)
    ├── domain/               # Pure business logic
    ├── application/          # Use cases (verbs)
    └── infrastructure/       # External integrations
tests/
├── features/                 # Gherkin scenarios
├── step_defs/                # Step implementations
├── test_cli.py               # CLI integration tests
└── test_domain.py            # Domain unit tests
```

## Conventions

- Package name: `snake_case`
- CLI command: `kebab-case`
- Service files: `{verb}_service.py`
- Feature files: `{feature}.feature`
- Step definitions: `test_{feature}.py`

## Summary

Python CLIs using hexagonal architecture, Poetry, Typer, and BDD/TDD testing patterns.
