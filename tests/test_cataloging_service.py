"""Integration tests for cataloging service."""

from pathlib import Path
from textwrap import dedent

import pytest

from praxis.application.cataloging_service import (
    catalog_artifact,
    check_duplicate_id,
    find_orphans,
    validate_metadata,
)


@pytest.fixture
def research_library(tmp_path: Path) -> Path:
    """Create a minimal research library structure."""
    library = tmp_path / "research-library"
    library.mkdir()
    
    # Create CATALOG.md
    catalog = library / "CATALOG.md"
    content = dedent("""\
        # Research Library Catalog
        
        _Last updated: 2026-01-01_
        _Total artifacts: 1_
        
        ---
        
        ## Quick Reference
        
        | ID | Title | Topic | Consensus | Date |
        |----|-------|-------|-----------|------|
        | [existing-artifact-2026-01-02](patterns/existing.md) | Existing Artifact | patterns | high | 2026-01-02 |
        
        ---
        
        ## By Topic
        
        ### Patterns
        
        | ID | Title | Consensus | Keywords |
        |----|-------|-----------|----------|
        | [existing-artifact-2026-01-02](patterns/existing.md) | Existing Artifact | high | test, example, pattern |
        
        ---
        
        ## By Consensus
        
        ### High Consensus
        
        - [Existing Artifact](patterns/existing.md) — patterns — test, example, pattern
        
        ### Strong Consensus
        
        _No artifacts yet_
        
        ### Medium Consensus
        
        _No artifacts yet_
        
        ### Partial Consensus (hypothesis under evaluation)
        
        _No artifacts yet_
        
        ### Low Consensus (use with caution)
        
        _No artifacts yet_
        
        ---
        
        ## Keyword Index
        
        ### test
        - [Existing Artifact](patterns/existing.md)
        
        ### example
        - [Existing Artifact](patterns/existing.md)
        
        ### pattern
        - [Existing Artifact](patterns/existing.md)
        
        ---
        
        ## Recently Added
        
        | Date | Title | Topic |
        |------|-------|-------|
        | 2026-01-02 | [Existing Artifact](patterns/existing.md) | patterns |
        
        ---
    """)
    catalog.write_text(content, encoding="utf-8")
    
    # Create existing artifact
    patterns_dir = library / "patterns"
    patterns_dir.mkdir()
    existing = patterns_dir / "existing.md"
    existing_content = dedent("""\
        # Existing Artifact
        
        <!--
        metadata:
          id: existing-artifact-2026-01-02
          title: Existing Artifact
          date: 2026-01-02
          status: approved
          topic: patterns
          keywords: [test, example, pattern]
          consensus: high
          sources_count: 3
        -->
        
        Content here.
    """)
    existing.write_text(existing_content, encoding="utf-8")
    
    return library


@pytest.fixture
def valid_artifact(tmp_path: Path) -> Path:
    """Create a valid artifact for testing."""
    artifact = tmp_path / "new-artifact.md"
    content = dedent("""\
        # New Artifact
        
        <!--
        metadata:
          id: roles-new-artifact-2026-01-04
          title: New Artifact Title
          date: 2026-01-04
          status: approved
          topic: roles
          keywords: [new, test, research]
          consensus: medium
          sources_count: 7
        -->
        
        ## Introduction
        
        Some research content here.
    """)
    artifact.write_text(content, encoding="utf-8")
    return artifact


def test_validate_metadata_valid(valid_artifact: Path) -> None:
    """Test validating artifact with valid metadata."""
    result = validate_metadata(valid_artifact)
    
    assert result.success is True
    assert result.entry is not None
    assert result.entry.id == "roles-new-artifact-2026-01-04"
    assert len(result.errors) == 0


