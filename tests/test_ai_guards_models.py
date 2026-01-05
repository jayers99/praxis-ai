"""Unit tests for AI Guards domain models."""

from pathlib import Path

import pytest

from praxis.domain.ai_guards import (
    AIVendor,
    EnvironmentConfig,
    GuardComposition,
    GuardFile,
    GuardLevel,
    GuardValidationIssue,
    GuardValidationResult,
    RenderedGuard,
)


def test_guard_file_creation():
    """Test creating a GuardFile."""
    guard = GuardFile(
        path=Path("/home/user/.ai-guards/core.md"),
        level=GuardLevel.USER_CORE,
        exists=True,
        content="# Core Guards\nUse TypeScript",
    )
    assert guard.path == Path("/home/user/.ai-guards/core.md")
    assert guard.level == GuardLevel.USER_CORE
    assert guard.exists is True
    assert guard.content is not None


def test_guard_file_nonexistent():
    """Test GuardFile for nonexistent file."""
    guard = GuardFile(
        path=Path("/nonexistent/file.md"),
        level=GuardLevel.USER_CORE,
        exists=False,
    )
    assert guard.exists is False
    assert guard.content is None


def test_environment_config_defaults():
    """Test EnvironmentConfig defaults to home."""
    config = EnvironmentConfig()
    assert config.active_environment == "home"
    assert config.env_file_path is None


def test_environment_config_work():
    """Test EnvironmentConfig with work environment."""
    config = EnvironmentConfig(
        active_environment="work",
        env_file_path=Path("/home/user/.ai-guards/env.md"),
    )
    assert config.active_environment == "work"
    assert config.env_file_path == Path("/home/user/.ai-guards/env.md")


def test_guard_composition_empty():
    """Test empty GuardComposition."""
    composition = GuardComposition(environment="home")
    assert composition.all_guards == []
    assert composition.environment == "home"
    assert composition.composition_order == []


def test_guard_composition_with_guards():
    """Test GuardComposition with multiple guards."""
    core_guard = GuardFile(
        path=Path("/home/user/.ai-guards/core.md"),
        level=GuardLevel.USER_CORE,
        exists=True,
        content="Core content",
    )
    project_guard = GuardFile(
        path=Path("/project/praxis/ai-guards/code.md"),
        level=GuardLevel.PROJECT_DOMAIN,
        exists=True,
        content="Project content",
        domain="code",
    )

    composition = GuardComposition(
        user_core=core_guard,
        project_guards=[project_guard],
        environment="home",
        composition_order=["user_core", "project (code)"],
    )

    assert len(composition.all_guards) == 2
    assert composition.all_guards[0] == core_guard
    assert composition.all_guards[1] == project_guard


def test_rendered_guard_creation():
    """Test RenderedGuard creation."""
    composition = GuardComposition(environment="home")
    rendered = RenderedGuard(
        vendor=AIVendor.CLAUDE,
        filename="CLAUDE.md",
        content="# AI Instructions for Claude\n",
        composition=composition,
    )

    assert rendered.vendor == AIVendor.CLAUDE
    assert rendered.filename == "CLAUDE.md"
    assert "Claude" in rendered.content
    assert rendered.warnings == []


def test_rendered_guard_with_warnings():
    """Test RenderedGuard with warnings."""
    composition = GuardComposition(environment="home")
    rendered = RenderedGuard(
        vendor=AIVendor.COPILOT,
        filename=".github/copilot-instructions.md",
        content="Content",
        composition=composition,
        warnings=["No user core guards found"],
    )

    assert len(rendered.warnings) == 1
    assert "No user core guards found" in rendered.warnings


def test_validation_result_valid():
    """Test valid GuardValidationResult."""
    composition = GuardComposition(environment="home")
    result = GuardValidationResult(
        valid=True,
        issues=[],
        composition=composition,
    )

    assert result.valid is True
    assert result.errors == []
    assert result.warnings == []


def test_validation_result_with_errors():
    """Test GuardValidationResult with errors."""
    composition = GuardComposition(environment="home")
    error_issue = GuardValidationIssue(
        severity="error",
        message="Critical error",
    )
    warning_issue = GuardValidationIssue(
        severity="warning",
        message="Warning message",
    )

    result = GuardValidationResult(
        valid=False,
        issues=[error_issue, warning_issue],
        composition=composition,
    )

    assert result.valid is False
    assert len(result.errors) == 1
    assert len(result.warnings) == 1
    assert result.errors[0].message == "Critical error"
    assert result.warnings[0].message == "Warning message"


def test_ai_vendor_enum():
    """Test AIVendor enum values."""
    assert AIVendor.CLAUDE.value == "claude"
    assert AIVendor.COPILOT.value == "copilot"
    assert AIVendor.GEMINI.value == "gemini"


def test_guard_level_enum():
    """Test GuardLevel enum values."""
    assert GuardLevel.USER_CORE.value == "user_core"
    assert GuardLevel.USER_ENV.value == "user_env"
    assert GuardLevel.USER_TOOLS.value == "user_tools"
    assert GuardLevel.PROJECT_DOMAIN.value == "project_domain"
