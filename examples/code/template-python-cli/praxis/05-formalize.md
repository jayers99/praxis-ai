# Formalize: template-python-cli

**Stage:** Formalize
**Domain:** Code
**Privacy:** Public

---

## Solution Overview Document (SOD)

### 1. Problem Statement

Developers need a consistent, well-structured starting point for Python CLI projects that:
- Follows modern Python packaging standards
- Separates concerns using proven architectural patterns
- Includes test scaffolding for BDD and TDD workflows
- Integrates with AI-assisted development (Claude Code)
- Tracks project lifecycle through Praxis governance

### 2. Proposed Solution

A reusable Python CLI project template using:
- **Hexagonal Architecture** for clean separation of concerns
- **Poetry** for dependency management
- **Typer** for CLI framework
- **pytest + pytest-bdd** for testing
- **ruff + mypy** for code quality
- **Praxis governance** for lifecycle tracking

### 3. Scope

#### In Scope
- Python 3.10+ CLI template
- Hexagonal Architecture (domain/application/infrastructure)
- BDD testing with Gherkin scenarios
- TDD testing with pytest
- Linting with ruff
- Type checking with mypy
- Praxis governance files
- Working helloworld example

#### Out of Scope
- CI/CD configuration
- Docker containerization
- Async/await patterns
- Database integrations
- Plugin architecture

### 4. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI (Typer)                          │
│                    [Input Adapter/Port]                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Application Layer                         │
│                 [Use Cases / Services]                       │
│              {verb}_service.py per command                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Domain Layer                            │
│              [Pure Business Logic]                           │
│           No external dependencies                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Infrastructure Layer                       │
│                 [Output Adapters/Ports]                      │
│            AWS, DB, APIs, File I/O                           │
└─────────────────────────────────────────────────────────────┘
```

### 5. File Structure

```
template-python-cli/
├── src/
│   └── template_python_cli/
│       ├── __init__.py              # Package metadata
│       ├── __main__.py              # python -m entry
│       ├── cli.py                   # Thin CLI adapter
│       ├── domain/                  # Pure business logic
│       │   ├── __init__.py
│       │   └── greeting.py
│       ├── application/             # Use cases
│       │   ├── __init__.py
│       │   └── helloworld_service.py
│       └── infrastructure/          # External integrations
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── features/
│   │   └── helloworld.feature
│   ├── step_defs/
│   │   ├── __init__.py
│   │   └── test_helloworld.py
│   ├── test_cli.py
│   └── test_domain.py
├── praxis/
│   ├── README.md
│   ├── praxis.yaml
│   ├── 01-capture.md
│   ├── 02-sense.md
│   ├── 03-explore.md
│   ├── 04-shape.md
│   └── 05-formalize.md
├── pyproject.toml
├── poetry.lock
├── CLAUDE.md
└── README.md
```

### 6. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| python | >=3.10 | Runtime |
| typer | >=0.9.0 | CLI framework |
| pytest | ^8.0 | Test runner |
| pytest-bdd | ^7.0 | BDD support |
| ruff | ^0.8 | Linting + formatting |
| mypy | ^1.0 | Type checking |

### 7. Conventions

| Aspect | Convention |
|--------|------------|
| Package name | `snake_case` |
| CLI command | `kebab-case` |
| Service files | `{verb}_service.py` |
| Feature files | `{feature}.feature` |
| Step definitions | `test_{feature}.py` |

### 8. Success Criteria

- [ ] Template can be cloned and run with `poetry install`
- [ ] `--help` shows available commands
- [ ] `helloworld` command works with default and custom name
- [ ] All tests pass (`poetry run pytest`)
- [ ] Linting passes (`poetry run ruff check .`)
- [ ] Type checking passes (`poetry run mypy src tests`)
- [ ] README Quick Start is accurate and complete

### 9. Constraints

- CLI must be thin (no business logic)
- Domain layer has zero external dependencies
- All external integrations go in infrastructure layer
- Tests must include BDD scenarios

### 10. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| pytest-bdd learning curve | Simple helloworld example demonstrates pattern |
| Hexagonal layers overkill for trivial CLIs | Trade-off for consistency; layers can be minimal |
| Poetry not available in all environments | Document alternative: pip install with pyproject.toml |

---

## Formalization Checklist

- [x] Problem statement is clear
- [x] Solution is specified
- [x] Scope is bounded (in/out)
- [x] Architecture is documented
- [x] File structure is defined
- [x] Dependencies are listed
- [x] Conventions are established
- [x] Success criteria are measurable
- [x] Constraints are explicit
- [x] Risks are identified

---

## Next Stage

When this SOD is approved, advance to **Commit** to lock scope and proceed to execution.

Note: This template is already implemented. Commit stage will confirm the implementation matches the SOD.
