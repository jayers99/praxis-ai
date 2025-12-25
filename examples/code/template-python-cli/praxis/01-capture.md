# Capture: template-python-cli

**Stage:** Capture
**Domain:** Code
**Privacy:** Public

---

## Purpose

Collect raw inputs for building a reusable Python CLI project template.

---

## Raw Inputs

### What makes a good CLI template?

- [x] Standard project structure
- [x] Dependency management (Poetry)
- [x] CLI entrypoint scaffolding
- [x] Test scaffolding (pytest)
- [x] Praxis governance files

### Prior Art / References

- [x] Python Packaging User Guide
- [x] Click documentation (covered via Typer — Typer is built on Click)
- [x] Typer documentation
- [-] argparse stdlib (skipped — Typer chosen)
- [x] cookiecutter templates (reviewed — future scope for distribution)
- [x] Existing internal CLI projects (shuffle-aws-vaults — DDD + thin CLI pattern)

#### Python Packaging User Guide — Key Findings

**Project Structure (src layout confirmed):**

```text
project_name/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── cli.py          # CLI interface
│       ├── core.py         # Business logic
│       └── __main__.py     # Module execution entry
├── tests/
├── pyproject.toml
├── README.md
└── LICENSE
```

**pyproject.toml essentials:**

```toml
[build-system]
requires = ["hatchling >= 1.26"]
build-backend = "hatchling.build"

[project]
name = "package-name"
version = "0.1.0"
description = "Brief description"
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [{ name = "...", email = "..." }]

[project.scripts]
command-name = "package_name.cli:app"
```

**CLI Framework:** Typer recommended (auto-completion, styled help). Alternatives: click, argparse.

#### Typer Documentation — CLI Entrypoint Pattern

**File structure:**

```text
src/package_name/
├── __init__.py
├── __main__.py      # python -m package_name
├── cli.py           # Typer app + commands
└── core.py          # Business logic (DDD)
```

**cli.py (multi-command app):**

```python
import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def hello(name: str, formal: bool = False):
    """Greet someone."""
    if formal:
        print(f"Good day, {name}.")
    else:
        print(f"Hello {name}!")

if __name__ == "__main__":
    app()
```

****main**.py:**

```python
from package_name.cli import app

app()
```

**pyproject.toml entrypoint:**

```toml
[project.scripts]
mycli = "package_name.cli:app"
```

**Key patterns:**

- `typer.Typer(no_args_is_help=True)` — show help when no command given
- Type hints drive CLI behavior (required vs optional)
- Separate `cli.py` from `core.py` for testability (DDD)

#### Internal CLI Pattern — Hexagonal Architecture (Ports and Adapters)

**Reference:** <https://github.com/jayers99/shuffle-aws-vaults>

**Also known as:** Clean Architecture, Onion Architecture, Ports and Adapters

**Core principle:** Domain at the center, infrastructure at the edges, dependencies point inward.

**Preferred structure (Hexagonal layers):**

```text
src/package_name/
├── cli.py                    # Thin entry point — delegates to application layer
├── domain/                   # Pure business logic, no external dependencies
│   ├── __init__.py
│   ├── models.py             # Entities (e.g., vault.py, recovery_point.py)
│   └── rules.py              # Business rules (e.g., filter_rule.py)
├── application/              # Use case orchestration (verbs live here)
│   ├── __init__.py
│   ├── list_service.py       # "list" verb logic
│   ├── get_service.py        # "get" verb logic
│   └── copy_service.py       # "copy" verb logic
└── infrastructure/           # External integrations (AWS, DB, APIs)
    ├── __init__.py
    ├── repository.py         # Data access (boto3, etc.)
    ├── config.py             # Configuration loading
    └── logger.py             # Logging setup
```

**Thin CLI pattern:**

```python
# cli.py — thin, delegates to application layer
import typer
from package_name.application import list_service, get_service

app = typer.Typer(no_args_is_help=True)

@app.command()
def list(output: str = "table"):
    """List available items."""
    list_service.execute(output_format=output)

@app.command()
def get(name: str, output: str = "json"):
    """Get a specific item."""
    get_service.execute(name=name, output_format=output)
```

