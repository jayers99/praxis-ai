"""Load and parse pyproject.toml files."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, cast

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[import-not-found]


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
        return cast(dict[str, Any], tomllib.load(f))


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

    # PEP 621 format ([project] dependencies)
    project = data.get("project", {})
    for dep_str in project.get("dependencies", []):
        # PEP 508 format: "package>=1.0" -> "package"
        name = dep_str.split(">")[0].split("<")[0].split("=")[0].split("!")[0].split("[")[0].strip()
        if name:
            deps.add(name.lower())

    # PEP 735 dependency-groups
    dep_groups = data.get("dependency-groups", {})
    for group_deps in dep_groups.values():
        for dep_str in group_deps:
            if isinstance(dep_str, str):
                name = dep_str.split(">")[0].split("<")[0].split("=")[0].split("!")[0].split("[")[0].strip()
                if name:
                    deps.add(name.lower())

    # Legacy Poetry format ([tool.poetry] dependencies)
    poetry = data.get("tool", {}).get("poetry", {})
    main_deps = poetry.get("dependencies", {})
    deps.update(k.lower() for k in main_deps)

    groups = poetry.get("group", {})
    for group in groups.values():
        group_deps = group.get("dependencies", {})
        deps.update(k.lower() for k in group_deps)

    legacy_dev = poetry.get("dev-dependencies", {})
    deps.update(k.lower() for k in legacy_dev)

    return deps


def get_console_scripts(project_root: Path) -> dict[str, str]:
    """Get console script entry points from pyproject.toml.

    Supports both PEP 621 ([project.scripts]) and Poetry ([tool.poetry.scripts]).

    Args:
        project_root: Project directory.

    Returns:
        Dict mapping script names to entry points.
    """
    data = load_pyproject(project_root)
    if not data:
        return {}

    # PEP 621 format
    project_scripts = data.get("project", {}).get("scripts", {})
    if project_scripts:
        return cast(dict[str, str], project_scripts)

    # Legacy Poetry format
    poetry = data.get("tool", {}).get("poetry", {})
    return cast(dict[str, str], poetry.get("scripts", {}))


# Backward-compatible alias
get_poetry_scripts = get_console_scripts
