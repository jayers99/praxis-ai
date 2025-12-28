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
