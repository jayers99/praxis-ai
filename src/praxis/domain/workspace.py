"""Workspace domain models for Praxis workspace management."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from praxis.domain.domains import Domain
from praxis.domain.privacy import PrivacyLevel


class ExtensionInfo(BaseModel):
    """Information about an available or installed extension."""

    name: str
    repo: str
    domain: Domain
    description: str
    installed: bool = False


class ExampleInfo(BaseModel):
    """Information about an available or installed example."""

    name: str
    repo: str
    domain: Domain
    description: str
    installed: bool = False


class WorkspaceDefaults(BaseModel):
    """Default settings for new projects in the workspace."""

    privacy: PrivacyLevel = PrivacyLevel.PERSONAL
    environment: str = "Home"


class WorkspaceConfig(BaseModel):
    """Configuration for a Praxis workspace (workspace-config.yaml)."""

    projects_path: str = "./projects"
    installed_extensions: list[str] = Field(default_factory=list)
    installed_examples: list[str] = Field(default_factory=list)
    defaults: WorkspaceDefaults = Field(default_factory=WorkspaceDefaults)


class WorkspaceInfo(BaseModel):
    """Information about a Praxis workspace."""

    path: Path
    config: WorkspaceConfig
    extensions_path: Path
    examples_path: Path
    projects_path: Path
    praxis_ai_path: Path | None = None


class WorkspaceInitResult(BaseModel):
    """Result of workspace initialization."""

    success: bool
    workspace_path: Path
    files_created: list[str] = Field(default_factory=list)
    dirs_created: list[str] = Field(default_factory=list)
    extensions_installed: list[str] = Field(default_factory=list)
    examples_installed: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ExtensionAddResult(BaseModel):
    """Result of adding an extension."""

    success: bool
    name: str
    path: Path | None = None
    error: str | None = None


class ExtensionRemoveResult(BaseModel):
    """Result of removing an extension."""

    success: bool
    name: str
    error: str | None = None


class ExtensionListResult(BaseModel):
    """Result of listing extensions."""

    available: list[ExtensionInfo]
    installed: list[str]


class ExampleAddResult(BaseModel):
    """Result of adding an example."""

    success: bool
    name: str
    path: Path | None = None
    error: str | None = None


class ExampleListResult(BaseModel):
    """Result of listing examples."""

    available: list[ExampleInfo]
    installed: list[str]
