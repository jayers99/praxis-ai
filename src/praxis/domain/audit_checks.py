"""Audit check definitions by domain."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

from praxis.domain.domains import Domain
from praxis.infrastructure.pyproject_loader import get_dependencies, get_poetry_scripts


@dataclass
class CheckDefinition:
    """Definition of a single audit check."""

    name: str
    category: str
    check_fn: Callable[[Path], bool]
    pass_message: str
    fail_message: str
    severity: Literal["warning", "failed"] = "warning"


def _has_hexagonal_dirs(project_root: Path) -> bool:
    """Check for hexagonal architecture directories."""
    src_dir = project_root / "src"
    if not src_dir.exists():
        return False

    # Find package directory (first subdir of src/)
    packages = [
        d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith("_")
    ]
    if not packages:
        return False

    pkg = packages[0]
    required = ["domain", "application", "infrastructure"]
    return all((pkg / d).is_dir() for d in required)


def _has_main_module(project_root: Path) -> bool:
    """Check for __main__.py in package."""
    src_dir = project_root / "src"
    if not src_dir.exists():
        return False

    packages = [
        d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith("_")
    ]
    if not packages:
        return False

    return (packages[0] / "__main__.py").exists()


def _has_bdd_tests(project_root: Path) -> bool:
    """Check for BDD test structure."""
    features_dir = project_root / "tests" / "features"
    return features_dir.is_dir() and bool(list(features_dir.glob("*.feature")))


# Code domain checks
CODE_CHECKS: list[CheckDefinition] = [
    # Tooling
    CheckDefinition(
        name="poetry_configured",
        category="tooling",
        check_fn=lambda p: (p / "pyproject.toml").exists(),
        pass_message="Poetry configured (pyproject.toml exists)",
        fail_message="Poetry not configured (pyproject.toml missing)",
    ),
    CheckDefinition(
        name="typer_dependency",
        category="tooling",
        check_fn=lambda p: "typer" in get_dependencies(p),
        pass_message="Typer CLI (typer in dependencies)",
        fail_message="Typer not found in dependencies",
    ),
    CheckDefinition(
        name="ruff_configured",
        category="tooling",
        check_fn=lambda p: "ruff" in get_dependencies(p),
        pass_message="ruff linter (in dev dependencies)",
        fail_message="ruff not found in dev dependencies",
    ),
    CheckDefinition(
        name="mypy_configured",
        category="tooling",
        check_fn=lambda p: "mypy" in get_dependencies(p),
        pass_message="mypy type checker (in dev dependencies)",
        fail_message="mypy not found in dev dependencies",
    ),
    # Structure
    CheckDefinition(
        name="hexagonal_structure",
        category="structure",
        check_fn=_has_hexagonal_dirs,
        pass_message="Hexagonal architecture (domain/, application/, infrastructure/)",
        fail_message="Hexagonal directories not found",
    ),
    CheckDefinition(
        name="console_script",
        category="structure",
        check_fn=lambda p: bool(get_poetry_scripts(p)),
        pass_message="Console script entry point configured",
        fail_message="No console script in [tool.poetry.scripts]",
    ),
    CheckDefinition(
        name="main_module",
        category="structure",
        check_fn=_has_main_module,
        pass_message="__main__.py exists (python -m support)",
        fail_message="__main__.py not found in package",
    ),
    # Testing
    CheckDefinition(
        name="bdd_tests",
        category="testing",
        check_fn=_has_bdd_tests,
        pass_message="BDD tests (tests/features/*.feature exists)",
        fail_message="BDD tests not found (tests/features/)",
    ),
    CheckDefinition(
        name="pytest_bdd_dependency",
        category="testing",
        check_fn=lambda p: "pytest-bdd" in get_dependencies(p),
        pass_message="pytest-bdd in dependencies",
        fail_message="pytest-bdd not found in dev dependencies",
    ),
]


CHECKS_BY_DOMAIN: dict[Domain, list[CheckDefinition]] = {
    Domain.CODE: CODE_CHECKS,
    # Other domains can be added as opinions are defined
    Domain.CREATE: [],
    Domain.WRITE: [],
    Domain.OBSERVE: [],
    Domain.LEARN: [],
}
