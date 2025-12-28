"""Tool runner - executes external validation tools (pytest, ruff, mypy)."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToolResult:
    """Result of running an external tool."""

    tool: str
    success: bool
    output: str
    error: str
    return_code: int


def run_tool(
    command: list[str],
    tool_name: str,
    cwd: Path,
    timeout: int = 300,
) -> ToolResult:
    """Run an external tool and capture its output.

    Args:
        command: Command and arguments to run.
        tool_name: Human-readable tool name for reporting.
        cwd: Working directory to run the command in.
        timeout: Maximum seconds to wait (default 5 minutes).

    Returns:
        ToolResult with success status and output.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return ToolResult(
            tool=tool_name,
            success=result.returncode == 0,
            output=result.stdout,
            error=result.stderr,
            return_code=result.returncode,
        )
    except subprocess.TimeoutExpired:
        return ToolResult(
            tool=tool_name,
            success=False,
            output="",
            error=f"{tool_name} timed out after {timeout} seconds",
            return_code=-1,
        )
    except FileNotFoundError:
        return ToolResult(
            tool=tool_name,
            success=False,
            output="",
            error=f"{tool_name} not found. Is it installed?",
            return_code=-1,
        )


def run_pytest(project_root: Path) -> ToolResult:
    """Run pytest in the project directory.

    Args:
        project_root: Project directory containing tests.

    Returns:
        ToolResult indicating if tests passed.
    """
    # Try poetry run pytest first, fall back to pytest
    commands = [
        ["poetry", "run", "pytest", "--tb=short", "-q"],
        ["pytest", "--tb=short", "-q"],
    ]

    for cmd in commands:
        result = run_tool(cmd, "pytest", project_root)
        if result.return_code != -1:  # Tool was found
            return result

    return ToolResult(
        tool="pytest",
        success=False,
        output="",
        error="pytest not found. Install with: pip install pytest",
        return_code=-1,
    )


def run_ruff(project_root: Path) -> ToolResult:
    """Run ruff linter in the project directory.

    Args:
        project_root: Project directory to lint.

    Returns:
        ToolResult indicating if linting passed.
    """
    commands = [
        ["poetry", "run", "ruff", "check", "."],
        ["ruff", "check", "."],
    ]

    for cmd in commands:
        result = run_tool(cmd, "ruff", project_root)
        if result.return_code != -1:
            return result

    return ToolResult(
        tool="ruff",
        success=False,
        output="",
        error="ruff not found. Install with: pip install ruff",
        return_code=-1,
    )


def run_mypy(project_root: Path) -> ToolResult:
    """Run mypy type checker in the project directory.

    Args:
        project_root: Project directory to type check.

    Returns:
        ToolResult indicating if type checking passed.
    """
    commands = [
        ["poetry", "run", "mypy", "."],
        ["mypy", "."],
    ]

    for cmd in commands:
        result = run_tool(cmd, "mypy", project_root)
        if result.return_code != -1:
            return result

    return ToolResult(
        tool="mypy",
        success=False,
        output="",
        error="mypy not found. Install with: pip install mypy",
        return_code=-1,
    )
