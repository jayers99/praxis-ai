"""Audit check definitions by domain."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal

from praxis.domain.domains import Domain
from praxis.domain.stages import Stage
from praxis.infrastructure.audit_helpers import dir_exists, file_exists_any
from praxis.infrastructure.pyproject_loader import (
    get_dependencies,
    get_poetry_scripts,
    load_pyproject,
)


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


# =============================================================================
# CLI Subtype Checks (code.cli)
# =============================================================================


def _cli_has_entry_point(project_root: Path) -> bool:
    """Check for CLI entry point (console script or __main__.py).

    A CLI entry point is considered present if:
    - pyproject.toml contains [tool.poetry.scripts] entries, OR
    - A __main__.py file exists in the main package under src/
    """
    # Check for console script
    if get_poetry_scripts(project_root):
        return True
    # Check for __main__.py
    return _has_main_module(project_root)


def _cli_has_help_flag(project_root: Path) -> bool:
    """Check for --help flag support in CLI files.

    This is a heuristic check that looks for common patterns indicating
    help flag support (Typer, argparse, click). A more thorough check
    would require running the CLI, but this gives a good signal.
    """
    src_dir = project_root / "src"
    if not src_dir.exists():
        return False

    # Look for CLI files
    cli_files: list[Path] = []
    for pattern in ["**/cli.py", "**/__main__.py"]:
        cli_files.extend(src_dir.glob(pattern))

    if not cli_files:
        return False

    # Check for patterns that indicate help support
    help_patterns = [
        "typer",  # Typer auto-generates help
        "argparse",  # argparse has default help
        "click",  # click has default help
        "--help",  # Explicit help flag
        "help=",  # Help parameter
    ]

    for cli_file in cli_files:
        try:
            content = cli_file.read_text().lower()
            if any(pattern in content for pattern in help_patterns):
                return True
        except (OSError, UnicodeDecodeError):
            # Skip files that can't be read (permissions, encoding issues)
            continue

    return False


def _cli_has_version_flag(project_root: Path) -> bool:
    """Check for --version flag support.

    Looks for patterns indicating version flag is implemented.
    """
    src_dir = project_root / "src"
    if not src_dir.exists():
        return False

    # Look for CLI files
    cli_files: list[Path] = []
    for pattern in ["**/cli.py", "**/__main__.py"]:
        cli_files.extend(src_dir.glob(pattern))

    if not cli_files:
        return False

    # Check for version-related patterns (pre-lowercase for efficiency)
    version_patterns = [
        "--version",
        "version_callback",
        "__version__",
        "version=",
    ]

    for cli_file in cli_files:
        try:
            content = cli_file.read_text().lower()
            if any(pattern in content for pattern in version_patterns):
                return True
        except (OSError, UnicodeDecodeError):
            # Skip files that can't be read (permissions, encoding issues)
            continue

    return False


CLI_CHECKS: list[CheckDefinition] = [
    CheckDefinition(
        name="cli_entry_point_exists",
        category="cli",
        check_fn=_cli_has_entry_point,
        pass_message="CLI entry point exists (console script or __main__.py)",
        fail_message=(
            "CLI entry point not found. Add [tool.poetry.scripts] or __main__.py"
        ),
        subtypes=["cli"],
    ),
    CheckDefinition(
        name="cli_help_present",
        category="cli",
        check_fn=_cli_has_help_flag,
        pass_message="--help flag support detected",
        fail_message="--help flag support not detected (add Typer, argparse, or click)",
        subtypes=["cli"],
    ),
    CheckDefinition(
        name="cli_version_flag",
        category="cli",
        check_fn=_cli_has_version_flag,
        pass_message="--version flag support detected",
        fail_message="--version flag not detected (add version callback or flag)",
        subtypes=["cli"],
    ),
]

# Add CLI checks to CODE_CHECKS
CODE_CHECKS.extend(CLI_CHECKS)


# =============================================================================
# Library Subtype Checks (code.library)
# =============================================================================


def _library_has_exports(project_root: Path) -> bool:
    """Check for library exports definition (__all__ or pyproject.toml).

    A library's public API is considered defined if:
    - __init__.py contains __all__ definition, OR
    - pyproject.toml has explicit packages/modules configuration
    """
    # Check for __all__ in __init__.py
    src_dir = project_root / "src"
    if src_dir.exists():
        packages = [
            d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith("_")
        ]
        if packages:
            init_file = packages[0] / "__init__.py"
            if init_file.exists():
                try:
                    content = init_file.read_text()
                    if "__all__" in content:
                        return True
                except (OSError, UnicodeDecodeError):
                    pass

    # Check for explicit package configuration in pyproject.toml
    data = load_pyproject(project_root)
    if data:
        poetry = data.get("tool", {}).get("poetry", {})
        # Explicit packages or modules indicate intentional exports
        if poetry.get("packages") or poetry.get("modules"):
            return True

    return False


def _library_has_version(project_root: Path) -> bool:
    """Check for version specification (__version__ and pyproject.toml).

    A library version is considered properly specified if:
    - pyproject.toml contains version field AND
    - __init__.py contains __version__ variable
    """
    # Check pyproject.toml version
    data = load_pyproject(project_root)
    if not data:
        return False

    poetry = data.get("tool", {}).get("poetry", {})
    if not poetry.get("version"):
        return False

    # Check for __version__ in package __init__.py
    src_dir = project_root / "src"
    if not src_dir.exists():
        return False

    packages = [
        d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith("_")
    ]
    if not packages:
        return False

    init_file = packages[0] / "__init__.py"
    if not init_file.exists():
        return False

    try:
        content = init_file.read_text()
        return "__version__" in content
    except (OSError, UnicodeDecodeError):
        return False


def _library_has_docstrings(project_root: Path) -> bool:
    """Check for docstrings on public functions in __init__.py.

    For formalize stage, we check if public exports have docstrings.
    This is a heuristic check looking for common docstring patterns.
    """
    src_dir = project_root / "src"
    if not src_dir.exists():
        return False

    packages = [
        d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith("_")
    ]
    if not packages:
        return False

    init_file = packages[0] / "__init__.py"
    if not init_file.exists():
        return False

    try:
        content = init_file.read_text()
        # Look for docstring patterns (triple quotes)
        # This is a heuristic - real check would parse AST
        has_exports = "__all__" in content or "def " in content or "class " in content
        has_docstrings = '"""' in content or "'''" in content
        return has_exports and has_docstrings
    except (OSError, UnicodeDecodeError):
        return False


