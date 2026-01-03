"""Audit check definitions by domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal

from praxis.domain.domains import Domain
from praxis.domain.stages import Stage
from praxis.infrastructure.audit_helpers import dir_exists, file_exists_any
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
    min_stage: Stage | None = None  # Check only applies at this stage or later
    subtypes: list[str] | None = field(default=None)  # Only for these subtypes


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


# =============================================================================
# Create Domain Checks
# =============================================================================

CREATE_CHECKS: list[CheckDefinition] = [
    CheckDefinition(
        name="brief_present",
        category="artifact",
        check_fn=lambda p: file_exists_any(p, "docs/brief.md"),
        pass_message="Brief exists (docs/brief.md)",
        fail_message=(
            "Brief not found. Create docs/brief.md to formalize your creative "
            "vision."
        ),
        min_stage=Stage.FORMALIZE,
    ),
    CheckDefinition(
        name="assets_organized",
        category="organization",
        check_fn=lambda p: dir_exists(p, "assets"),
        pass_message="Assets organized (assets/ directory exists)",
        fail_message=(
            "Assets not organized. Create an assets/ directory for your "
            "creative outputs."
        ),
    ),
    CheckDefinition(
        name="prompts_documented",
        category="workflow",
        check_fn=lambda p: (
            dir_exists(p, "prompts") or file_exists_any(p, "docs/prompts.md")
        ),
        pass_message="Prompts documented (prompts/ or docs/prompts.md exists)",
        fail_message=(
            "Prompts not documented. Create prompts/ directory or docs/prompts.md "
            "to track your AI generation prompts."
        ),
        subtypes=["generative"],
    ),
    CheckDefinition(
        name="references_present",
        category="workflow",
        check_fn=lambda p: dir_exists(p, "references", "inspiration"),
        pass_message="References present (references/ or inspiration/ exists)",
        fail_message=(
            "References not found. Create references/ or inspiration/ directory "
            "for visual references and inspiration."
        ),
        subtypes=["visual", "design"],
    ),
]


# =============================================================================
# Write Domain Checks
# =============================================================================

WRITE_CHECKS: list[CheckDefinition] = [
    CheckDefinition(
        name="brief_present",
        category="artifact",
        check_fn=lambda p: file_exists_any(p, "docs/brief.md"),
        pass_message="Brief exists (docs/brief.md)",
        fail_message=(
            "Brief not found. Create docs/brief.md to formalize your writing "
            "project."
        ),
        min_stage=Stage.FORMALIZE,
    ),
    CheckDefinition(
        name="outline_present",
        category="workflow",
        check_fn=lambda p: file_exists_any(p, "docs/outline.md", "outline.md"),
        pass_message="Outline present (docs/outline.md or outline.md exists)",
        fail_message=(
            "Outline not found. Create docs/outline.md or outline.md "
            "to structure your writing."
        ),
        min_stage=Stage.SHAPE,
    ),
    CheckDefinition(
        name="drafts_organized",
        category="organization",
        check_fn=lambda p: dir_exists(p, "drafts"),
        pass_message="Drafts organized (drafts/ directory exists)",
        fail_message=(
            "Drafts not organized. Create a drafts/ directory for your "
            "work-in-progress."
        ),
    ),
    CheckDefinition(
        name="citations_present",
        category="workflow",
        check_fn=lambda p: file_exists_any(
            p,
            "docs/citations.md",
            "citations.md",
            "docs/bibliography.md",
            "bibliography.md",
        ),
        pass_message="Citations present (citations or bibliography file exists)",
        fail_message=(
            "Citations not found. Create docs/citations.md or bibliography.md "
            "to track your sources."
        ),
        subtypes=["academic", "journalistic"],
    ),
]


# =============================================================================
# Learn Domain Checks
# =============================================================================

LEARN_CHECKS: list[CheckDefinition] = [
    CheckDefinition(
        name="plan_present",
        category="artifact",
        check_fn=lambda p: file_exists_any(p, "docs/plan.md"),
        pass_message="Plan exists (docs/plan.md)",
        fail_message=(
            "Plan not found. Create docs/plan.md to formalize your learning "
            "objectives."
        ),
        min_stage=Stage.FORMALIZE,
    ),
    CheckDefinition(
        name="resources_documented",
        category="workflow",
        check_fn=lambda p: file_exists_any(p, "docs/resources.md", "reading-list.md"),
        pass_message=(
            "Resources documented (docs/resources.md or reading-list.md exists)"
        ),
        fail_message=(
            "Resources not documented. Create docs/resources.md or reading-list.md "
            "to track your learning materials."
        ),
    ),
    CheckDefinition(
        name="practice_log_present",
        category="workflow",
        check_fn=lambda p: (
            file_exists_any(p, "docs/practice-log.md") or dir_exists(p, "practice")
        ),
        pass_message="Practice log present (docs/practice-log.md or practice/ exists)",
        fail_message=(
            "Practice log not found. Create docs/practice-log.md or practice/ "
            "directory to track your skill-building exercises."
        ),
        subtypes=["skill", "practice"],
    ),
    CheckDefinition(
        name="progress_tracked",
        category="workflow",
        check_fn=lambda p: file_exists_any(p, "docs/progress.md", "log.md"),
        pass_message="Progress tracked (docs/progress.md or log.md exists)",
        fail_message=(
            "Progress not tracked. Create docs/progress.md or log.md "
            "to record your learning journey."
        ),
        subtypes=["course", "exploration"],
    ),
]


# =============================================================================
# Observe Domain Checks
# =============================================================================

OBSERVE_CHECKS: list[CheckDefinition] = [
    CheckDefinition(
        name="captures_organized",
        category="organization",
        check_fn=lambda p: dir_exists(p, "captures", "inbox"),
        pass_message="Captures organized (captures/ or inbox/ exists)",
        fail_message=(
            "Captures not organized. Create captures/ or inbox/ directory "
            "to collect your observations."
        ),
    ),
    CheckDefinition(
        name="index_present",
        category="organization",
        check_fn=lambda p: file_exists_any(p, "index.md", "catalog.md"),
        pass_message="Index present (index.md or catalog.md exists)",
        fail_message=(
            "Index not found. Create index.md or catalog.md "
            "to navigate your captured materials."
        ),
    ),
]


# Update CHECKS_BY_DOMAIN with new domain checks
CHECKS_BY_DOMAIN.update({
    Domain.CREATE: CREATE_CHECKS,
    Domain.WRITE: WRITE_CHECKS,
    Domain.OBSERVE: OBSERVE_CHECKS,
    Domain.LEARN: LEARN_CHECKS,
})
