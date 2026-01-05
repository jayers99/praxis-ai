"""Library query and maintenance application service.

Wraps librarian infrastructure and cataloging_service for CLI usage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from praxis.application.cataloging_service import find_orphans, reindex_library
from praxis.infrastructure.librarian import (
    get_citations,
    query_library,
    search_library,
)


@dataclass
class LibraryQueryResult:
    """Result of a library query."""

    success: bool
    query: str = ""
    coverage_level: str = ""
    coverage_reasoning: str = ""
    match_count: int = 0
    summary: str = ""
    sources: list[dict[str, str]] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class LibrarySearchResult:
    """Result of a library search."""

    success: bool
    keyword: str = ""
    topic: str | None = None
    matches: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class LibraryCiteResult:
    """Result of getting a citation."""

    success: bool
    artifact_id: str = ""
    citation: dict[str, str] | None = None
    formatted: str = ""
    errors: list[str] = field(default_factory=list)


@dataclass
class LibraryOrphansResult:
    """Result of checking for orphaned artifacts."""

    success: bool
    orphans: list[str] = field(default_factory=list)
    count: int = 0
    errors: list[str] = field(default_factory=list)


@dataclass
class LibraryStaleResult:
    """Result of checking for stale artifacts."""

    success: bool
    stale_artifacts: list[dict[str, str]] = field(default_factory=list)
    count: int = 0
    threshold_days: int = 0
    errors: list[str] = field(default_factory=list)


@dataclass
class LibraryReindexResult:
    """Result of reindexing the library."""

    success: bool
    implemented: bool = False
    errors: list[str] = field(default_factory=list)


def _get_default_library_path() -> Path:
    """Get the default research library path.

    Looks for research-library in the current working directory first,
    then checks relative to the praxis package installation.
    """
    # Try current working directory
    cwd_library = Path.cwd() / "research-library"
    if cwd_library.exists():
        return cwd_library

    # Try relative to package (for development/testing)
    import importlib.util

    spec = importlib.util.find_spec("praxis")
    if spec and spec.origin:
        # Package is at src/praxis, library is at repo root
        package_root = Path(spec.origin).parent.parent.parent
        repo_library = package_root / "research-library"
        if repo_library.exists():
            return repo_library

    # Fallback to current directory
    return cwd_library


def query_library_service(
    question: str,
    library_path: Path | None = None,
) -> LibraryQueryResult:
    """Query the research library with a question.

    Args:
        question: Natural language question.
        library_path: Path to research library (defaults to auto-detected).

    Returns:
        LibraryQueryResult with coverage assessment and sources.
    """
    # Validate question
    if not question or not question.strip():
        return LibraryQueryResult(
            success=False,
            errors=["Query cannot be empty"],
        )

    # Resolve library path
    if library_path is None:
        library_path = _get_default_library_path()

    catalog_path = library_path / "CATALOG.md"
    if not catalog_path.exists():
        return LibraryQueryResult(
            success=False,
            errors=[f"CATALOG.md not found at {catalog_path}"],
        )

    # Query library
    response = query_library(question.strip(), library_path)

    # Convert sources to serializable format
    sources = []
    for source in response.sources:
        sources.append(
            {
                "artifact_id": source.artifact_id,
                "title": source.title,
                "path": str(source.path),
                "consensus": source.consensus,
                "date": source.date,
                "key_finding": source.key_finding,
            }
        )

    return LibraryQueryResult(
        success=True,
        query=response.query,
        coverage_level=response.coverage.level,
        coverage_reasoning=response.coverage.reasoning,
        match_count=response.coverage.match_count,
        summary=response.summary,
        sources=sources,
        gaps=response.gaps,
    )


def search_library_service(
    keyword: str,
    topic: str | None = None,
    library_path: Path | None = None,
) -> LibrarySearchResult:
    """Search the research library by keyword.

    Args:
        keyword: Keyword to search for.
        topic: Optional topic to filter by.
        library_path: Path to research library (defaults to auto-detected).

    Returns:
        LibrarySearchResult with matching artifacts.
    """
    # Validate keyword
    if not keyword or not keyword.strip():
        return LibrarySearchResult(
            success=False,
            errors=["--keyword is required"],
        )

    # Resolve library path
    if library_path is None:
        library_path = _get_default_library_path()

    catalog_path = library_path / "CATALOG.md"
    if not catalog_path.exists():
        return LibrarySearchResult(
            success=False,
            errors=[f"CATALOG.md not found at {catalog_path}"],
        )

    # Search library
    matches = search_library(
        query=keyword.strip(),
        catalog_path=catalog_path,
        topic_filter=topic.strip() if topic else None,
    )

    # Convert to serializable format
    match_list = []
    for match in matches:
        match_list.append(
            {
                "id": match.id,
                "title": match.title,
                "path": str(match.path),
                "topic": match.topic,
                "consensus": match.consensus,
                "date": match.date,
                "relevance_score": match.relevance_score,
            }
        )

    return LibrarySearchResult(
        success=True,
        keyword=keyword.strip(),
        topic=topic.strip() if topic else None,
        matches=match_list,
    )


def cite_artifact(
    artifact_id: str,
    library_path: Path | None = None,
) -> LibraryCiteResult:
    """Get a formatted citation for an artifact.

    Args:
        artifact_id: The artifact ID to cite.
        library_path: Path to research library (defaults to auto-detected).

    Returns:
        LibraryCiteResult with formatted citation.
    """
    # Validate artifact_id
    if not artifact_id or not artifact_id.strip():
        return LibraryCiteResult(
            success=False,
            errors=["Artifact ID is required"],
        )

    # Resolve library path
    if library_path is None:
        library_path = _get_default_library_path()

    catalog_path = library_path / "CATALOG.md"
    if not catalog_path.exists():
        return LibraryCiteResult(
            success=False,
            errors=[f"CATALOG.md not found at {catalog_path}"],
        )

    # Get citations
    citations = get_citations(artifact_id.strip(), library_path)

    if not citations:
        return LibraryCiteResult(
            success=False,
            artifact_id=artifact_id.strip(),
            errors=[f"Artifact not found: {artifact_id}"],
        )

    citation = citations[0]

    # Format citation
    # Format: [Title](path) - Consensus: {consensus}, Date: {date}
    formatted = (
        f"[{citation.title}]({citation.path})\n" f"  Consensus: {citation.consensus}\n" f"  Date: {citation.date}"
    )

    if citation.key_finding:
        formatted += f"\n  Key finding: {citation.key_finding[:200]}..."

    return LibraryCiteResult(
        success=True,
        artifact_id=citation.artifact_id,
        citation={
            "artifact_id": citation.artifact_id,
            "title": citation.title,
            "path": str(citation.path),
            "consensus": citation.consensus,
            "date": citation.date,
            "key_finding": citation.key_finding,
        },
        formatted=formatted,
    )


def check_orphans(
    library_path: Path | None = None,
) -> LibraryOrphansResult:
    """Check for orphaned artifacts not in CATALOG.md.

    Args:
        library_path: Path to research library (defaults to auto-detected).

    Returns:
        LibraryOrphansResult with list of orphaned artifacts.
    """
    # Resolve library path
    if library_path is None:
        library_path = _get_default_library_path()

    if not library_path.exists():
        return LibraryOrphansResult(
            success=False,
            errors=[f"Library path does not exist: {library_path}"],
        )

    # Find orphans
    orphans = find_orphans(library_path)

    return LibraryOrphansResult(
        success=True,
        orphans=[str(p) for p in orphans],
        count=len(orphans),
    )


def check_stale(
    days: int = 180,
    library_path: Path | None = None,
) -> LibraryStaleResult:
    """Check for stale artifacts older than threshold.

    Args:
        days: Number of days before an artifact is considered stale.
        library_path: Path to research library (defaults to auto-detected).

    Returns:
        LibraryStaleResult with list of stale artifacts.
    """
    # Resolve library path
    if library_path is None:
        library_path = _get_default_library_path()

    catalog_path = library_path / "CATALOG.md"
    if not catalog_path.exists():
        return LibraryStaleResult(
            success=False,
            errors=[f"CATALOG.md not found at {catalog_path}"],
        )

    # Parse catalog and check dates
    from praxis.infrastructure.librarian import parse_catalog

    artifacts = parse_catalog(catalog_path)

    # Calculate threshold date
    from datetime import timedelta

    threshold_date = datetime.now() - timedelta(days=days)
    threshold_str = threshold_date.strftime("%Y-%m-%d")

    stale_artifacts = []
    for artifact in artifacts:
        artifact_date = artifact.get("date", "")
        # Simple string comparison works for YYYY-MM-DD format
        if artifact_date and artifact_date < threshold_str:
            stale_artifacts.append(
                {
                    "id": artifact["id"],
                    "title": artifact["title"],
                    "date": artifact_date,
                    "path": artifact["path"],
                }
            )

    return LibraryStaleResult(
        success=True,
        stale_artifacts=stale_artifacts,
        count=len(stale_artifacts),
        threshold_days=days,
    )


def reindex_library_service(
    library_path: Path | None = None,
) -> LibraryReindexResult:
    """Reindex the research library.

    Note: This is currently a placeholder. Full reindexing requires
    scanning all artifacts and rebuilding CATALOG.md.

    Args:
        library_path: Path to research library (defaults to auto-detected).

    Returns:
        LibraryReindexResult indicating status.
    """
    # Resolve library path
    if library_path is None:
        library_path = _get_default_library_path()

    if not library_path.exists():
        return LibraryReindexResult(
            success=False,
            errors=[f"Library path does not exist: {library_path}"],
        )

    # Call the reindex function (currently returns False as not implemented)
    success = reindex_library(library_path)

    if success:
        return LibraryReindexResult(
            success=True,
            implemented=True,
        )
    else:
        return LibraryReindexResult(
            success=True,  # Not an error, just not implemented
            implemented=False,
            errors=["Reindex is not yet implemented. Use incremental cataloging."],
        )
