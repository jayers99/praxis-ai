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


class OpinionContribution(BaseModel):
    """A single opinion file contribution from an extension."""

    source: str = Field(
        description="Relative path in extension (e.g., 'opinions/code/principles.md')"
    )
    target: str = Field(
        description="Target path in opinions tree (e.g., 'code/principles.md')"
    )


class TemplateContribution(BaseModel):
    """A single template file contribution from an extension."""

    source: str = Field(
        description=(
            "Relative path in extension "
            "(e.g., 'templates/formalize/mobile-sod.md')"
        )
    )
    target: str = Field(
        description=(
            "Target path in template tree "
            "(e.g., 'code/formalize/mobile-sod.md')"
        )
    )
    subtypes: list[str] = Field(
        default_factory=list,
        description="Subtypes this template applies to (empty = all subtypes)",
    )


class ExtensionManifest(BaseModel):
    """Manifest for extension contributions (praxis-extension.yaml).

    Schema version 0.1 - experimental, subject to breaking changes before v1.0.
    """

    manifest_version: str = Field(
        description="Manifest schema version (e.g., '0.1', '1.0')"
    )
    name: str = Field(description="Extension name (must match directory name)")
    description: str | None = Field(
        default=None, description="Human-readable description"
    )
    contributions: ExtensionContributions = Field(
        default_factory=lambda: ExtensionContributions()
    )


class AuditCheckContribution(BaseModel):
    """A single audit check contribution from an extension."""

    name: str = Field(description="Check name (unique within extension)")
    category: str = Field(description="Check category (e.g., 'structure', 'tooling')")
    check_type: str = Field(
        description="Type of check (file_exists, dir_exists, file_contains)"
    )
    path: str = Field(
        description="File or directory path to check (relative to project root)"
    )
    pattern: str | None = Field(
        default=None,
        description="Regex pattern for file_contains check type",
    )
    pass_message: str = Field(description="Message to display when check passes")
    fail_message: str = Field(description="Message to display when check fails")
    severity: str = Field(
        default="warning",
        description="Severity level (warning or failed)",
    )
    min_stage: str | None = Field(
        default=None,
        description="Minimum stage for check to apply (optional)",
    )


class AuditContribution(BaseModel):
    """Audit checks contribution for a specific domain."""

    domain: str = Field(description="Domain these checks apply to (code, create, etc.)")
    subtypes: list[str] = Field(
        default_factory=list,
        description="Subtypes these checks apply to (empty = all subtypes)",
    )
    checks: list[AuditCheckContribution] = Field(
        default_factory=list,
        description="List of audit check definitions",
    )


class ExtensionContributions(BaseModel):
    """Contributions that an extension provides."""

    opinions: list[OpinionContribution] = Field(default_factory=list)
    templates: list[TemplateContribution] = Field(default_factory=list)
    audits: list[AuditContribution] = Field(default_factory=list)


class ManifestLoadResult(BaseModel):
    """Result of loading an extension manifest."""

    success: bool
    extension_name: str
    manifest: ExtensionManifest | None = None
    error: str | None = None
    warning: str | None = None
