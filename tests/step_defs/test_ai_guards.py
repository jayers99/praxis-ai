"""Step definitions for AI Guards BDD tests."""

import subprocess
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/ai_guards.feature")


@given("I have initialized a Praxis workspace", target_fixture="workspace_path")
def initialized_workspace(tmp_path):
    """Initialize a Praxis workspace."""
    return tmp_path


@given("I have a code project", target_fixture="project_path")
def code_project(tmp_path):
    """Create a code project with praxis.yaml."""
    project_dir = tmp_path / "test-project"
    project_dir.mkdir()

    # Create praxis.yaml
    praxis_yaml = project_dir / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
""",
        encoding="utf-8",
    )

    return project_dir


@given("I have a code project with no AI guards configured", target_fixture="project_path")
def code_project_no_guards(tmp_path):
    """Create a code project without AI guards."""
    project_dir = tmp_path / "test-project"
    project_dir.mkdir()

    # Create praxis.yaml
    praxis_yaml = project_dir / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
""",
        encoding="utf-8",
    )

    return project_dir


@given(
    parsers.parse('the project has a "{filepath}" file with content:\n{content}'),
    target_fixture="guard_file",
)
def project_guard_file_with_content(project_path, filepath, content):
    """Create a project guard file with specific content."""
    guard_path = project_path / filepath
    guard_path.parent.mkdir(parents=True, exist_ok=True)
    guard_path.write_text(content.strip(), encoding="utf-8")
    return guard_path


@given(
    parsers.parse('the project has a "{filepath}" file with guards'),
    target_fixture="guard_file",
)
def project_guard_file_with_guards(project_path, filepath):
    """Create a project guard file with sample guards."""
    guard_path = project_path / filepath
    guard_path.parent.mkdir(parents=True, exist_ok=True)
    guard_path.write_text(
        "# Code Domain Guards\nUse TypeScript\n",
        encoding="utf-8",
    )
    return guard_path


@when(parsers.parse('I run "{command}"'), target_fixture="command_result")
def run_command(project_path, command):
    """Run a praxis command in the project directory."""
    # Parse command to extract arguments
    parts = command.split()
    cmd_parts = ["praxis"] + parts[1:]  # Skip "praxis" prefix

    # Run command
    result = subprocess.run(
        cmd_parts,
        cwd=project_path,
        capture_output=True,
        text=True,
    )

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


@then("the command should succeed")
def command_succeeds(command_result):
    """Check that command succeeded."""
    assert command_result["returncode"] == 0, (
        f"Command failed with:\n{command_result['stderr']}"
    )


@then("a CLAUDE.md file should be created")
def claude_file_created(project_path):
    """Check that CLAUDE.md was created."""
    claude_file = project_path / "CLAUDE.md"
    assert claude_file.exists(), "CLAUDE.md was not created"


@then("no CLAUDE.md file should be created")
def no_claude_file_created(project_path):
    """Check that CLAUDE.md was not created."""
    claude_file = project_path / "CLAUDE.md"
    assert not claude_file.exists(), "CLAUDE.md should not have been created"


@then("a .github/copilot-instructions.md file should be created")
def copilot_file_created(project_path):
    """Check that copilot-instructions.md was created."""
    copilot_file = project_path / ".github" / "copilot-instructions.md"
    assert copilot_file.exists(), "copilot-instructions.md was not created"


@then("no .github/copilot-instructions.md file should be created")
def no_copilot_file_created(project_path):
    """Check that copilot-instructions.md was not created."""
    copilot_file = project_path / ".github" / "copilot-instructions.md"
    assert not copilot_file.exists(), "copilot-instructions.md should not be created"


@then("a GEMINI.md file should be created")
def gemini_file_created(project_path):
    """Check that GEMINI.md was created."""
    gemini_file = project_path / "GEMINI.md"
    assert gemini_file.exists(), "GEMINI.md was not created"


@then("no GEMINI.md file should be created")
def no_gemini_file_created(project_path):
    """Check that GEMINI.md was not created."""
    gemini_file = project_path / "GEMINI.md"
    assert not gemini_file.exists(), "GEMINI.md should not have been created"


@then("no guard files should be created")
def no_guard_files_created(project_path):
    """Check that no guard files were created."""
    assert not (project_path / "CLAUDE.md").exists()
    assert not (project_path / "GEMINI.md").exists()
    copilot_file = project_path / ".github" / "copilot-instructions.md"
    assert not copilot_file.exists()


@then(parsers.parse('the file should contain "{text}"'))
def claude_file_contains(project_path, text):
    """Check that CLAUDE.md contains specific text."""
    claude_file = project_path / "CLAUDE.md"
    content = claude_file.read_text(encoding="utf-8")
    assert text in content, f"Expected '{text}' not found in CLAUDE.md"


@then(parsers.parse('the CLAUDE.md file should contain "{text}"'))
def claude_md_contains(project_path, text):
    """Check that CLAUDE.md contains specific text."""
    claude_file = project_path / "CLAUDE.md"
    content = claude_file.read_text(encoding="utf-8")
    assert text in content, f"Expected '{text}' not found in CLAUDE.md"


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(command_result, text):
    """Check that command output contains specific text."""
    output = command_result["stdout"] + command_result["stderr"]
    assert text in output, f"Expected '{text}' not found in output"
