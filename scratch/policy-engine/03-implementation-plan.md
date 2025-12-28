# Policy Engine Implementation Plan

**Status:** Ready for approval
**Date:** 2025-12-27
**Relates to:** Issue #3, ADR-002, doc 02 (synthesis-commentary)

---

## Executive Summary

Implement `praxis validate` CLI using Pydantic, following the hexagonal architecture patterns established in template-python-cli. The validator implements ADR-002's validation rules: schema validation, artifact existence checks, regression warnings, and privacy downgrade detection.

---

## 1. Project Structure

```
src/praxis/
├── __init__.py
├── __main__.py                    # python -m praxis entry point
├── cli.py                         # Thin Typer CLI layer
├── domain/
│   ├── __init__.py
│   ├── models.py                  # Pydantic models: PraxisConfig, ValidationResult
│   ├── stages.py                  # Stage enum + ALLOWED_REGRESSIONS table
│   ├── domains.py                 # Domain enum + ARTIFACT_PATHS mapping
│   └── privacy.py                 # PrivacyLevel enum
├── application/
│   ├── __init__.py
│   └── validate_service.py        # Orchestrates validation rules
└── infrastructure/
    ├── __init__.py
    ├── yaml_loader.py             # Load praxis.yaml via Pydantic
    ├── artifact_checker.py        # Check artifact existence on filesystem
    ├── git_history.py             # Detect regressions via git diff
    └── env_resolver.py            # Resolve environment from PRAXIS_ENV or praxis.yaml
```

---

## 2. Core Components

### 2.1 Domain Models (Pydantic)

```python
# domain/models.py
from pydantic import BaseModel, model_validator
from .stages import Stage
from .domains import Domain
from .privacy import PrivacyLevel

class PraxisConfig(BaseModel):
    domain: Domain
    stage: Stage
    privacy_level: PrivacyLevel
    environment: str = "Home"  # Home | Work

class ValidationIssue(BaseModel):
    rule: str
    severity: Literal["error", "warning"]
    message: str

class ValidationResult(BaseModel):
    valid: bool
    issues: list[ValidationIssue] = []
```

### 2.2 Stage Enum + Regression Table

```python
# domain/stages.py
from enum import Enum

class Stage(str, Enum):
    CAPTURE = "capture"
    SENSE = "sense"
    EXPLORE = "explore"
    SHAPE = "shape"
    FORMALIZE = "formalize"
    COMMIT = "commit"
    EXECUTE = "execute"
    SUSTAIN = "sustain"
    CLOSE = "close"

# Stages that require formalization artifacts (stage >= commit)
REQUIRES_ARTIFACT = {Stage.COMMIT, Stage.EXECUTE, Stage.SUSTAIN, Stage.CLOSE}

ALLOWED_REGRESSIONS = {
    Stage.EXECUTE: {Stage.COMMIT, Stage.FORMALIZE},
    Stage.SUSTAIN: {Stage.EXECUTE, Stage.COMMIT},
    Stage.CLOSE: {Stage.CAPTURE},
}
```

### 2.3 Domain → Artifact Mapping

```python
# domain/domains.py
from enum import Enum
from pathlib import Path

class Domain(str, Enum):
    CODE = "code"
    CREATE = "create"
    WRITE = "write"
    OBSERVE = "observe"
    LEARN = "learn"

ARTIFACT_PATHS = {
    Domain.CODE: Path("docs/sod.md"),
    Domain.CREATE: Path("docs/brief.md"),
    Domain.WRITE: Path("docs/brief.md"),
    Domain.LEARN: Path("docs/plan.md"),
    Domain.OBSERVE: None,  # No artifact required
}
```

---

## 3. Validation Rules (from ADR-002)

| Rule | Severity | Implementation |
|------|----------|----------------|
| Unknown domain/stage/privacy | Error | Pydantic enum validation (automatic) |
| Missing formalize artifact | Error | `artifact_checker.py` — check path exists |
| Invalid stage regression | Warning | `git_history.py` — compare to HEAD~1 |
| Privacy downgrade | Warning | `git_history.py` — compare to HEAD~1 |

