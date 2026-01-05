"""Domain specification models for custom domain definitions."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class AIConstraint(BaseModel):
    """AI behavior constraint for a domain."""

    name: str = Field(description="Constraint name (e.g., 'citation_required')")
    value: bool | str = Field(description="Constraint value")
    description: str | None = Field(
        default=None,
        description="Human-readable explanation of the constraint",
    )


class DomainSpecification(BaseModel):
    """Specification for a custom domain.

    This defines all characteristics of a domain that can be used
    to extend Praxis without modifying core code.
    """

    # Core identity
    name: str = Field(
        pattern=r"^[a-z][a-z0-9-]*$",
        description="Domain identifier (lowercase, alphanumeric, dashes)",
    )
    display_name: str = Field(description="Human-readable domain name")
    description: str = Field(description="What kind of work this domain covers")

    # Lifecycle configuration
    formalize_artifact_name: str | None = Field(
        default=None,
        description="Name of the formalize artifact (e.g., 'Solution Overview Document')",
    )
    formalize_artifact_path: str | None = Field(
        default=None,
        pattern=r"^docs/.*\.md$",
        description="Path to formalize artifact (e.g., 'docs/sod.md')",
    )
    allowed_stages: list[str] = Field(
        default_factory=lambda: [
            "capture",
            "sense",
            "explore",
            "shape",
            "formalize",
            "commit",
            "execute",
            "sustain",
            "close",
        ],
        description="Lifecycle stages allowed for this domain",
    )

    # Privacy and security
    default_privacy: str = Field(
        default="personal",
        description="Default privacy level for new projects",
    )

    # AI permissions
    ai_permissions: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "AI operation permissions: suggest, complete, generate, transform, execute"
        ),
    )
    ai_constraints: list[AIConstraint] = Field(
        default_factory=list,
        description="Additional AI behavior constraints",
    )

    # Subtypes
    subtypes: list[str] = Field(
        default_factory=list,
        description="Valid subtypes for this domain",
    )

    # Metadata
    author: str | None = Field(default=None, description="Domain specification author")
    version: str = Field(default="1.0", description="Domain specification version")
    created_at: str | None = Field(
        default=None,
        description="ISO8601 timestamp of creation",
    )


class DomainCreationResult(BaseModel):
    """Result of domain creation process."""

    success: bool
    domain_name: str | None = None
    spec_path: str | None = Field(
        default=None,
        description="Path to generated domain specification file",
    )
    files_created: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class DomainMenuOption(BaseModel):
    """Predefined domain template option for menu selection."""

    key: str = Field(description="Option key for menu selection")
    name: str = Field(description="Domain name")
    display_name: str = Field(description="Human-readable display name")
    description: str = Field(description="What this domain is for")
    formalize_artifact_name: str | None = None
    formalize_artifact_path: str | None = None
    default_privacy: str = "personal"
    ai_permissions: dict[str, str] = Field(default_factory=dict)
    subtypes: list[str] = Field(default_factory=list)
