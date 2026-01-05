"""Unit tests for AI Guards service."""

import tempfile
from pathlib import Path

import pytest

from praxis.application.ai_guards_service import (
    compose_guards,
    list_active_guards,
    render_guard_for_vendor,
    validate_guard_composition,
)
from praxis.domain.ai_guards import (
    AIVendor,
    GuardComposition,
    GuardFile,
    GuardLevel,
)


def test_compose_guards_no_guards(tmp_path):
    """Test composing guards when no guards exist."""
    # Create a project directory without any guard files
    composition = compose_guards("code", tmp_path)

    assert composition.user_core is None
    assert composition.user_tools is None
    assert composition.user_env is None
    assert composition.project_guards == []
    assert composition.environment == "home"  # default


def test_compose_guards_with_project_guards(tmp_path):
    """Test composing guards with project-level guards."""
    # Create project guards directory
    guards_dir = tmp_path / "praxis" / "ai-guards"
    guards_dir.mkdir(parents=True)

    # Create a code.md guard file
    code_guard_path = guards_dir / "code.md"
    code_guard_path.write_text("# Code Guards\nUse TypeScript", encoding="utf-8")

    # Compose guards
    composition = compose_guards("code", tmp_path)

    assert len(composition.project_guards) == 1
    assert composition.project_guards[0].domain == "code"
    assert composition.project_guards[0].exists is True
    assert "TypeScript" in composition.project_guards[0].content or ""


def test_render_guard_for_claude():
    """Test rendering guards for Claude."""
    # Create a simple composition
    composition = GuardComposition(
        user_core=GuardFile(
            path=Path("/fake/core.md"),
            level=GuardLevel.USER_CORE,
            exists=True,
            content="Use clear variable names",
        ),
        environment="home",
    )

    # Render for Claude
    rendered = render_guard_for_vendor(composition, AIVendor.CLAUDE)

    assert rendered.vendor == AIVendor.CLAUDE
    assert rendered.filename == "CLAUDE.md"
    assert "Claude" in rendered.content
    assert "User Core Guards" in rendered.content
    assert "Use clear variable names" in rendered.content


def test_render_guard_for_copilot():
    """Test rendering guards for GitHub Copilot."""
    composition = GuardComposition(environment="home")

    rendered = render_guard_for_vendor(composition, AIVendor.COPILOT)

    assert rendered.vendor == AIVendor.COPILOT
    assert rendered.filename == ".github/copilot-instructions.md"
    assert "Copilot" in rendered.content


def test_render_guard_for_gemini():
    """Test rendering guards for Gemini."""
    composition = GuardComposition(environment="home")

    rendered = render_guard_for_vendor(composition, AIVendor.GEMINI)

    assert rendered.vendor == AIVendor.GEMINI
    assert rendered.filename == "GEMINI.md"
    assert "Gemini" in rendered.content


def test_render_guard_with_all_guard_types():
    """Test rendering with all guard types present."""
    composition = GuardComposition(
        user_core=GuardFile(
            path=Path("/fake/core.md"),
            level=GuardLevel.USER_CORE,
            exists=True,
            content="Core content",
        ),
        user_tools=GuardFile(
            path=Path("/fake/tools.md"),
            level=GuardLevel.USER_TOOLS,
            exists=True,
            content="Tool mappings",
        ),
        user_env=GuardFile(
            path=Path("/fake/env/home.md"),
            level=GuardLevel.USER_ENV,
            exists=True,
            content="Home environment",
        ),
        project_guards=[
            GuardFile(
                path=Path("/fake/praxis/ai-guards/code.md"),
                level=GuardLevel.PROJECT_DOMAIN,
                exists=True,
                content="Code domain guards",
                domain="code",
            )
        ],
        environment="home",
    )

    rendered = render_guard_for_vendor(composition, AIVendor.CLAUDE)

    assert "Core content" in rendered.content
    assert "Tool mappings" in rendered.content
    assert "Home environment" in rendered.content
    assert "Code domain guards" in rendered.content
    assert "User Core Guards" in rendered.content
    assert "Environment Overlay" in rendered.content
    assert "Tool Mappings" in rendered.content
    assert "Project Guards: code" in rendered.content


def test_render_guard_no_guards_has_warning():
    """Test rendering with no guards produces warning."""
    composition = GuardComposition(environment="home")

    rendered = render_guard_for_vendor(composition, AIVendor.CLAUDE)

    assert len(rendered.warnings) > 0
    assert any("No user core guards found" in w for w in rendered.warnings)


def test_validate_empty_composition():
    """Test validating empty composition."""
    composition = GuardComposition(environment="home")

    result = validate_guard_composition(composition)

    # Should be valid (warnings are okay)
    assert result.valid is True
    assert len(result.warnings) > 0  # Should have warnings about missing guards


def test_validate_composition_with_guards():
    """Test validating composition with guards."""
    composition = GuardComposition(
        user_core=GuardFile(
            path=Path("/fake/core.md"),
            level=GuardLevel.USER_CORE,
            exists=True,
            content="Core content",
        ),
        environment="home",
    )

    result = validate_guard_composition(composition)

    assert result.valid is True


def test_validate_detects_environment_leakage():
    """Test validation detects potential environment leakage."""
    # Create a work environment composition with home paths
    composition = GuardComposition(
        user_core=GuardFile(
            path=Path("/fake/core.md"),
            level=GuardLevel.USER_CORE,
            exists=True,
            content="Use ~/personal/scripts for automation",
        ),
        environment="work",  # Work environment but references ~/personal
    )

    result = validate_guard_composition(composition)

    # Should be valid but have warnings
    assert result.valid is True
    assert len(result.warnings) > 0
    assert any("environment leakage" in w.message.lower() for w in result.warnings)


def test_list_active_guards_no_guards(tmp_path):
    """Test listing guards when none exist."""
    descriptions = list_active_guards("code", tmp_path)

    assert len(descriptions) > 0
    assert "Active environment:" in descriptions[0]


def test_list_active_guards_with_guards(tmp_path):
    """Test listing guards with some present."""
    # Create project guards directory
    guards_dir = tmp_path / "praxis" / "ai-guards"
    guards_dir.mkdir(parents=True)

    # Create a code.md guard file
    code_guard_path = guards_dir / "code.md"
    code_guard_path.write_text("# Code Guards", encoding="utf-8")

    descriptions = list_active_guards("code", tmp_path)

    assert any("project_domain" in desc for desc in descriptions)
    assert any("✓" in desc for desc in descriptions)  # At least one exists
