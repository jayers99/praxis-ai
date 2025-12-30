"""Git operations for cloning and updating repositories."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from pydantic import BaseModel


class CloneResult(BaseModel):
    """Result of a git clone operation."""

    success: bool
    path: Path | None = None
    error: str | None = None


def clone_repo(repo_url: str, target_path: Path) -> CloneResult:
    """Clone a git repository to the specified path.

    Args:
        repo_url: URL of the git repository
        target_path: Path where the repo should be cloned

    Returns:
        CloneResult indicating success or failure
    """
    if target_path.exists():
        return CloneResult(
            success=False,
            path=target_path,
            error=f"Target path already exists: {target_path}",
        )

    try:
        # Ensure parent directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ["git", "clone", repo_url, str(target_path)],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
        )

        if result.returncode == 0:
            return CloneResult(success=True, path=target_path)
        else:
            return CloneResult(
                success=False,
                error=result.stderr.strip() or "Clone failed with no error message",
            )

    except subprocess.TimeoutExpired:
        return CloneResult(
            success=False,
            error="Clone timed out after 120 seconds",
        )
    except FileNotFoundError:
        return CloneResult(
            success=False,
            error="git command not found. Please install git.",
        )
    except Exception as e:
        return CloneResult(
            success=False,
            error=str(e),
        )


def update_repo(repo_path: Path) -> CloneResult:
    """Update (git pull) a repository.

    Args:
        repo_path: Path to the repository

    Returns:
        CloneResult indicating success or failure
    """
    if not repo_path.exists():
        return CloneResult(
            success=False,
            error=f"Repository not found: {repo_path}",
        )

    if not (repo_path / ".git").exists():
        return CloneResult(
            success=False,
            error=f"Not a git repository: {repo_path}",
        )

    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "pull", "--ff-only"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            return CloneResult(success=True, path=repo_path)
        else:
            return CloneResult(
                success=False,
                path=repo_path,
                error=result.stderr.strip() or "Pull failed",
            )

    except subprocess.TimeoutExpired:
        return CloneResult(
            success=False,
            path=repo_path,
            error="Pull timed out after 60 seconds",
        )
    except Exception as e:
        return CloneResult(
            success=False,
            path=repo_path,
            error=str(e),
        )


def remove_repo(repo_path: Path) -> CloneResult:
    """Remove a cloned repository.

    Args:
        repo_path: Path to the repository to remove

    Returns:
        CloneResult indicating success or failure
    """
    if not repo_path.exists():
        return CloneResult(
            success=False,
            error=f"Path does not exist: {repo_path}",
        )

    try:
        shutil.rmtree(repo_path)
        return CloneResult(success=True, path=repo_path)
    except Exception as e:
        return CloneResult(
            success=False,
            path=repo_path,
            error=str(e),
        )