**Hexagonal mapping:**

```text
┌─────────────────────────────────────────────────────────┐
│                      Adapters (Ports)                   │
│  ┌─────────────┐                    ┌────────────────┐  │
│  │   cli.py    │ ← Input Adapter    │ infrastructure/│  │
│  │  (Typer)    │                    │  (AWS, DB)     │  │
│  └──────┬──────┘                    └───────┬────────┘  │
│         │          Output Adapter →         │           │
│         ▼                                   ▼           │
│  ┌─────────────────────────────────────────────────┐    │
│  │              application/ (Use Cases)           │    │
│  │         list_service, get_service, etc.         │    │
│  └─────────────────────┬───────────────────────────┘    │
│                        │                                │
│                        ▼                                │
│  ┌─────────────────────────────────────────────────┐    │
│  │              domain/ (Core Business)            │    │
│  │         models, rules — zero dependencies       │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Key patterns:**

- **CLI is a port** (input adapter) — thin, no business logic, just argument parsing + delegation
- **Verbs map to use cases** (application services: list → list_service, get → get_service)
- **Domain layer has zero external dependencies** — testable in isolation, pure business logic
- **Infrastructure is an adapter** (output adapter) — isolates AWS/DB/API behind repository pattern
- **Dependencies point inward** — domain knows nothing about CLI or infrastructure

**Benefits:**

- CLI changes don't affect business logic
- Domain logic testable without mocking external services
- Clear boundaries for testing (unit → domain, integration → infrastructure)
- Swap adapters easily (e.g., CLI → REST API, AWS → local file)
- Scales well as verbs/features grow

### Preferences / Constraints

- **Poetry** for dependency management (works at home + work)
- **pytest** for testing
- **ruff** for linting + formatting (replaces black, flake8, isort)
- **mypy** for type checking
- **BDD** — Behavior-driven development (outer loop, Gherkin scenarios)
- **TDD** — Test-driven development (inner loop, red-green-refactor)
- **DDD** — Domain-driven design (structure code around domain concepts)

#### Work Tooling (available at work)

- pytest, mypy, ruff, black (using ruff instead)
- gherkin (BDD specs) — consider for acceptance tests
- karate (API testing) — future scope
- pactflow (contract testing) — future scope
- sonar, SSAP, Raven — work-only, not in template

#### Test Scaffolding Pattern (pytest + Typer)

**Test directory structure:**

```text
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_cli.py          # CLI command tests
└── test_core.py         # Business logic tests (unit)
```

**test_cli.py (Typer testing pattern):**

```python
from typer.testing import CliRunner
from package_name.cli import app

runner = CliRunner()

def test_hello_default():
    result = runner.invoke(app, ["hello", "World"])
    assert result.exit_code == 0
    assert "Hello World!" in result.output

def test_hello_formal():
    result = runner.invoke(app, ["hello", "World", "--formal"])
    assert result.exit_code == 0
    assert "Good day, World." in result.output
```

**conftest.py (shared fixtures):**

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Test"}
```

**Key patterns:**

- `CliRunner` from typer.testing for CLI tests
- Separate `test_cli.py` (integration) from `test_core.py` (unit)
- Test exit codes + output assertions
- Use fixtures for shared test data

#### BDD Pattern (pytest-bdd + Gherkin)

**Test directory with BDD:**

```text
tests/
├── __init__.py
├── conftest.py              # Shared fixtures + step definitions
├── features/
│   └── greeting.feature     # Gherkin scenarios (BDD outer loop)
├── step_defs/
│   └── test_greeting.py     # Step implementations
├── test_cli.py              # CLI integration tests
└── test_core.py             # Unit tests (TDD inner loop)
```

**features/greeting.feature:**

