"""Domain models for research library cataloging.

This module defines the core domain entities for cataloging research artifacts
into the research library. It supports the Cataloger role defined in
core/roles/definitions/cataloger.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CatalogEntry:
    """A research artifact entry for the catalog.

    Represents a validated research artifact with all required metadata
    for inclusion in the research library catalog.

    Attributes:
        id: Unique identifier, format: {topic}-{slug}-{YYYY-MM-DD}
        title: Human-readable title of the artifact
        date: ISO date format (YYYY-MM-DD)
        status: Approval status (must be "approved" or "validated")
        topic: Topic folder name within research-library
        keywords: 3-7 searchable terms
        consensus: Level of consensus (high, medium, low, etc.)
        sources_count: Number of sources cited (must be >= 0)
        path: Relative path within research-library
        also_relevant: Optional list of secondary topics for cross-listing
        supersedes: Optional ID of artifact being replaced
        related: Optional list of related artifact IDs
    """

    id: str
    title: str
    date: str
    status: str
    topic: str
    keywords: list[str]
    consensus: str
    sources_count: int
    path: Path
    also_relevant: list[str] | None = None
    supersedes: str | None = None
    related: list[str] | None = None


@dataclass
class ValidationError:
    """A validation error for artifact metadata.

    Attributes:
        field: Name of the field that failed validation
        message: Human-readable error message
    """

    field: str
    message: str


@dataclass
class CatalogResult:
    """Result of a cataloging operation.

    Attributes:
        success: Whether the operation succeeded
        entry: The catalog entry if successful
        errors: List of validation errors if unsuccessful
    """

    success: bool
    entry: CatalogEntry | None = None
    errors: list[ValidationError] = field(default_factory=list)