### 3.1 Artifact Existence Check

```python
# infrastructure/artifact_checker.py
def check_artifact_exists(config: PraxisConfig, project_root: Path) -> ValidationIssue | None:
    if config.stage not in REQUIRES_ARTIFACT:
        return None

    artifact_path = ARTIFACT_PATHS.get(config.domain)
    if artifact_path is None:
        return None  # Observe domain has no artifact

    full_path = project_root / artifact_path
    if not full_path.exists():
        return ValidationIssue(
            rule="missing_artifact",
            severity="error",
            message=f"Stage '{config.stage}' requires artifact at {artifact_path}, but file not found"
        )
    return None
```

### 3.2 Regression Detection (via Git)

```python
# infrastructure/git_history.py
def get_previous_config(project_root: Path) -> PraxisConfig | None:
    """Load praxis.yaml from HEAD~1 via git show."""
    result = subprocess.run(
        ["git", "show", "HEAD:praxis.yaml"],
        cwd=project_root,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return None  # No prior commit or file didn't exist
    return PraxisConfig.model_validate(yaml.safe_load(result.stdout))

def check_regression(current: PraxisConfig, previous: PraxisConfig | None) -> ValidationIssue | None:
    if previous is None:
        return None

    if current.stage < previous.stage:  # Moving backward
        allowed = ALLOWED_REGRESSIONS.get(previous.stage, set())
        if current.stage not in allowed:
            return ValidationIssue(
                rule="invalid_regression",
                severity="warning",
                message=f"Regression from {previous.stage} → {current.stage} not in allowed table. Allowed: {allowed}"
            )
    return None
```

---

## 4. CLI Interface

```bash
# Primary command
praxis validate [PATH]

# Examples
praxis validate                    # Validates ./praxis.yaml
praxis validate ./projects/foo     # Validates ./projects/foo/praxis.yaml
praxis validate --strict           # Treat warnings as errors (exit 1)
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Valid (no errors, warnings allowed) |
| 1 | Invalid (errors found) |
| 2 | Invalid (warnings found, --strict mode) |

### CLI Implementation

```python
# cli.py
import typer
from pathlib import Path
from praxis.application.validate_service import validate

app = typer.Typer(no_args_is_help=False)

@app.command()
def validate_cmd(
    path: Path = typer.Argument(Path("."), help="Path to project root or praxis.yaml"),
    strict: bool = typer.Option(False, "--strict", help="Treat warnings as errors"),
) -> None:
    """Validate a praxis.yaml configuration."""
    result = validate(path)

    for issue in result.issues:
        icon = "✗" if issue.severity == "error" else "⚠"
        typer.echo(f"{icon} [{issue.severity.upper()}] {issue.message}")

    if result.valid:
        typer.echo("✓ praxis.yaml is valid")
        raise typer.Exit(0)

    errors = [i for i in result.issues if i.severity == "error"]
    warnings = [i for i in result.issues if i.severity == "warning"]

    if errors:
        raise typer.Exit(1)
    if warnings and strict:
        raise typer.Exit(2)
    raise typer.Exit(0)
```

---

## 5. Testing Strategy

### 5.1 BDD Feature File

```gherkin
# tests/features/validate.feature
Feature: Praxis Validate CLI

  Scenario: Valid configuration passes
    Given a praxis.yaml with domain "code" and stage "execute"
    And a docs/sod.md file exists
    When I run praxis validate
    Then the exit code should be 0
    And the output should contain "valid"

  Scenario: Missing SOD at Execute stage fails
    Given a praxis.yaml with domain "code" and stage "execute"
    And no docs/sod.md file exists
    When I run praxis validate
    Then the exit code should be 1
    And the output should contain "ERROR"
    And the output should contain "docs/sod.md"

  Scenario: Invalid regression produces warning
    Given a praxis.yaml with stage "explore"
    And the previous commit had stage "execute"
    When I run praxis validate
    Then the exit code should be 0
    And the output should contain "WARNING"
    And the output should contain "regression"
