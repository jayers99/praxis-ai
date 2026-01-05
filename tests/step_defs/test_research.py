"""Step definitions for research.feature."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/research.feature")


@given("a valid research corpus exists")
def create_corpus(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a temporary corpus directory."""
    corpus_path = tmp_path / "corpus"
    corpus_path.mkdir()
    # Add a sample file
    (corpus_path / "sample.md").write_text("# Sample Research\nContent here.")
    context["corpus_path"] = corpus_path
    context["working_dir"] = tmp_path


@given(parsers.parse('an active research session exists at phase "{phase}"'))
def create_active_session(
    tmp_path: Path, context: dict[str, Any], phase: str
) -> None:
    """Create a session at the specified phase."""
    context["working_dir"] = tmp_path

    # Create corpus
    corpus_path = tmp_path / "corpus"
    corpus_path.mkdir()
    (corpus_path / "sample.md").write_text("# Sample\nContent.")
    context["corpus_path"] = corpus_path

    # Create session.yaml at the specified phase
    from datetime import datetime

    import yaml

    # Build phase history for current phase
    phases = ["intake", "rtc", "idas", "sad", "ccr", "asr", "synthesis"]
    phase_history = []
    now = datetime.now().isoformat()

    for p in phases:
        phase_history.append({"phase": p, "timestamp": now})
        if p == phase:
            break

    session_data = {
        "id": f"test-session-{datetime.now().strftime('%Y%m%d')}",
        "topic": "Test Topic",
        "corpus_path": str(corpus_path),
        "tier": 2,
        "phase": phase,
        "status": "active",
        "created_at": now,
        "updated_at": now,
        "phase_history": phase_history,
    }

    session_path = tmp_path / "session.yaml"
    session_path.write_text(yaml.dump(session_data))


@given("no research session exists in the working directory")
def no_session_exists(tmp_path: Path, context: dict[str, Any]) -> None:
    """Ensure no session exists."""
    context["working_dir"] = tmp_path
    session_path = tmp_path / "session.yaml"
    if session_path.exists():
        session_path.unlink()


@when(
    parsers.parse(
        'I run praxis research init with topic "{topic}" and corpus path'
    )
)
def run_research_init(
    cli_runner: CliRunner, context: dict[str, Any], topic: str
) -> None:
    """Run research init command."""
    working_dir = context["working_dir"]
    corpus_path = context["corpus_path"]
    result = cli_runner.invoke(
        app,
        [
            "research",
            "init",
            "--topic",
            topic,
            "--corpus",
            str(corpus_path),
            str(working_dir),
        ],
    )
    context["result"] = result


@when("I run praxis research init without topic")
def run_research_init_no_topic(
    cli_runner: CliRunner, context: dict[str, Any]
) -> None:
    """Run research init command without topic."""
    working_dir = context["working_dir"]
    corpus_path = context["corpus_path"]
    result = cli_runner.invoke(
        app,
        [
            "research",
            "init",
            "--corpus",
            str(corpus_path),
            str(working_dir),
        ],
    )
    context["result"] = result


@when("I run praxis research status")
def run_research_status(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run research status command."""
    working_dir = context["working_dir"]
    result = cli_runner.invoke(app, ["research", "status", str(working_dir)])
    context["result"] = result


@when("I run praxis research status with json flag")
def run_research_status_json(
    cli_runner: CliRunner, context: dict[str, Any]
) -> None:
    """Run research status command with JSON output."""
    working_dir = context["working_dir"]
    result = cli_runner.invoke(
        app, ["research", "status", str(working_dir), "--json"]
    )
    context["result"] = result


@when("I run praxis research run")
def run_research_run(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run research run command."""
    working_dir = context["working_dir"]
    result = cli_runner.invoke(app, ["research", "run", str(working_dir)])
    context["result"] = result


@when(parsers.parse('I run praxis research approve with rationale "{rationale}"'))
def run_research_approve(
    cli_runner: CliRunner, context: dict[str, Any], rationale: str
) -> None:
    """Run research approve command."""
    working_dir = context["working_dir"]
    result = cli_runner.invoke(
        app,
        ["research", "approve", "--rationale", rationale, str(working_dir)],
    )
    context["result"] = result


@when(parsers.parse('I run praxis research reject with rationale "{rationale}"'))
def run_research_reject(
    cli_runner: CliRunner, context: dict[str, Any], rationale: str
) -> None:
    """Run research reject command."""
    working_dir = context["working_dir"]
    result = cli_runner.invoke(
        app,
        ["research", "reject", "--rationale", rationale, str(working_dir)],
    )
    context["result"] = result


@then("a session.yaml file is created")
def check_session_file_created(context: dict[str, Any]) -> None:
    """Verify session.yaml was created."""
    working_dir = context["working_dir"]
    session_path = working_dir / "session.yaml"
    assert session_path.exists(), f"session.yaml not found at {session_path}"


@then(parsers.parse('the session phase is now "{phase}"'))
def check_session_phase(context: dict[str, Any], phase: str) -> None:
    """Verify the session is at the expected phase."""
    import yaml

    working_dir = context["working_dir"]
    session_path = working_dir / "session.yaml"
    data = yaml.safe_load(session_path.read_text())
    assert data["phase"] == phase, f"Expected phase {phase}, got {data['phase']}"


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
