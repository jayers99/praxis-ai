"""Domain models for AI Guards composition and rendering."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class AIVendor(str, Enum):
    """Supported AI assistant vendors."""

    CLAUDE = "claude"
    COPILOT = "copilot"
    GEMINI = "gemini"


class GuardLevel(str, Enum):
    """Level at which a guard is defined."""

    USER_CORE = "user_core"  # ~/.ai-guards/core.md
    USER_ENV = "user_env"  # ~/.ai-guards/env/{home|work}.md
    USER_TOOLS = "user_tools"  # ~/.ai-guards/tools.md
    PROJECT_DOMAIN = "project_domain"  # praxis/ai-guards/{domain}.md


class GuardFile(BaseModel):
    """A single guard file with metadata."""

    path: Path = Field(description="Absolute path to the guard file")
    level: GuardLevel = Field(description="Level at which this guard is defined")
    exists: bool = Field(description="Whether the file exists on disk")
    content: str | None = Field(
        default=None,
        description="File content if exists",
    )
    domain: str | None = Field(
        default=None,
        description="Domain name for project-level guards",
    )


class EnvironmentConfig(BaseModel):
    """User-level environment configuration."""

    active_environment: Literal["home", "work"] = Field(
        default="home",
        description="Currently active environment",
    )
    env_file_path: Path | None = Field(
        default=None,
        description="Path to env.md selector file",
    )


class GuardComposition(BaseModel):
    """Composed AI guards from multiple sources."""

    user_core: GuardFile | None = Field(
        default=None,
        description="User core guards",
    )
    user_tools: GuardFile | None = Field(
        default=None,
        description="User tool mappings",
    )
    user_env: GuardFile | None = Field(
        default=None,
        description="Environment overlay (home or work)",
    )
    project_guards: list[GuardFile] = Field(
        default_factory=list,
        description="Project-level domain guards",
    )
    environment: Literal["home", "work"] = Field(
        default="home",
        description="Active environment",
    )
    composition_order: list[str] = Field(
        default_factory=list,
        description="Order in which guards were composed (for debugging)",
    )

    @property
    def all_guards(self) -> list[GuardFile]:
        """Return all guard files in composition order."""
        guards = []
        if self.user_core:
            guards.append(self.user_core)
        if self.user_env:
            guards.append(self.user_env)
        if self.user_tools:
            guards.append(self.user_tools)
        guards.extend(self.project_guards)
        return guards


class RenderedGuard(BaseModel):
    """Final rendered guard file for a specific AI vendor."""

    vendor: AIVendor = Field(description="Target AI vendor")
    filename: str = Field(description="Target filename (e.g., CLAUDE.md)")
    content: str = Field(description="Rendered content")
    composition: GuardComposition = Field(
        description="Source composition used to generate this render",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Warnings during rendering (e.g., missing guards)",
    )


class GuardValidationIssue(BaseModel):
    """A single validation issue for guard composition."""

    severity: Literal["error", "warning", "info"] = Field(
        description="Issue severity",
    )
    message: str = Field(description="Human-readable issue description")
    guard_file: str | None = Field(
        default=None,
        description="Guard file path related to this issue",
    )


class GuardValidationResult(BaseModel):
    """Result of validating a guard composition."""

    valid: bool = Field(description="Whether composition is valid")
    issues: list[GuardValidationIssue] = Field(
        default_factory=list,
        description="Validation issues found",
    )
    composition: GuardComposition | None = Field(
        default=None,
        description="The composition that was validated",
    )

    @property
    def errors(self) -> list[GuardValidationIssue]:
        """Return only error-severity issues."""
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[GuardValidationIssue]:
        """Return only warning-severity issues."""
        return [i for i in self.issues if i.severity == "warning"]