```

### 5.2 Unit Tests

```python
# tests/domain/test_stages.py
def test_execute_requires_artifact():
    assert Stage.EXECUTE in REQUIRES_ARTIFACT

def test_explore_does_not_require_artifact():
    assert Stage.EXPLORE not in REQUIRES_ARTIFACT

# tests/domain/test_regression.py
def test_execute_to_formalize_allowed():
    assert Stage.FORMALIZE in ALLOWED_REGRESSIONS[Stage.EXECUTE]

def test_execute_to_explore_not_allowed():
    assert Stage.EXPLORE not in ALLOWED_REGRESSIONS[Stage.EXECUTE]
```

---

## 6. Dependencies

```toml
# pyproject.toml additions
[tool.poetry.dependencies]
python = ">=3.10"
typer = ">=0.9.0"
pydantic = ">=2.0"
pyyaml = ">=6.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-bdd = "^7.0"
ruff = "^0.8"
mypy = "^1.0"

[tool.poetry.scripts]
praxis = "praxis.cli:app"
```

---

## 7. Implementation Phases

### Phase 1: Core Validation (MVP)
1. Create project structure under `src/praxis/`
2. Implement Pydantic models (Domain, Stage, PrivacyLevel, PraxisConfig)
3. Implement artifact existence check
4. Implement basic CLI with validate command
5. Write acceptance tests for core scenarios

### Phase 2: Git-Based Detection
1. Implement git_history.py for reading previous config
2. Add regression detection
3. Add privacy downgrade detection
4. Extend tests for git-based scenarios

### Phase 3: Polish
1. Add --strict flag
2. Improve error messages
3. Add --json output option for CI integration
4. Documentation

---

## 8. Design Decisions (Resolved)

### D1: Package Location
**Decision:** `src/praxis/` — Top-level package, the official Praxis CLI.
- Command: `praxis validate`
- Future commands like `praxis compile` fit naturally as subcommands.

### D2: Git Integration Scope
**Decision:** Compare to HEAD only.
- No git repo → skip regression/privacy checks (info message)
- Uncommitted new file → skip (no baseline to compare)
- Compare current praxis.yaml to `HEAD:praxis.yaml`

### D3: Environment Source
**Decision:** ENV var override.
- Read `environment` from praxis.yaml as default
- Allow `PRAXIS_ENV=Work` to override the declared value
- This enables same project to validate differently in different contexts

---

## 9. Acceptance Criteria (from CLAUDE.md)

- [ ] Valid `praxis.yaml` passes validation
- [ ] Missing SOD at Execute stage → Error with explicit message
- [ ] Invalid regression (Execute → Explore) → Warning
- [ ] Privacy downgrade detected → Warning

---

## 10. Files to Create

| File | Purpose |
|------|---------|
| `src/praxis/__init__.py` | Package init, version |
| `src/praxis/__main__.py` | python -m entry point |
| `src/praxis/cli.py` | Typer CLI |
| `src/praxis/domain/models.py` | Pydantic models |
| `src/praxis/domain/stages.py` | Stage enum + regression table |
| `src/praxis/domain/domains.py` | Domain enum + artifact paths |
| `src/praxis/domain/privacy.py` | PrivacyLevel enum |
| `src/praxis/application/validate_service.py` | Validation orchestration |
| `src/praxis/infrastructure/yaml_loader.py` | YAML parsing |
| `src/praxis/infrastructure/artifact_checker.py` | File existence check |
| `src/praxis/infrastructure/git_history.py` | Git-based detection |
| `src/praxis/infrastructure/env_resolver.py` | PRAXIS_ENV override logic |
| `tests/features/validate.feature` | BDD scenarios |
| `tests/step_defs/test_validate.py` | Step definitions |
| `tests/conftest.py` | Fixtures |
| `pyproject.toml` | Package config |