def test_validate_metadata_missing_metadata(tmp_path: Path) -> None:
    """Test validating artifact with no metadata."""
    artifact = tmp_path / "no-metadata.md"
    artifact.write_text("# Artifact\n\nNo metadata here.", encoding="utf-8")
    
    result = validate_metadata(artifact)
    
    assert result.success is False
    assert len(result.errors) > 0
    assert any("No metadata block" in e.message for e in result.errors)


def test_check_duplicate_id(research_library: Path) -> None:
    """Test checking for duplicate IDs."""
    catalog_path = research_library / "CATALOG.md"
    
    # Existing ID should be found
    assert check_duplicate_id("existing-artifact-2026-01-02", catalog_path) is True
    
    # New ID should not be found
    assert check_duplicate_id("new-artifact-2026-01-04", catalog_path) is False


def test_catalog_artifact_success(
    valid_artifact: Path, research_library: Path
) -> None:
    """Test successfully cataloging an artifact."""
    catalog_path = research_library / "CATALOG.md"
    
    result = catalog_artifact(
        valid_artifact,
        topic="roles",
        library_path=research_library,
        catalog_path=catalog_path,
    )
    
    assert result.success is True
    assert result.entry is not None
    assert result.entry.id == "roles-new-artifact-2026-01-04"
    
    # Verify artifact was moved
    destination = research_library / "roles" / "new-artifact.md"
    assert destination.exists()
    
    # Verify CATALOG.md was updated
    catalog_content = catalog_path.read_text(encoding="utf-8")
    assert "roles-new-artifact-2026-01-04" in catalog_content
    assert "New Artifact Title" in catalog_content
    assert "_Total artifacts: 2_" in catalog_content


def test_catalog_artifact_duplicate_id(
    valid_artifact: Path, research_library: Path
) -> None:
    """Test cataloging artifact with duplicate ID."""
    catalog_path = research_library / "CATALOG.md"
    
    # Modify artifact to have existing ID
    content = valid_artifact.read_text(encoding="utf-8")
    content = content.replace(
        "roles-new-artifact-2026-01-04", "existing-artifact-2026-01-02"
    )
    valid_artifact.write_text(content, encoding="utf-8")
    
    result = catalog_artifact(
        valid_artifact,
        topic="patterns",
        library_path=research_library,
        catalog_path=catalog_path,
    )
    
    assert result.success is False
    assert any("duplicate ID" in e.message for e in result.errors)


def test_catalog_artifact_creates_topic_folder(
    valid_artifact: Path, research_library: Path
) -> None:
    """Test that cataloging creates topic folder if missing."""
    catalog_path = research_library / "CATALOG.md"
    
    # Topic "roles" doesn't exist yet
    assert not (research_library / "roles").exists()
    
    result = catalog_artifact(
        valid_artifact,
        topic="roles",
        library_path=research_library,
        catalog_path=catalog_path,
    )
    
    assert result.success is True
    
    # Verify topic folder was created
    assert (research_library / "roles").exists()
    assert (research_library / "roles" / "new-artifact.md").exists()


def test_find_orphans_no_orphans(research_library: Path) -> None:
    """Test finding orphans when none exist."""
    orphans = find_orphans(research_library)
    
    assert len(orphans) == 0


def test_find_orphans_with_orphan(research_library: Path) -> None:
    """Test finding orphaned artifacts."""
    # Create an orphan artifact
    orphan = research_library / "patterns" / "orphan.md"
    orphan.write_text("# Orphan\n\nNot in catalog.", encoding="utf-8")
    
    orphans = find_orphans(research_library)
    
    assert len(orphans) == 1
    assert Path("patterns/orphan.md") in orphans


def test_find_orphans_ignores_catalog_and_index(research_library: Path) -> None:
    """Test that find_orphans ignores CATALOG.md and _index.md files."""
    # Create _index.md file
    index = research_library / "patterns" / "_index.md"
    index.write_text("# Index\n\nTopic index.", encoding="utf-8")
    
    orphans = find_orphans(research_library)
    
    # Should not include CATALOG.md or _index.md
    assert len(orphans) == 0
