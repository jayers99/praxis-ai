"""Infrastructure helpers for audit checks."""

from __future__ import annotations

from pathlib import Path


def dir_exists(project_root: Path, *paths: str) -> bool:
    """Check if any of the specified directories exist.

    Args:
        project_root: Project root directory.
        *paths: One or more directory paths to check (relative to project root).

    Returns:
        True if any of the directories exist, False otherwise.
    """
    return any((project_root / p).is_dir() for p in paths)


def file_exists_any(project_root: Path, *paths: str) -> bool:
    """Check if any of the specified files exist.

    Args:
        project_root: Project root directory.
        *paths: One or more file paths to check (relative to project root).

    Returns:
        True if any of the files exist, False otherwise.
    """
    return any((project_root / p).is_file() for p in paths)
