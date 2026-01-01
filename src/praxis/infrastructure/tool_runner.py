"""Tool runner - executes external validation tools (pytest, ruff, mypy, coverage)."""

from __future__ import annotations

import re
import subprocess
import sys
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


def _output_indicates_missing_tool(result: ToolResult) -> bool:
    """Heuristic: detect cases where a wrapper exists but the underlying tool isn't available.

    This module tries commands in a preferred order (e.g. `poetry run ...` then
    `python -m ...` then bare executable). If a command fails because the underlying
    tool isn't installed, we treat that failure as "try the next command" rather than
    a hard failure.
    """

    combined = (result.output + "\n" + result.error).lower()
    return (
        "command not found" in combined
        or "no module named" in combined
        or "not installed" in combined
        or "is not installed" in combined
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
        [sys.executable, "-m", "pytest", "--tb=short", "-q"],
        ["pytest", "--tb=short", "-q"],
    ]

    for cmd in commands:
        result = run_tool(cmd, "pytest", project_root)
        if result.return_code == -1:
            continue
        if result.success:
            return result
        if _output_indicates_missing_tool(result):
            continue
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
        [sys.executable, "-m", "ruff", "check", "."],
        ["ruff", "check", "."],
    ]

    for cmd in commands:
        result = run_tool(cmd, "ruff", project_root)
        if result.return_code == -1:
            continue
        if result.success:
            return result
        if _output_indicates_missing_tool(result):
            continue
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
        [sys.executable, "-m", "mypy", "."],
        ["mypy", "."],
    ]

    for cmd in commands:
        result = run_tool(cmd, "mypy", project_root)
        if result.return_code == -1:
            continue
        if result.success:
            return result
        if _output_indicates_missing_tool(result):
            continue
        return result

    return ToolResult(
        tool="mypy",
        success=False,
        output="",
        error="mypy not found. Install with: pip install mypy",
        return_code=-1,
    )


@dataclass
class CoverageResult:
    """Result of running coverage check."""

    tool: str
    success: bool
    coverage_percent: float | None
    threshold: int
    output: str
    error: str


def parse_coverage_percent(output: str) -> float | None:
    """Parse coverage percentage from pytest-cov output.

    Looks for patterns like:
    - "TOTAL ... 85%" (pytest-cov summary line)
    - "Total coverage: 85.00%"
    - "Coverage: 85%"

    Args:
        output: Combined stdout/stderr from pytest-cov.

    Returns:
        Coverage percentage as float, or None if not found.
    """
    # Pattern for pytest-cov TOTAL line: "TOTAL    123    45    85%"
    match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
    if match:
        return float(match.group(1))

    # Pattern for "X%" at end of a line with TOTAL
    match = re.search(r"TOTAL.*?(\d+(?:\.\d+)?)\s*%", output)
    if match:
        return float(match.group(1))

    # Generic pattern for coverage percentage
    match = re.search(r"(\d+(?:\.\d+)?)\s*%\s*(?:coverage|covered)", output, re.I)
    if match:
        return float(match.group(1))

    return None


def run_coverage(project_root: Path, threshold: int) -> CoverageResult:
    """Run pytest with coverage and check against threshold.

    Args:
        project_root: Project directory containing tests.
        threshold: Minimum coverage percentage required (0-100).

    Returns:
        CoverageResult with coverage percentage and pass/fail status.
    """
    # Try poetry run pytest with coverage first, fall back to pytest
    commands = [
        ["poetry", "run", "pytest", "--cov", "--cov-report=term", "-q"],
        [
            sys.executable,
            "-m",
            "pytest",
            "--cov",
            "--cov-report=term",
            "-q",
        ],
        ["pytest", "--cov", "--cov-report=term", "-q"],
    ]

    for cmd in commands:
        result = run_tool(cmd, "coverage", project_root)
        if result.return_code == -1:
            continue

        if not result.success and _output_indicates_missing_tool(result):
            continue

        # Tool was found (or tests ran), parse coverage
        combined_output = result.output + result.error
        coverage_pct = parse_coverage_percent(combined_output)

        if coverage_pct is None:
            return CoverageResult(
                tool="coverage",
                success=False,
                coverage_percent=None,
                threshold=threshold,
                output=result.output,
                error="Could not parse coverage percentage from output",
            )

        meets_threshold = coverage_pct >= threshold
        return CoverageResult(
            tool="coverage",
            success=meets_threshold,
            coverage_percent=coverage_pct,
            threshold=threshold,
            output=result.output,
            error="" if meets_threshold else (
                f"Coverage {coverage_pct:.0f}% is below threshold {threshold}%"
            ),
        )

    return CoverageResult(
        tool="coverage",
        success=False,
        coverage_percent=None,
        threshold=threshold,
        output="",
        error="pytest-cov not found. Install with: pip install pytest-cov",
    )
