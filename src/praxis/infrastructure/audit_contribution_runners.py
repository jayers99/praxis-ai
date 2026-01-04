"""Infrastructure for running extension-contributed audit checks."""

from __future__ import annotations

import re
from pathlib import Path


def run_file_exists_check(project_root: Path, path: str) -> bool:
    """Check if a file exists at the specified path.

    Args:
        project_root: Project root directory.
        path: Relative path to the file.

    Returns:
        True if file exists, False otherwise.
    """
    file_path = project_root / path
    return file_path.is_file()


def run_dir_exists_check(project_root: Path, path: str) -> bool:
    """Check if a directory exists at the specified path.

    Args:
        project_root: Project root directory.
        path: Relative path to the directory.

    Returns:
        True if directory exists, False otherwise.
    """
    dir_path = project_root / path
    return dir_path.is_dir()


def run_file_contains_check(project_root: Path, path: str, pattern: str) -> bool:
    """Check if a file contains content matching the given regex pattern.

    Args:
        project_root: Project root directory.
        path: Relative path to the file.
        pattern: Regex pattern to search for.

    Returns:
        True if file exists and contains the pattern, False otherwise.

    Raises:
        re.error: If the pattern is invalid regex syntax.
    """
    file_path = project_root / path
    
    if not file_path.is_file():
        return False
    
    try:
        # Compile the pattern to validate it
        compiled_pattern = re.compile(pattern)
        
        # Read file and search for pattern
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        return compiled_pattern.search(content) is not None
    except (OSError, UnicodeDecodeError):
        # File can't be read - treat as check failure
        return False
