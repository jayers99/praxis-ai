"""Research library cataloging service.

Orchestrates cataloging of research artifacts into the research library.
Implements the Cataloger role operations.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from praxis.domain.catalog import CatalogEntry, CatalogResult
from praxis.infrastructure.catalog_metadata_parser import (
    parse_artifact_metadata,
    validate_artifact_metadata,
)
from praxis.infrastructure.catalog_writer import update_catalog


def validate_metadata(artifact_path: Path) -> CatalogResult:
    """Validate artifact metadata.
    
    Args:
        artifact_path: Path to the research artifact.
        
    Returns:
        CatalogResult with validation outcome.
    """
    try:
        metadata = parse_artifact_metadata(artifact_path)
    except Exception as e:
        from praxis.domain.catalog import ValidationError
        
        return CatalogResult(
            success=False,
            errors=[ValidationError(field="metadata", message=str(e))],
        )
    
    if not metadata:
        from praxis.domain.catalog import ValidationError
        
        return CatalogResult(
            success=False,
            errors=[
                ValidationError(
                    field="metadata",
                    message="No metadata block found in artifact",
                )
            ],
        )
    
    return validate_artifact_metadata(metadata, artifact_path)


def check_duplicate_id(artifact_id: str, catalog_path: Path) -> bool:
    """Check if an artifact ID already exists in the catalog.
    
    Args:
        artifact_id: The artifact ID to check.
        catalog_path: Path to CATALOG.md.
        
    Returns:
        True if ID exists, False otherwise.
    """
    if not catalog_path.exists():
        return False
    
    content = catalog_path.read_text(encoding="utf-8")
    # Look for ID in Quick Reference section
    # Pattern: | [id](path) | ...
    import re
    
    pattern = rf"\|\s*\[{re.escape(artifact_id)}\]\("
    return bool(re.search(pattern, content))


def catalog_artifact(
    artifact_path: Path,
    topic: str,
    library_path: Path,
    catalog_path: Path | None = None,
) -> CatalogResult:
    """Catalog a research artifact into the research library.
    
    Full workflow:
    1. Validate metadata
    2. Check for duplicate ID
    3. Create topic folder if needed
    4. Move artifact to topic folder
    5. Update CATALOG.md
    
    Args:
        artifact_path: Path to the artifact to catalog.
        topic: Topic folder name (e.g., "patterns", "roles").
        library_path: Path to research-library directory.
        catalog_path: Optional path to CATALOG.md (defaults to library_path/CATALOG.md).
        
    Returns:
        CatalogResult with outcome.
    """
    # Default catalog path
    if catalog_path is None:
        catalog_path = library_path / "CATALOG.md"
    
    # Step 1: Validate metadata
    validation_result = validate_metadata(artifact_path)
    if not validation_result.success:
        return validation_result
    
    assert validation_result.entry is not None
    entry = validation_result.entry
    
    # Step 2: Check for duplicate ID
    if check_duplicate_id(entry.id, catalog_path):
        from praxis.domain.catalog import ValidationError
        
        return CatalogResult(
            success=False,
            errors=[
                ValidationError(
                    field="id", message=f"duplicate ID: {entry.id}"
                )
            ],
        )
    
    # Step 3: Create topic folder if needed
    topic_path = library_path / topic
    topic_path.mkdir(parents=True, exist_ok=True)
    
    # Step 4: Move artifact to topic folder
    destination = topic_path / artifact_path.name
    shutil.copy2(artifact_path, destination)
    
    # Update entry path to be relative to library
    entry.path = Path(topic) / artifact_path.name
    
    # Step 5: Update CATALOG.md
    try:
        update_catalog(catalog_path, entry)
    except Exception as e:
        # Rollback: remove copied file
        if destination.exists():
            destination.unlink()
        
        from praxis.domain.catalog import ValidationError
        
        return CatalogResult(
            success=False,
            errors=[
                ValidationError(
                    field="catalog",
                    message=f"Failed to update catalog: {e}",
                )
            ],
        )
    
    return CatalogResult(success=True, entry=entry)


def find_orphans(library_path: Path, catalog_path: Path | None = None) -> list[Path]:
    """Find artifacts not listed in CATALOG.md.
    
    Args:
        library_path: Path to research-library directory.
        catalog_path: Optional path to CATALOG.md (defaults to library_path/CATALOG.md).
        
    Returns:
        List of relative paths to orphaned artifacts.
    """
    if catalog_path is None:
        catalog_path = library_path / "CATALOG.md"
    
    if not catalog_path.exists():
        return []
    
    # Get all markdown files in library (excluding CATALOG.md and _index.md files)
    all_artifacts: set[Path] = set()
    for md_file in library_path.rglob("*.md"):
        # Skip CATALOG.md and _index.md files
        if md_file.name in ["CATALOG.md", "_index.md"]:
            continue
        # Get path relative to library_path
        rel_path = md_file.relative_to(library_path)
        all_artifacts.add(rel_path)
    
    # Get all artifacts listed in catalog
    content = catalog_path.read_text(encoding="utf-8")
    
    # Parse Quick Reference table to get cataloged paths
    import re
    
    # Pattern: | [id](path) | ...
    pattern = r"\|\s*\[[^\]]+\]\(([^\)]+)\)\s*\|"
    cataloged_paths: set[Path] = set()
    
    for match in re.finditer(pattern, content):
        path_str = match.group(1).strip()
        cataloged_paths.add(Path(path_str))
    
    # Find orphans: artifacts not in catalog
    orphans = all_artifacts - cataloged_paths
    
    return sorted(orphans)


def reindex_library(library_path: Path, catalog_path: Path | None = None) -> bool:
    """Rebuild CATALOG.md from all artifacts in the library.
    
    This is a complete rebuild operation. It:
    1. Scans all artifacts in the library
    2. Validates their metadata
    3. Rebuilds CATALOG.md from scratch
    
    Note: This is currently a placeholder. Full implementation would require
    reading all artifacts and reconstructing the entire CATALOG.md file.
    For MVP, we rely on incremental updates via catalog_artifact().
    
    Args:
        library_path: Path to research-library directory.
        catalog_path: Optional path to CATALOG.md (defaults to library_path/CATALOG.md).
        
    Returns:
        True if successful, False otherwise.
    """
    # Placeholder for future implementation
    # Full reindexing would:
    # 1. Scan all .md files (excluding CATALOG.md, _index.md)
    # 2. Parse and validate metadata from each
    # 3. Rebuild CATALOG.md structure from scratch
    # 4. Ensure deterministic ordering (by date, then by ID)
    
    # For MVP, return False to indicate not yet implemented
    return False
