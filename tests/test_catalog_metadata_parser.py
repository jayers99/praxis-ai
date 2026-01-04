"""Unit tests for catalog metadata parser."""

from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from praxis.infrastructure.catalog_metadata_parser import (
    parse_artifact_metadata,
    validate_artifact_metadata,
)


@pytest.fixture
def tmp_artifact(tmp_path: Path) -> Path:
    """Create a temporary artifact file."""
    artifact = tmp_path / "test-artifact.md"
    return artifact


def test_parse_artifact_metadata_valid(tmp_artifact: Path) -> None:
    """Test parsing valid artifact metadata."""
    content = dedent("""\
        # Test Artifact
        
        <!--
        metadata:
          id: patterns-test-artifact-2026-01-04
          title: Test Artifact Title
          date: 2026-01-04
          status: approved
          topic: patterns
          keywords: [test, example, validation]
          consensus: high
          sources_count: 5
        -->
        
        ## Body content
        
        Some content here.
    """)
    tmp_artifact.write_text(content, encoding="utf-8")
    
    metadata = parse_artifact_metadata(tmp_artifact)
    
    assert metadata["id"] == "patterns-test-artifact-2026-01-04"
    assert metadata["title"] == "Test Artifact Title"
    # YAML parses dates as datetime.date objects, so convert to string
    assert str(metadata["date"]) == "2026-01-04"
    assert metadata["status"] == "approved"
    assert metadata["topic"] == "patterns"
    assert metadata["keywords"] == ["test", "example", "validation"]
    assert metadata["consensus"] == "high"
    assert metadata["sources_count"] == 5


def test_parse_artifact_metadata_no_metadata(tmp_artifact: Path) -> None:
    """Test parsing artifact with no metadata block."""
    content = dedent("""\
        # Test Artifact
        
        No metadata here.
    """)
    tmp_artifact.write_text(content, encoding="utf-8")
    
    metadata = parse_artifact_metadata(tmp_artifact)
    
    assert metadata == {}


def test_parse_artifact_metadata_file_not_found() -> None:
    """Test parsing non-existent artifact."""
    with pytest.raises(FileNotFoundError):
        parse_artifact_metadata(Path("/nonexistent/file.md"))


def test_parse_artifact_metadata_malformed_yaml(tmp_artifact: Path) -> None:
    """Test parsing artifact with malformed YAML."""
    content = dedent("""\
        # Test Artifact
        
        <!--
        metadata:
          id: invalid yaml: [unclosed bracket
        -->
    """)
    tmp_artifact.write_text(content, encoding="utf-8")
    
    with pytest.raises(yaml.YAMLError):
        parse_artifact_metadata(tmp_artifact)


def test_validate_artifact_metadata_valid() -> None:
    """Test validation with all required fields."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "approved",
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is True
    assert result.entry is not None
    assert result.entry.id == "patterns-test-artifact-2026-01-04"
    assert result.entry.title == "Test Artifact Title"
    assert len(result.errors) == 0


def test_validate_artifact_metadata_status_validated() -> None:
    """Test that 'validated' status is accepted (in addition to 'approved')."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "validated",
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is True
    assert result.entry is not None


def test_validate_artifact_metadata_missing_required_field() -> None:
    """Test validation with missing required field."""
    metadata = {
        # Missing 'id'
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "approved",
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is False
    assert len(result.errors) == 1
    assert result.errors[0].field == "id"
    assert "required field missing" in result.errors[0].message


def test_validate_artifact_metadata_invalid_id_format() -> None:
    """Test validation with invalid ID format."""
    metadata = {
        "id": "invalid-id-format",  # Missing date
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "approved",
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is False
    assert any(e.field == "id" for e in result.errors)
    assert any("invalid format" in e.message for e in result.errors)


def test_validate_artifact_metadata_invalid_date_format() -> None:
    """Test validation with invalid date format."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "01/04/2026",  # Invalid format
        "status": "approved",
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is False
    assert any(e.field == "date" for e in result.errors)


def test_validate_artifact_metadata_invalid_status() -> None:
    """Test validation with invalid status."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "draft",  # Invalid status
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is False
    assert any(e.field == "status" for e in result.errors)


def test_validate_artifact_metadata_too_few_keywords() -> None:
    """Test validation with too few keywords."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "approved",
        "topic": "patterns",
        "keywords": ["test", "example"],  # Only 2 keywords
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is False
    assert any(e.field == "keywords" for e in result.errors)
    assert any("at least 3" in e.message for e in result.errors)


def test_validate_artifact_metadata_too_many_keywords() -> None:
    """Test validation with too many keywords."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "approved",
        "topic": "patterns",
        "keywords": ["k1", "k2", "k3", "k4", "k5", "k6", "k7", "k8"],  # 8 keywords
        "consensus": "high",
        "sources_count": 5,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is False
    assert any(e.field == "keywords" for e in result.errors)
    assert any("at most 7" in e.message for e in result.errors)


def test_validate_artifact_metadata_negative_sources_count() -> None:
    """Test validation with negative sources_count."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "approved",
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": -1,
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is False
    assert any(e.field == "sources_count" for e in result.errors)


def test_validate_artifact_metadata_with_optional_fields() -> None:
    """Test validation with optional fields included."""
    metadata = {
        "id": "patterns-test-artifact-2026-01-04",
        "title": "Test Artifact Title",
        "date": "2026-01-04",
        "status": "approved",
        "topic": "patterns",
        "keywords": ["test", "example", "validation"],
        "consensus": "high",
        "sources_count": 5,
        "also_relevant": ["foundations", "roles"],
        "supersedes": "patterns-old-artifact-2025-12-01",
        "related": ["patterns-related-2026-01-01"],
    }
    
    result = validate_artifact_metadata(metadata)
    
    assert result.success is True
    assert result.entry is not None
    assert result.entry.also_relevant == ["foundations", "roles"]
    assert result.entry.supersedes == "patterns-old-artifact-2025-12-01"
    assert result.entry.related == ["patterns-related-2026-01-01"]
