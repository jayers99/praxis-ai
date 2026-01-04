"""Research library search and catalog parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

CoverageLevel = Literal["good", "partial", "limited", "none"]

# Stop words for basic keyword extraction
STOP_WORDS = {
    "what",
    "is",
    "are",
    "the",
    "a",
    "an",
    "how",
    "why",
    "where",
    "when",
    "do",
    "does",
    "can",
    "could",
    "would",
    "should",
    "about",
    "for",
    "in",
    "on",
    "to",
    "of",
    "and",
    "or",
    "with",
}


@dataclass
class LibraryMatch:
    """A single matching artifact from the research library."""

    id: str  # e.g., "roles-rationale-2025-12-28"
    title: str  # e.g., "Rationale for Praxis Roles Architecture"
    path: Path  # e.g., Path("roles/rationale.md")
    topic: str  # e.g., "roles"
    consensus: str  # e.g., "High"
    date: str  # e.g., "2025-12-28"
    keywords: list[str]  # e.g., ["praxis-roles", "accountability"]
    relevance_score: float  # 0.0-1.0


@dataclass
class Citation:
    """A citation for a library artifact."""

    artifact_id: str
    title: str
    path: Path
    consensus: str
    date: str
    key_finding: str


@dataclass
class CoverageAssessment:
    """Assessment of how well the library covers a topic."""

    level: CoverageLevel
    match_count: int
    avg_relevance: float
    reasoning: str


@dataclass
class LibraryResponse:
    """Response from a library query."""

    query: str
    coverage: CoverageAssessment
    summary: str
    sources: list[Citation]
    gaps: list[str]


def parse_catalog(catalog_path: Path) -> list[dict[str, Any]]:
    """Parse CATALOG.md and extract artifact metadata.

    Args:
        catalog_path: Path to CATALOG.md file.

    Returns:
        List of dictionaries with artifact metadata.
        Returns empty list if file is missing or malformed.
    """
    if not catalog_path.exists():
        return []

    try:
        content = catalog_path.read_text(encoding="utf-8")
    except Exception:
        # Log warning but don't fail
        return []

    artifacts: list[dict[str, Any]] = []

    # Parse the Quick Reference table (primary source)
    # Format: | [id](path) | Title | Topic | Consensus | Date |
    quick_ref_pattern = (
        r"\|\s*\[([^\]]+)\]\(([^\)]+)\)\s*\|"
        r"\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|"
        r"\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|"
    )

    for match in re.finditer(quick_ref_pattern, content):
        artifact_id = match.group(1).strip()
        path = match.group(2).strip()
        title = match.group(3).strip()
        topic = match.group(4).strip()
        consensus = match.group(5).strip()
        date = match.group(6).strip()

        artifacts.append(
            {
                "id": artifact_id,
                "path": path,
                "title": title,
                "topic": topic,
                "consensus": consensus,
                "date": date,
                "keywords": [],  # Will be populated from keyword index if needed
            }
        )

    # Parse keyword index to augment artifacts
    # Find the "By Topic" section and extract keywords per artifact
    topic_section_match = re.search(
        r"## By Topic\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL
    )
    if topic_section_match:
        topic_content = topic_section_match.group(1)
        # Pattern for keyword rows: | [id](path) | Title | Consensus | Keywords |
        keyword_pattern = (
            r"\|\s*\[([^\]]+)\]\([^\)]+\)\s*\|"
            r"\s*[^\|]+\s*\|\s*[^\|]+\s*\|\s*([^\|]+)\s*\|"
        )
        for match in re.finditer(keyword_pattern, topic_content):
            artifact_id = match.group(1).strip()
            keywords_str = match.group(2).strip()
            # Parse keywords (comma-separated)
            keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]

            # Update artifact with keywords
            for artifact in artifacts:
                if artifact["id"] == artifact_id:
                    artifact["keywords"] = keywords
                    break

    return artifacts


def calculate_relevance_score(
    artifact: dict[str, Any], query_terms: list[str]
) -> float:
    """Calculate relevance score for an artifact based on query terms.

    Scoring:
    - Exact keyword match: +0.4
    - Partial keyword match: +0.2
    - Title contains word: +0.2
    - Topic matches word: +0.1
    - Last 30 days recency: +0.1 (only if content match exists)

    Args:
        artifact: Artifact metadata dictionary.
        query_terms: List of normalized query terms.

    Returns:
        Relevance score between 0.0 and 1.0.
    """
    score = 0.0

    # Normalize for comparison
    title_lower = artifact["title"].lower()
    topic_lower = artifact["topic"].lower()
    keywords_lower = [k.lower() for k in artifact["keywords"]]
    artifact_id_lower = artifact["id"].lower()

    for term in query_terms:
        term_lower = term.lower()

        # Exact keyword match
        if term_lower in keywords_lower:
            score += 0.4
        else:
            # Partial keyword match (substring)
            for keyword in keywords_lower:
                if term_lower in keyword or keyword in term_lower:
                    score += 0.2
                    break

        # Title contains word
        if term_lower in title_lower or term_lower in artifact_id_lower:
            score += 0.2

        # Topic matches word
        if term_lower in topic_lower or topic_lower in term_lower:
            score += 0.1

    # Recency bonus (last 30 days) - only if there's already a content match
    # Simple heuristic: check if date contains recent year/month
    # For MVP, just check if date starts with "2026-01" or "2025-12"
    if score > 0:
        date = artifact.get("date", "")
        if date.startswith("2026-01") or date.startswith("2025-12"):
            score += 0.1

    # Cap at 1.0
    return min(score, 1.0)


def search_library(
    query: str,
    catalog_path: Path,
    topic_filter: str | None = None,
    min_score: float = 0.1,
) -> list[LibraryMatch]:
    """Search the research library catalog for relevant artifacts.

    Args:
        query: Search query string (e.g., "roles scrum").
        catalog_path: Path to CATALOG.md file.
        topic_filter: Optional topic to filter by (e.g., "roles").
        min_score: Minimum relevance score threshold (default 0.1).

    Returns:
        List of LibraryMatch objects, ranked by relevance (highest first).
        Returns empty list if catalog doesn't exist or is malformed.
    """
    artifacts = parse_catalog(catalog_path)
    if not artifacts:
        return []

    # Normalize query into terms
    query_terms = [term.strip() for term in query.split() if term.strip()]
    if not query_terms:
        return []

    matches: list[LibraryMatch] = []

    for artifact in artifacts:
        # Apply topic filter if provided
        if topic_filter and artifact["topic"] != topic_filter:
            continue

        # Calculate relevance score
        score = calculate_relevance_score(artifact, query_terms)

        # Skip if below threshold
        if score < min_score:
            continue

        # Create LibraryMatch
        keywords_list = artifact.get("keywords", [])
        if not isinstance(keywords_list, list):
            keywords_list = []

        match = LibraryMatch(
            id=str(artifact["id"]),
            title=str(artifact["title"]),
            path=Path(artifact["path"]),
            topic=str(artifact["topic"]),
            consensus=str(artifact["consensus"]),
            date=str(artifact["date"]),
            keywords=keywords_list,
            relevance_score=score,
        )
        matches.append(match)

    # Sort by relevance score (descending)
    matches.sort(key=lambda m: m.relevance_score, reverse=True)

    return matches


def extract_keywords(question: str) -> list[str]:
    """Extract searchable keywords from a question.

    Removes stop words and short words (< 3 characters).

    Args:
        question: Natural language question.

    Returns:
        List of keywords extracted from the question.
    """
    # Remove punctuation and split into words
    words = re.sub(r"[^\w\s]", " ", question.lower()).split()
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]


def get_artifact_summary(artifact_id: str, library_path: Path) -> str:
    """Extract executive summary from artifact.

    Args:
        artifact_id: Artifact identifier.
        library_path: Path to research library root (containing CATALOG.md).

    Returns:
        Content from the Executive Summary section.
        Returns empty string if artifact not found or no summary section.
    """
    # First, find the artifact path from the catalog
    catalog_path = library_path / "CATALOG.md"
    artifacts = parse_catalog(catalog_path)

    artifact_path = None
    for artifact in artifacts:
        if artifact["id"] == artifact_id:
            artifact_path = library_path / artifact["path"]
            break

    if not artifact_path or not artifact_path.exists():
        return ""

    try:
        content = artifact_path.read_text(encoding="utf-8")
    except Exception:
        return ""

    # Find the Executive Summary section
    # Pattern: ## Executive Summary followed by content until next ##
    pattern = r"## Executive Summary\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        summary = match.group(1).strip()
        return summary

    return ""


def assess_coverage(query: str, library_path: Path) -> CoverageAssessment:
    """Assess how well the library covers a topic.

    Coverage thresholds:
    - good: 3+ matches, avg relevance >= 0.6
    - partial: 1-2 matches, avg relevance >= 0.4
    - limited: 1+ matches, avg relevance < 0.4
    - none: 0 matches

    Args:
        query: Search query or topic.
        library_path: Path to research library root (containing CATALOG.md).

    Returns:
        CoverageAssessment with level and reasoning.
    """
    catalog_path = library_path / "CATALOG.md"
    keywords = extract_keywords(query)

    # Use search_library with extracted keywords
    search_query = " ".join(keywords) if keywords else query
    matches = search_library(search_query, catalog_path, min_score=0.1)

    match_count = len(matches)
    if match_count > 0:
        avg_relevance = sum(m.relevance_score for m in matches) / match_count
    else:
        avg_relevance = 0.0

    # Determine coverage level based on thresholds
    if match_count == 0:
        level: CoverageLevel = "none"
        reasoning = f"No matching artifacts found for query: {query}"
    elif match_count >= 3 and avg_relevance >= 0.6:
        level = "good"
        reasoning = (
            f"Found {match_count} highly relevant artifacts "
            f"(avg relevance: {avg_relevance:.2f})"
        )
    elif (match_count >= 1 and match_count <= 2 and avg_relevance >= 0.4) or (
        match_count >= 3 and avg_relevance >= 0.4
    ):
        level = "partial"
        reasoning = (
            f"Found {match_count} moderately relevant artifact(s) "
            f"(avg relevance: {avg_relevance:.2f})"
        )
    else:
        level = "limited"
        reasoning = (
            f"Found {match_count} artifact(s) with low relevance "
            f"(avg relevance: {avg_relevance:.2f})"
        )

    return CoverageAssessment(
        level=level,
        match_count=match_count,
        avg_relevance=avg_relevance,
        reasoning=reasoning,
    )


def get_citations(artifact_id: str, library_path: Path) -> list[Citation]:
    """Get formatted citations for an artifact.

    Args:
        artifact_id: Artifact identifier.
        library_path: Path to research library root (containing CATALOG.md).

    Returns:
        List containing a single Citation for the artifact.
        Returns empty list if artifact not found.
    """
    catalog_path = library_path / "CATALOG.md"
    artifacts = parse_catalog(catalog_path)

    for artifact in artifacts:
        if artifact["id"] == artifact_id:
            # Extract a key finding from the summary
            summary = get_artifact_summary(artifact_id, library_path)
            # Use first line or first sentence as key finding
            key_finding = ""
            if summary:
                lines = summary.split("\n")
                # Find first non-empty line
                for line in lines:
                    stripped = line.strip()
                    if stripped and not stripped.startswith("-"):
                        key_finding = stripped
                        break
                # If still empty, use first bullet point
                if not key_finding:
                    for line in lines:
                        stripped = line.strip()
                        if stripped.startswith("-"):
                            key_finding = stripped[1:].strip()
                            break

            citation = Citation(
                artifact_id=artifact["id"],
                title=artifact["title"],
                path=Path(artifact["path"]),
                consensus=artifact["consensus"],
                date=artifact["date"],
                key_finding=key_finding,
            )
            return [citation]

    return []


def query_library(question: str, library_path: Path) -> LibraryResponse:
    """Answer a question using library artifacts.

    Args:
        question: Natural language question.
        library_path: Path to research library root (containing CATALOG.md).

    Returns:
        LibraryResponse with coverage assessment, summary, sources, and gaps.
    """
    # Handle empty query
    if not question or not question.strip():
        return LibraryResponse(
            query="",
            coverage=CoverageAssessment(
                level="none",
                match_count=0,
                avg_relevance=0.0,
                reasoning="Empty query provided",
            ),
            summary="",
            sources=[],
            gaps=[],
        )

    # Extract keywords from question
    keywords = extract_keywords(question)
    search_query = " ".join(keywords) if keywords else question

    # Search library
    catalog_path = library_path / "CATALOG.md"
    matches = search_library(search_query, catalog_path, min_score=0.1)

    # Assess coverage
    coverage = assess_coverage(question, library_path)

    # Build response based on coverage
    if coverage.level == "none":
        return LibraryResponse(
            query=question,
            coverage=coverage,
            summary="",
            sources=[],
            gaps=[question],
        )

    # Extract summaries from top matches (up to 3)
    top_matches = matches[:3]
    summaries = []
    sources = []

    for match in top_matches:
        summary = get_artifact_summary(match.id, library_path)
        if summary:
            summaries.append(summary)

        # Create citation
        citation = Citation(
            artifact_id=match.id,
            title=match.title,
            path=match.path,
            consensus=match.consensus,
            date=match.date,
            key_finding=summary.split("\n")[0].strip() if summary else "",
        )
        sources.append(citation)

    # Combine summaries
    combined_summary = "\n\n".join(summaries) if summaries else ""

    # Identify gaps (topics mentioned but not well covered)
    gaps = []
    if coverage.level in ["limited", "partial"]:
        # Extract topics that may not be well covered
        for keyword in keywords:
            # Check if this keyword has low coverage
            keyword_lower = keyword.lower()
            keyword_matches = [
                m
                for m in matches
                if keyword_lower in m.title.lower()
                or keyword_lower in " ".join(m.keywords).lower()
            ]
            if len(keyword_matches) < 2:
                gaps.append(keyword)

    return LibraryResponse(
        query=question,
        coverage=coverage,
        summary=combined_summary,
        sources=sources,
        gaps=gaps,
    )
