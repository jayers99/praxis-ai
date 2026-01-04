"""CLI contract tests - verify JSON schemas and exit codes remain stable."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from praxis.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def valid_project(tmp_path: Path) -> Path:
    """Create a valid praxis project."""
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )
    return tmp_path


@pytest.fixture
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a valid workspace."""
    workspace_path = tmp_path / "workspace"
    workspace_path.mkdir()
    
    # Create workspace structure
    (workspace_path / "extensions").mkdir()
    (workspace_path / "examples").mkdir()
    (workspace_path / "projects").mkdir()
    
    # Create workspace config
    config_path = workspace_path / "workspace-config.yaml"
    config_path.write_text(
        """installed_extensions: []
installed_examples: []
defaults:
  privacy: personal
  environment: Home
"""
    )
    
    monkeypatch.setenv("PRAXIS_HOME", str(workspace_path))
    return workspace_path


class TestStatusContract:
    """Test praxis status JSON schema and exit codes."""

    def test_json_schema_structure(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Status JSON output has required top-level fields."""
        result = cli_runner.invoke(app, ["status", str(valid_project), "--json"])
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        
        # Required top-level fields
        assert "project_name" in data
        assert "config" in data
        assert "stage_index" in data
        assert "stage_count" in data
        assert "next_stage" in data
        assert "next_stage_requirements" in data
        assert "artifact_path" in data
        assert "artifact_exists" in data
        assert "validation" in data
        assert "next_steps" in data
        
        # Config structure
        config = data["config"]
        assert "domain" in config
        assert "stage" in config
        assert "privacy_level" in config
        assert "environment" in config
        
        # Validation structure
        validation = data["validation"]
        assert "valid" in validation
        assert "issues" in validation
        
    def test_quiet_suppresses_output(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Status --quiet produces no output on success."""
        result = cli_runner.invoke(app, ["status", str(valid_project), "--quiet"])
        assert result.exit_code == 0
        assert result.output.strip() == ""


class TestValidateContract:
    """Test praxis validate JSON schema and exit codes."""

    def test_json_schema_structure(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Validate JSON output has required fields."""
        result = cli_runner.invoke(app, ["validate", str(valid_project), "--json"])
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        
        # Required fields
        assert "valid" in data
        assert "config" in data
        assert "issues" in data
        assert "version" in data
        assert "tool_checks" in data
        
        # Version field
        assert data["version"] == "1.0"
        
        # Config structure
        config = data["config"]
        assert "domain" in config
        assert "stage" in config
        assert "privacy_level" in config
        
    def test_exit_code_on_valid_config(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Validate exits 0 for valid config."""
        result = cli_runner.invoke(app, ["validate", str(valid_project)])
        assert result.exit_code == 0
        
    def test_exit_code_on_invalid_config(
        self, cli_runner: CliRunner, tmp_path: Path
    ) -> None:
        """Validate exits 1 for invalid config."""
        # Create invalid config (missing required field)
        praxis_yaml = tmp_path / "praxis.yaml"
        praxis_yaml.write_text(
            """domain: invalid_domain
stage: capture
"""
        )
        
        result = cli_runner.invoke(app, ["validate", str(tmp_path)])
        assert result.exit_code == 1
        
    def test_quiet_suppresses_output_on_success(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Validate --quiet produces no output on success."""
        result = cli_runner.invoke(app, ["validate", str(valid_project), "--quiet"])
        assert result.exit_code == 0
        assert result.output.strip() == ""
        
    def test_quiet_suppresses_output_on_failure(
        self, cli_runner: CliRunner, tmp_path: Path
    ) -> None:
        """Validate --quiet produces no output on failure."""
        # Create invalid config
        praxis_yaml = tmp_path / "praxis.yaml"
        praxis_yaml.write_text("invalid: yaml")
        
        result = cli_runner.invoke(app, ["validate", str(tmp_path), "--quiet"])
        assert result.exit_code == 1
        assert result.output.strip() == ""


class TestAuditContract:
    """Test praxis audit JSON schema and exit codes."""

    def test_json_schema_structure(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Audit JSON output has required fields."""
        result = cli_runner.invoke(app, ["audit", str(valid_project), "--json"])
        
        data = json.loads(result.output)
        
        # Required fields
        assert "project_name" in data
        assert "domain" in data
        assert "checks" in data
        
        # Check structure (if any checks exist)
        if data["checks"]:
            check = data["checks"][0]
            assert "name" in check
            assert "category" in check
            assert "status" in check
            assert "message" in check
            assert check["status"] in ["passed", "warning", "failed"]
            
    def test_exit_code_no_failures(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Audit exits 0 when no failures (warnings OK)."""
        result = cli_runner.invoke(app, ["audit", str(valid_project)])
        # May have warnings but should not fail
        assert result.exit_code == 0
        
    def test_strict_mode_fails_on_warnings(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Audit --strict exits 1 on warnings."""
        result = cli_runner.invoke(app, ["audit", str(valid_project), "--strict"])
        # Will have warnings for missing tooling, should fail in strict mode
        assert result.exit_code == 1
        
    def test_quiet_suppresses_output(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Audit --quiet produces no output on success."""
        result = cli_runner.invoke(app, ["audit", str(valid_project), "--quiet"])
        assert result.output.strip() == ""


class TestContextContract:
    """Test praxis context JSON schema and exit codes."""

    def test_json_schema_structure(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Context JSON output has required fields."""
        result = cli_runner.invoke(app, ["context", str(valid_project), "--json"])
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        
        # Required fields
        assert "schema_version" in data
        assert "project_name" in data
        assert "domain" in data
        assert "stage" in data
        assert "privacy_level" in data
        assert "environment" in data
        assert "opinions" in data
        assert "formalize_artifact" in data
        assert "errors" in data
        
        # Schema version
        assert data["schema_version"] == "1.0"
        
    def test_quiet_suppresses_output(
        self, cli_runner: CliRunner, valid_project: Path
    ) -> None:
        """Context --quiet produces no output on success."""
        result = cli_runner.invoke(app, ["context", str(valid_project), "--quiet"])
        assert result.exit_code == 0
        assert result.output.strip() == ""


class TestOpinionsContract:
    """Test praxis opinions JSON schema and exit codes."""

    def test_json_schema_structure(self, cli_runner: CliRunner) -> None:
        """Opinions JSON output has required fields."""
        result = cli_runner.invoke(
            app, ["opinions", "--domain", "code", "--stage", "capture", "--json"]
        )
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        
        # Required fields
        assert "domain" in data
        assert "stage" in data
        assert "subtype" in data
        assert "files" in data
        
        # File structure (if any files exist)
        if data["files"]:
            file = data["files"][0]
            assert "path" in file
            assert "exists" in file
            assert "status" in file
            assert "version" in file


class TestWorkspaceInfoContract:
    """Test praxis workspace info JSON schema and exit codes."""

    def test_json_schema_structure(
        self, cli_runner: CliRunner, workspace: Path
    ) -> None:
        """Workspace info JSON output has required fields."""
        result = cli_runner.invoke(app, ["workspace", "info", "--json"])
        assert result.exit_code == 0
        
        data = json.loads(result.output)
        
        # Required fields
        assert "path" in data
        assert "extensions_path" in data
        assert "examples_path" in data
        assert "projects_path" in data
        assert "installed_extensions" in data
        assert "installed_examples" in data
        assert "defaults" in data
        
        # Defaults structure
        defaults = data["defaults"]
        assert "privacy" in defaults
        assert "environment" in defaults
        
    def test_quiet_suppresses_output(
        self, cli_runner: CliRunner, workspace: Path
    ) -> None:
        """Workspace info --quiet produces no output on success."""
        result = cli_runner.invoke(app, ["workspace", "info", "--quiet"])
        assert result.exit_code == 0
        assert result.output.strip() == ""
        
    def test_exit_code_no_workspace(self, cli_runner: CliRunner) -> None:
        """Workspace info exits 3 when PRAXIS_HOME not set."""
        result = cli_runner.invoke(app, ["workspace", "info"])
        assert result.exit_code == 3


class TestExitCodeConsistency:
    """Test exit code semantics across commands."""

    def test_init_requires_args_with_json(
        self, cli_runner: CliRunner, tmp_path: Path
    ) -> None:
        """Init --json without required args exits 1."""
        result = cli_runner.invoke(app, ["init", str(tmp_path), "--json"])
        assert result.exit_code == 1
        
        # Should have error in JSON
        data = json.loads(result.output)
        assert "errors" in data
        
    def test_init_requires_args_with_quiet(
        self, cli_runner: CliRunner, tmp_path: Path
    ) -> None:
        """Init --quiet without required args exits 1."""
        result = cli_runner.invoke(app, ["init", str(tmp_path), "--quiet"])
        assert result.exit_code == 1
        
    def test_new_requires_args_with_json(self, cli_runner: CliRunner) -> None:
        """New --json without required args exits 1."""
        result = cli_runner.invoke(app, ["new", "test-proj", "--json"])
        assert result.exit_code == 1
        
        # Should have error in JSON
        data = json.loads(result.output)
        assert not data["success"]
        assert len(data["errors"]) > 0
