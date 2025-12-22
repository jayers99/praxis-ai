# Shape: template-python-cli

**Stage:** Shape
**Domain:** Code
**Privacy:** Public

---

## Purpose

Define the final form of the Python CLI template — the canonical structure, conventions, and boundaries that will be formalized.

---

## Template Definition

### Name
`template-python-cli`

### Description
A reusable Python CLI project template using Hexagonal Architecture, BDD/TDD testing, and Praxis governance.

---

## Canonical Structure

```
template-python-cli/
├── src/
│   └── {package_name}/
│       ├── __init__.py              # Package metadata (version, etc.)
│       ├── __main__.py              # python -m entry point
│       ├── cli.py                   # Thin CLI adapter (Typer)
│       ├── domain/                  # Pure business logic
│       │   ├── __init__.py
│       │   └── {domain_module}.py   # Domain entities and logic
│       ├── application/             # Use cases (verbs)
│       │   ├── __init__.py
│       │   └── {verb}_service.py    # One service per CLI command
│       └── infrastructure/          # External integrations
│           └── __init__.py          # Placeholder for AWS, DB, APIs
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Shared pytest fixtures
│   ├── features/                    # Gherkin scenarios (BDD)
│   │   └── {feature}.feature
│   ├── step_defs/                   # Step implementations
│   │   ├── __init__.py
│   │   └── test_{feature}.py
│   ├── test_cli.py                  # CLI integration tests
│   └── test_domain.py               # Domain unit tests
├── praxis/                          # Praxis governance
│   ├── praxis.yaml                  # Current state
│   ├── 01-capture.md                # Stage artifact
│   ├── 02-sense.md                  # Stage artifact
│   ├── 03-explore.md                # Stage artifact
│   └── 04-shape.md                  # This file
├── pyproject.toml                   # Poetry configuration
├── poetry.lock                      # Locked dependencies
├── CLAUDE.md                        # AI context
└── README.md                        # User documentation
```

---

## Conventions

### Naming
- **Package name:** `snake_case` (e.g., `template_python_cli`)
- **CLI command:** `kebab-case` (e.g., `template-python-cli`)
- **Service files:** `{verb}_service.py` (e.g., `helloworld_service.py`)
- **Feature files:** `{feature}.feature` (e.g., `helloworld.feature`)
- **Step defs:** `test_{feature}.py` (e.g., `test_helloworld.py`)

### Architecture
- **CLI is thin:** No business logic, only argument parsing and delegation
- **Application services:** One per CLI command (verb), orchestrates domain
- **Domain is pure:** No external dependencies, testable in isolation
- **Infrastructure is isolated:** All external integrations (APIs, DB, files)

### Testing
- **BDD (outer loop):** Gherkin scenarios for acceptance criteria
- **TDD (inner loop):** Red-green-refactor for implementation
- **Three test types:**
  - `tests/features/` + `tests/step_defs/` — BDD acceptance
  - `tests/test_cli.py` — CLI integration (via CliRunner)
  - `tests/test_domain.py` — Domain unit tests

### Tooling
| Tool | Purpose | Configuration |
|------|---------|---------------|
| Poetry | Dependency management | `pyproject.toml` |
| Typer | CLI framework | `cli.py` |
| pytest | Test runner | `pyproject.toml` |
| pytest-bdd | BDD support | `tests/features/` |
| ruff | Linting + formatting | `pyproject.toml` |
| mypy | Type checking | `pyproject.toml` |

---

## Boundaries

### In Scope
- Python 3.10+
- Single CLI entry point
- Hexagonal Architecture layers
- BDD + TDD testing patterns
- Praxis governance files
- Basic documentation (README, CLAUDE.md)

### Out of Scope
- CI/CD configuration (GitHub Actions, etc.)
- Docker containerization
- Multiple entry points
- Plugin architecture
- Async/await patterns
- Database integrations (infrastructure layer is placeholder only)

---

## Customization Points

When using this template:

1. **Rename package:** `template_python_cli` → `your_package_name`
2. **Rename CLI command:** `template-python-cli` → `your-cli-name`
3. **Replace helloworld:** Add your own commands following the same pattern
4. **Extend infrastructure:** Add external integrations as needed
5. **Update praxis.yaml:** Set appropriate domain, stage, privacy, environment

---

## Acceptance Criteria

Before advancing to Formalize, verify:

- [x] All conventions documented above are implemented
- [x] Structure matches canonical layout
- [x] README accurately reflects the template
- [x] Tests validate the patterns work (7 passing)
- [x] CLAUDE.md provides sufficient AI context

---

## Next Stage

When the shape is finalized and accepted, advance to **Formalize** to create the formal specification (SOD) for this template.
