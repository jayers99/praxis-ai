"""Research artifact metadata parser.

Parses metadata from research artifacts stored in HTML comments with embedded YAML.
Validates metadata according to Cataloger role requirements.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from praxis.domain.catalog import CatalogEntry, CatalogResult, ValidationError


def parse_artifact_metadata(artifact_path: Path) -> dict[str, Any]:
    """Parse metadata from a research artifact.

    Extracts metadata from HTML comment blocks in the format:
    <!--
    metadata:
      id: artifact-id-2026-01-01
      title: Artifact Title
      ...
    -->

    Args:
        artifact_path: Path to the research artifact markdown file.

    Returns:
        Dictionary of metadata fields. Returns empty dict if no metadata found.

    Raises:
        FileNotFoundError: If artifact_path does not exist.
        yaml.YAMLError: If metadata YAML is malformed.
    """
    if not artifact_path.exists():
        raise FileNotFoundError(f"Artifact not found: {artifact_path}")

    content = artifact_path.read_text(encoding="utf-8")

    # Match HTML comment block with metadata
    # Pattern: <!-- ... metadata: ... -->
    pattern = r"<!--\s*\n?\s*metadata:\s*\n(.*?)\n\s*-->"
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        return {}

    yaml_content = match.group(1)

    # Parse YAML content
    try:
        metadata = yaml.safe_load(yaml_content)
        if not isinstance(metadata, dict):
            return {}
        return metadata
    except yaml.YAMLError:
        # Re-raise to let caller handle malformed YAML
        raise


def validate_artifact_metadata(metadata: dict[str, Any], artifact_path: Path | None = None) -> CatalogResult:
    """Validate artifact metadata against Cataloger role requirements.

    Required fields per core/roles/definitions/cataloger.md:
    - id: Unique, format {topic}-{slug}-{YYYY-MM-DD}
    - title: Non-empty string
    - date: ISO date format (YYYY-MM-DD)
    - status: Must be "approved" or "validated"
    - topic: Valid topic folder name
    - keywords: 3-7 searchable terms
    - consensus: Non-empty string
    - sources_count: Integer >= 0

    Args:
        metadata: Dictionary of metadata fields from artifact.
        artifact_path: Optional path for constructing relative path.

    Returns:
        CatalogResult with validation outcome.
    """
    errors: list[ValidationError] = []

    # Validate required fields
    required_fields = [
        "id",
        "title",
        "date",
        "status",
        "topic",
        "keywords",
        "consensus",
        "sources_count",
    ]

    for field_name in required_fields:
        if field_name not in metadata or metadata[field_name] is None:
            errors.append(ValidationError(field=field_name, message=f"{field_name}: required field missing"))

    # If basic required fields are missing, return early
    if errors:
        return CatalogResult(success=False, errors=errors)

    # Validate id format: {topic}-{slug}-{YYYY-MM-DD}
    id_pattern = r"^[a-z0-9-]+-\d{4}-\d{2}-\d{2}$"
    if not re.match(id_pattern, str(metadata["id"])):
        errors.append(
            ValidationError(
                field="id",
                message=f"id: invalid format, expected {{topic}}-{{slug}}-{{YYYY-MM-DD}}, got: {metadata['id']}",
            )
        )

    # Validate title is non-empty
    if not str(metadata["title"]).strip():
        errors.append(ValidationError(field="title", message="title: cannot be empty"))

    # Validate date format: YYYY-MM-DD
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, str(metadata["date"])):
        errors.append(
            ValidationError(
                field="date",
                message=f"date: invalid format, expected YYYY-MM-DD, got: {metadata['date']}",
            )
        )

    # Validate status: must be "approved" or "validated"
    status = str(metadata["status"]).lower()
    if status not in ["approved", "validated"]:
        errors.append(
            ValidationError(
                field="status",
                message=f"status: must be 'approved' or 'validated', got: {metadata['status']}",
            )
        )

    # Validate topic is non-empty
    if not str(metadata["topic"]).strip():
        errors.append(ValidationError(field="topic", message="topic: cannot be empty"))

    # Validate keywords: must be a list with 3-7 items
    keywords = metadata.get("keywords", [])
    if not isinstance(keywords, list):
        errors.append(ValidationError(field="keywords", message="keywords: must be a list"))
    elif len(keywords) < 3:
        errors.append(
            ValidationError(
                field="keywords",
                message=f"keywords: must have at least 3 items, got {len(keywords)}",
            )
        )
    elif len(keywords) > 7:
        errors.append(
            ValidationError(
                field="keywords",
                message=f"keywords: must have at most 7 items, got {len(keywords)}",
            )
        )

    # Validate consensus is non-empty
    if not str(metadata["consensus"]).strip():
        errors.append(ValidationError(field="consensus", message="consensus: cannot be empty"))

    # Validate sources_count: must be integer >= 0
    try:
        sources_count = int(metadata["sources_count"])
        if sources_count < 0:
            errors.append(
                ValidationError(
                    field="sources_count",
                    message=f"sources_count: must be >= 0, got {sources_count}",
                )
            )
    except (ValueError, TypeError):
        errors.append(
            ValidationError(
                field="sources_count",
                message=f"sources_count: must be an integer, got: {metadata['sources_count']}",
            )
        )

    # If there are validation errors, return failure
    if errors:
        return CatalogResult(success=False, errors=errors)

    # Construct path from topic and filename if artifact_path provided
    if artifact_path:
        relative_path = Path(metadata["topic"]) / artifact_path.name
    else:
        relative_path = Path(metadata["topic"]) / f"{metadata['id']}.md"

    # Create CatalogEntry
    entry = CatalogEntry(
        id=str(metadata["id"]),
        title=str(metadata["title"]),
        date=str(metadata["date"]),
        status=str(metadata["status"]),
        topic=str(metadata["topic"]),
        keywords=list(metadata["keywords"]),
        consensus=str(metadata["consensus"]),
        sources_count=int(metadata["sources_count"]),
        path=relative_path,
        also_relevant=metadata.get("also_relevant"),
        supersedes=metadata.get("supersedes"),
        related=metadata.get("related"),
    )

    return CatalogResult(success=True, entry=entry)
