"""Safe file writing utilities."""

from __future__ import annotations

from pathlib import Path


def write_file(
    path: Path, content: str, force: bool = False
) -> tuple[bool, str | None]:
    """Write content to a file, respecting force flag.

    Args:
        path: Path to the file to write.
        content: Content to write.
        force: If True, overwrite existing files. If False, error on existing.

    Returns:
        Tuple of (success, error_message). error_message is None on success.
    """
    if path.exists() and not force:
        return False, f"File exists: {path}. Use --force to overwrite."

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return True, None
    except OSError as e:
        return False, f"Failed to write {path}: {e}"


def check_files_exist(paths: list[Path]) -> list[Path]:
    """Check which files already exist.

    Args:
        paths: List of paths to check.

    Returns:
        List of paths that exist.
    """
    return [p for p in paths if p.exists()]
