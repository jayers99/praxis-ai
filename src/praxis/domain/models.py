"""Pydantic models for Praxis configuration and validation."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from praxis.domain.domains import Domain
from praxis.domain.privacy import PrivacyLevel
from praxis.domain.stages import Stage


class PraxisConfig(BaseModel):
    """Configuration from praxis.yaml."""

    domain: Domain
    stage: Stage
    privacy_level: PrivacyLevel
    environment: str = Field(default="Home", pattern=r"^(Home|Work)$")


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
