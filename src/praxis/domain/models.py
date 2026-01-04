"""Pydantic models for Praxis configuration and validation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from praxis.domain.domains import Domain
from praxis.domain.privacy import PrivacyLevel
from praxis.domain.stages import Stage


class StageHistoryEntry(BaseModel):
    """A single stage transition in project history."""

    timestamp: str = Field(description="ISO8601 timestamp of transition")
    from_stage: str = Field(description="Stage before transition")
    to_stage: str = Field(description="Stage after transition")
    contract_id: str | None = Field(
        default=None,
        description="Contract ID for Formalize transitions",
    )
    reason: str | None = Field(
        default=None,
        description="Rationale for non-standard regressions",
    )


class PraxisConfig(BaseModel):
    """Configuration from praxis.yaml."""

    domain: Domain
    subtype: str | None = Field(
        default=None,
        description="Optional subtype (domain-specific).",
    )
    stage: Stage
    privacy_level: PrivacyLevel
    environment: str = Field(default="Home", pattern=r"^(Home|Work)$")
    coverage_threshold: int | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Minimum test coverage percentage (0-100). Optional.",
    )
    history: list[StageHistoryEntry] = Field(
        default_factory=list,
        description="Stage transition history (most recent last).",
    )


class ValidationIssue(BaseModel):
    """A single validation issue (error or warning)."""

    rule: str
    severity: Literal["error", "warning"]
    message: str


class ValidationResult(BaseModel):
    """Result of validating a praxis.yaml configuration."""

    valid: bool
    config: PraxisConfig | None = None
    issues: list[ValidationIssue] = Field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        """Return only error-severity issues."""
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Return only warning-severity issues."""
        return [i for i in self.issues if i.severity == "warning"]


class InitResult(BaseModel):
    """Result of initializing a Praxis project."""

    success: bool
    files_created: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class StageResult(BaseModel):
    """Result of a stage transition."""

    success: bool
    issues: list[ValidationIssue] = Field(default_factory=list)
    needs_confirmation: bool = False
    warning_message: str | None = None


class ToolCheckResult(BaseModel):
    """Result of running an external validation tool."""

    tool: str
    success: bool
    output: str = ""
    error: str = ""


class CoverageCheckResult(BaseModel):
    """Result of running coverage check."""

    tool: str = "coverage"
    success: bool
    coverage_percent: float | None = None
    threshold: int
    error: str = ""


class AuditCheck(BaseModel):
    """Single audit check result."""

    name: str
    category: str  # tooling, structure, testing
    status: Literal["passed", "warning", "failed"]
    message: str


class AuditResult(BaseModel):
    """Complete audit result."""

    project_name: str
    domain: str
    checks: list[AuditCheck] = Field(default_factory=list)

    @property
    def passed(self) -> list[AuditCheck]:
        """Return only passed checks."""
        return [c for c in self.checks if c.status == "passed"]

    @property
    def warnings(self) -> list[AuditCheck]:
        """Return only warning checks."""
        return [c for c in self.checks if c.status == "warning"]

    @property
    def failed(self) -> list[AuditCheck]:
        """Return only failed checks."""
        return [c for c in self.checks if c.status == "failed"]


class ContextBundle(BaseModel):
    """Deterministic AI context bundle for a Praxis project."""

    schema_version: str = Field(
        default="1.0",
        description="Schema version for backwards compatibility tracking",
    )
    project_name: str = Field(description="Project name from directory")
    domain: str = Field(description="Project domain (code, create, write, etc.)")
    stage: str = Field(description="Current lifecycle stage")
    privacy_level: str = Field(description="Privacy level of the project")
    environment: str = Field(description="Environment (Home, Work)")
    subtype: str | None = Field(
        default=None,
        description="Optional subtype (e.g., cli, library, api)",
    )
    opinions: list[str] = Field(
        default_factory=list,
        description="Resolved opinion file paths in resolution order",
    )
    formalize_artifact: dict[str, str | None] = Field(
        default_factory=dict,
        description="Formalize artifact info (path and excerpt)",
    )
    errors: list[str] = Field(
        default_factory=list,
        description="Any errors encountered during context generation",
    )
