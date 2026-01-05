"""Step definitions for library.feature."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/library.feature")


# Use the actual research library from the repository
LIBRARY_PATH = Path(__file__).parent.parent.parent / "research-library"


@given("the research library exists with cataloged artifacts")
def library_exists(context: dict[str, Any]) -> None:
    """Ensure the research library exists."""
    assert LIBRARY_PATH.exists(), f"Research library not found at {LIBRARY_PATH}"
    catalog_path = LIBRARY_PATH / "CATALOG.md"
    assert catalog_path.exists(), f"CATALOG.md not found at {catalog_path}"
    context["library_path"] = LIBRARY_PATH


@when(parsers.parse('I run praxis library query "{question}"'))
def run_library_query(
    cli_runner: CliRunner, context: dict[str, Any], question: str
) -> None:
    """Run library query command."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        ["library", "query", question, "--library-path", str(library_path)],
    )
    context["result"] = result


@when("I run praxis library query with empty string")
def run_library_query_empty(
    cli_runner: CliRunner, context: dict[str, Any]
) -> None:
    """Run library query command with empty string."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        ["library", "query", "", "--library-path", str(library_path)],
    )
    context["result"] = result


@when(parsers.parse('I run praxis library query "{question}" with json flag'))
def run_library_query_json(
    cli_runner: CliRunner, context: dict[str, Any], question: str
) -> None:
    """Run library query command with JSON output."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        [
            "library",
            "query",
            question,
            "--library-path",
            str(library_path),
            "--json",
        ],
    )
    context["result"] = result


@when(parsers.parse('I run praxis library search with keyword "{keyword}"'))
def run_library_search(
    cli_runner: CliRunner, context: dict[str, Any], keyword: str
) -> None:
    """Run library search command."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        [
            "library",
            "search",
            "--keyword",
            keyword,
            "--library-path",
            str(library_path),
        ],
    )
    context["result"] = result


@when(parsers.parse('I run praxis library cite "{artifact_id}"'))
def run_library_cite(
    cli_runner: CliRunner, context: dict[str, Any], artifact_id: str
) -> None:
    """Run library cite command."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        ["library", "cite", artifact_id, "--library-path", str(library_path)],
    )
    context["result"] = result


@when("I run praxis library check-orphans")
def run_library_check_orphans(
    cli_runner: CliRunner, context: dict[str, Any]
) -> None:
    """Run library check-orphans command."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        ["library", "check-orphans", "--library-path", str(library_path)],
    )
    context["result"] = result


@when(parsers.parse("I run praxis library check-stale with days {days:d}"))
def run_library_check_stale(
    cli_runner: CliRunner, context: dict[str, Any], days: int
) -> None:
    """Run library check-stale command."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        [
            "library",
            "check-stale",
            "--days",
            str(days),
            "--library-path",
            str(library_path),
        ],
    )
    context["result"] = result


@when("I run praxis library reindex")
def run_library_reindex(
    cli_runner: CliRunner, context: dict[str, Any]
) -> None:
    """Run library reindex command."""
    library_path = context["library_path"]
    result = cli_runner.invoke(
        app,
        ["library", "reindex", "--library-path", str(library_path)],
    )
    context["result"] = result


@then(parsers.parse('the JSON output should contain "{key}"'))
def check_json_contains_key(context: dict[str, Any], key: str) -> None:
    """Verify the JSON output contains the specified key."""
    result = context["result"]
    try:
        output_data = json.loads(result.output)
        assert key in output_data, (
            f"Expected key '{key}' in JSON output. "
            f"Got keys: {list(output_data.keys())}"
        )
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON output: {e}. Output: {result.output}")
