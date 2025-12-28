"""Load and parse pyproject.toml files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import tomllib


def load_pyproject(project_root: Path) -> dict[str, Any] | None:
    """Load pyproject.toml if it exists.

    Args:
        project_root: Project directory.

    Returns:
        Parsed TOML data, or None if file doesn't exist.
    """
    path = project_root / "pyproject.toml"
    if not path.exists():
        return None

    with open(path, "rb") as f:
        return tomllib.load(f)


def get_dependencies(project_root: Path) -> set[str]:
    """Get all dependencies from pyproject.toml.

    Includes both main dependencies and dev dependencies.

    Args:
        project_root: Project directory.

    Returns:
        Set of dependency names (lowercase).
    """
    data = load_pyproject(project_root)
    if not data:
        return set()

    deps: set[str] = set()
    poetry = data.get("tool", {}).get("poetry", {})

    # Main dependencies
    main_deps = poetry.get("dependencies", {})
    deps.update(k.lower() for k in main_deps.keys())

    # Dev dependencies (Poetry 1.2+ style)
    groups = poetry.get("group", {})
    for group in groups.values():
        group_deps = group.get("dependencies", {})
        deps.update(k.lower() for k in group_deps.keys())

    # Legacy dev-dependencies
    legacy_dev = poetry.get("dev-dependencies", {})
    deps.update(k.lower() for k in legacy_dev.keys())

    return deps


def get_poetry_scripts(project_root: Path) -> dict[str, str]:
    """Get console script entry points from pyproject.toml.

    Args:
        project_root: Project directory.

    Returns:
        Dict mapping script names to entry points.
    """
    data = load_pyproject(project_root)
    if not data:
        return {}

    poetry = data.get("tool", {}).get("poetry", {})
    return poetry.get("scripts", {})