def _library_has_docs_site(project_root: Path) -> bool:
    """Check for documentation site (sphinx/mkdocs).

    For commit+ stages, we expect a proper docs site setup.
    """
    # Check for common docs directories and config files
    docs_indicators = [
        project_root / "docs" / "conf.py",  # Sphinx
        project_root / "mkdocs.yml",  # MkDocs
        project_root / "docs" / "index.md",  # MkDocs
        project_root / "docs" / "index.rst",  # Sphinx
    ]
    return any(indicator.exists() for indicator in docs_indicators)


def _library_has_changelog(project_root: Path) -> bool:
    """Check for changelog file.

    Looks for common changelog file names.
    """
    return file_exists_any(
        project_root,
        "CHANGELOG.md",
        "CHANGELOG.rst",
        "CHANGELOG.txt",
        "HISTORY.md",
        "CHANGES.md",
    )


LIBRARY_CHECKS: list[CheckDefinition] = [
    CheckDefinition(
        name="library_exports_defined",
        category="library",
        check_fn=_library_has_exports,
        pass_message="Library exports defined (__all__ or pyproject.toml packages)",
        fail_message=(
            "Library exports not defined. Add __all__ to __init__.py or configure "
            "packages in pyproject.toml"
        ),
        subtypes=["library"],
    ),
    CheckDefinition(
        name="library_version_specified",
        category="library",
        check_fn=_library_has_version,
        pass_message="Version specified (__version__ and pyproject.toml)",
        fail_message=(
            "Version not properly specified. Add __version__ to __init__.py and "
            "version to pyproject.toml"
        ),
        subtypes=["library"],
    ),
    CheckDefinition(
        name="library_public_api_documented",
        category="library",
        check_fn=_library_has_docstrings,
        pass_message="Public API documented (docstrings present)",
        fail_message="Public API not documented. Add docstrings to public functions/classes",
        subtypes=["library"],
        min_stage=Stage.FORMALIZE,
    ),
    CheckDefinition(
        name="library_docs_site",
        category="library",
        check_fn=_library_has_docs_site,
        pass_message="Documentation site configured (sphinx/mkdocs)",
        fail_message="Documentation site not found. Set up sphinx or mkdocs",
        subtypes=["library"],
        min_stage=Stage.COMMIT,
    ),
    CheckDefinition(
        name="library_changelog_exists",
        category="library",
        check_fn=_library_has_changelog,
        pass_message="Changelog exists (CHANGELOG.md or equivalent)",
        fail_message="Changelog not found. Create CHANGELOG.md to track changes",
        subtypes=["library"],
    ),
]

# Add LIBRARY checks to CODE_CHECKS
CODE_CHECKS.extend(LIBRARY_CHECKS)


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
