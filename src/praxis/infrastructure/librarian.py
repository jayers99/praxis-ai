"""Research library search and catalog parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


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
