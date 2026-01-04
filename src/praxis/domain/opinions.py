"""Domain models for opinions resolution."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class OpinionStatus(str, Enum):
    """Status of an opinion file."""

    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"


class OpinionFrontmatter(BaseModel):
    """YAML frontmatter from an opinion file."""

    domain: str | None = None  # Optional for _shared files
    version: str
    status: OpinionStatus
    stage: str | None = None
    subtype: str | None = None
    inherits: list[str] | None = None
    author: Literal["human", "ai", "hybrid"] | None = None
    last_reviewed: str | None = None


class OpinionFile(BaseModel):
    """A single opinion file with its metadata and content."""

    path: str = Field(description="Relative path from opinions/ directory")
    exists: bool = Field(description="Whether the file exists on disk")
    frontmatter: OpinionFrontmatter | None = Field(
        default=None,
        description="Parsed YAML frontmatter, if file exists and is valid",
    )
    content: str | None = Field(
        default=None,
        description="Markdown content (excluding frontmatter)",
    )
    parse_error: str | None = Field(
        default=None,
        description="Error message if file could not be parsed",
    )
    source: str = Field(
        default="core",
        description="Provenance: 'core' or extension name that contributed this file",
    )


class ResolvedOpinions(BaseModel):
    """Result of resolving opinions for a project context."""

    domain: str
    stage: str | None = None
    subtype: str | None = None
    files: list[OpinionFile] = Field(
        default_factory=list,
        description="Opinion files in resolution order (general → specific)",
    )
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-fatal warnings during resolution",
    )

    @property
    def existing_files(self) -> list[OpinionFile]:
        """Return only files that exist on disk."""
        return [f for f in self.files if f.exists]

    @property
    def file_paths(self) -> list[str]:
        """Return paths of existing files in resolution order."""
        return [f.path for f in self.existing_files]


class OpinionsTree(BaseModel):
    """Tree structure of all available opinion files."""

    root: str = Field(description="Root opinions directory path")
    domains: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Map of domain name to list of file paths",
    )
    shared: list[str] = Field(
        default_factory=list,
        description="Files in _shared/ directory",
    )
    total_files: int = Field(default=0, description="Total number of opinion files")
    extension_contributions: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Map of extension name to list of contributed file paths",
    )
    provenance: dict[str, str] = Field(
        default_factory=dict,
        description="Map of file path to source ('core' or extension name)",
    )
