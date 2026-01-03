---
domain: code
subtype: cli-python
version: "1.0"
status: active
author: human
---

# Code × CLI × Python Opinions

> **Scope:** Python CLI tools, extending general CLI principles

## Quick Navigation

- [CLI Principles](../principles.md) — Parent CLI principles
- [Code Principles](../../../principles.md) — Domain principles

## Python CLI at a Glance

| Aspect | Value |
|--------|-------|
| Framework | Typer (recommended) |
| Packaging | Poetry with console scripts |
| Architecture | Hexagonal (domain/application/infrastructure) |
| Testing | BDD with pytest-bdd |

## Architecture

Follow hexagonal architecture to separate concerns:

```
src/
└── package_name/
    ├── __init__.py
    ├── __main__.py           # python -m entry
    ├── cli.py                # Thin CLI (Typer)
    ├── domain/               # Pure business logic
    ├── application/          # Use cases (verbs)
    └── infrastructure/       # External integrations
```

### Layer Rules

| Layer | Can Import | Cannot Import |
|-------|------------|---------------|
| domain | stdlib, pydantic | application, infrastructure |
| application | domain, stdlib | infrastructure directly |
| infrastructure | anything | — |
| cli | application, typer | domain, infrastructure |

## Recommended Stack

| Purpose | Tool | Rationale |
|---------|------|-----------|
| CLI Framework | Typer | Type hints, auto-help, shell completion |
| Dependency Mgmt | Poetry | Lock files, dev dependencies |
| Linting | ruff | Fast, comprehensive |
| Type Checking | mypy | Static analysis |
| Testing | pytest + pytest-bdd | BDD with Gherkin |

## Testing Strategy

- **BDD outer loop:** Feature files describe user behavior
- **TDD inner loop:** Unit tests drive implementation
- **Integration tests:** CLI invocation via `typer.testing.CliRunner`

### File Structure

```
tests/
├── features/                 # Gherkin scenarios
│   ├── init.feature
│   └── validate.feature
├── step_defs/                # Step implementations
│   ├── test_init.py
│   └── test_validate.py
└── conftest.py               # Shared fixtures
```

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Package | snake_case | `my_cli_tool` |
| CLI command | kebab-case | `my-cli-tool` |
| Service files | `{verb}_service.py` | `init_service.py` |
| Feature files | `{feature}.feature` | `validate.feature` |
| Step definitions | `test_{feature}.py` | `test_validate.py` |

## Entry Points

### Console Script (Primary)

```toml
[tool.poetry.scripts]
my-tool = "my_package.cli:app"
```

### Python -m Support

```python
# src/my_package/__main__.py
from my_package.cli import app

if __name__ == "__main__":
    app()
```

## Anti-Patterns (Python-Specific)

### Business Logic in CLI Layer

- **What:** Complex logic in `cli.py`
- **Why bad:** Hard to test, violates hexagonal
- **Instead:** Delegate to application services

### Direct Infrastructure Access

- **What:** Reading files or calling APIs from domain
- **Why bad:** Couples domain to I/O
- **Instead:** Use infrastructure adapters

### Missing Type Hints

- **What:** Untyped functions and parameters
- **Why bad:** Mypy can't help, IDE support degraded
- **Instead:** Type all public interfaces

## Quality Gates (Python CLI)

| Gate | Severity |
|------|----------|
| ruff passes | must-have |
| mypy passes | must-have |
| pytest passes | must-have |
| `--help` works | must-have |
| `--version` works | must-have |
| Console script defined | must-have |
| `__main__.py` exists | should-have |

## References

- [CLI-Python Opinion](../../cli-python.md) — Legacy file (being migrated)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/)