```gherkin
Feature: Greeting command
  As a CLI user
  I want to greet someone
  So that I can be polite

  Scenario: Default greeting
    Given a name "World"
    When I run the hello command
    Then I should see "Hello World!"

  Scenario: Formal greeting
    Given a name "World"
    And the formal flag is set
    When I run the hello command
    Then I should see "Good day, World."
```

**step_defs/test_greeting.py:**

```python
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from typer.testing import CliRunner
from package_name.cli import app

scenarios('../features/greeting.feature')

runner = CliRunner()

@pytest.fixture
def context():
    return {}

@given(parsers.parse('a name "{name}"'))
def given_name(context, name):
    context['name'] = name

@given('the formal flag is set')
def formal_flag(context):
    context['formal'] = True

@when('I run the hello command')
def run_hello(context):
    args = ['hello', context['name']]
    if context.get('formal'):
        args.append('--formal')
    context['result'] = runner.invoke(app, args)

@then(parsers.parse('I should see "{expected}"'))
def check_output(context, expected):
    assert expected in context['result'].output
    assert context['result'].exit_code == 0
```

**Development flow (outside-in):**

1. Write Gherkin scenario (BDD - what behavior?)
2. Run pytest-bdd → fails (red)
3. Implement step definitions
4. Write unit test for domain logic (TDD - how to build?)
5. Implement in core.py using domain concepts (DDD)
6. All tests pass (green)
7. Refactor

### Directory Structure (decided)

```text
template-python-cli/
├── src/                # Application source code
├── tests/              # Test suite (TDD)
├── docs/               # Documentation
├── praxis/             # Praxis governance files
│   ├── praxis.yaml
│   └── {STAGE}.md      # Active stage artifact
├── CLAUDE.md           # AI context
└── README.md           # Project overview
```

#### Praxis Governance Files Pattern

**Design principles:**

- Enable seamless handoff between sessions, machines, or context resets
- Assume context window = 0 (no prior knowledge)
- All decisions captured in files, not memory

**praxis.yaml (starter template — blank):**

```yaml
domain:
stage:
privacy_level:
environment:
```

AI prompts user for all values at project initialization.

**Stage files (one per stage):**

```text
praxis/
├── praxis.yaml       # Current state (always present)
├── 01-capture.md     # Raw inputs, references, constraints
├── 02-sense.md       # Organized patterns, themes
├── 03-explore.md     # Options considered, spikes
├── 04-shape.md       # Refined approach, trade-offs
├── 05-formalize.md   # Formalize artifact (SOD)
├── 06-commit.md      # Commit readiness, final checks
├── 07-execute.md     # Implementation notes, decisions
├── 08-sustain.md     # Maintenance patterns, known issues
└── 09-close.md       # Retrospective, lessons learned
```

**Key rules:**

1. `praxis.yaml` tracks current stage — update as you progress
2. Stage files persist — never delete prior stage artifacts
3. Each stage file is self-contained context for that phase
4. `CLAUDE.md` at project root provides AI with project overview

**Initialization flow:**

1. AI detects blank/missing `praxis.yaml`
2. AI prompts: "What domain? (Code/Create/Write/Observe/Learn)"
3. AI prompts: "What privacy level? (Public/Personal/Confidential/Restricted)"
4. AI prompts: "What environment? (Home/Work)"
5. AI sets stage to `capture` and creates `01-capture.md`
6. User begins capturing inputs

---

## Open Questions

1. ~~Which CLI library? (click vs typer vs argparse)~~ → **Decided: Typer** (type hints, auto-completion, official recommendation)
2. ~~src layout vs flat layout?~~ → **Decided: src layout**
3. ~~What Praxis files belong in a template?~~ → **Decided: praxis/ subdir with blank praxis.yaml + stage files**
4. ~~Dependency management tool?~~ → **Decided: Poetry** (available at home + Work, modern, pyproject.toml native)
5. ~~Praxis governance file pattern?~~ → **Decided: Blank praxis.yaml, AI prompts for values, one file per stage, CLAUDE.md at root**

---

## Next Stage

When sufficient inputs are gathered, advance to **Sense** to organize and summarize patterns.
