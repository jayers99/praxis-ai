"""Unit tests for catalog writer."""

from pathlib import Path
from textwrap import dedent

import pytest

from praxis.domain.catalog import CatalogEntry
from praxis.infrastructure.catalog_writer import (
    _find_section_boundaries,
    _update_quick_reference,
    _update_recently_added,
    update_catalog,
)


@pytest.fixture
def minimal_catalog(tmp_path: Path) -> Path:
    """Create a minimal CATALOG.md for testing."""
    catalog = tmp_path / "CATALOG.md"
    content = dedent("""\
        # Research Library Catalog

        _Last updated: 2026-01-01_
        _Total artifacts: 2_

        ---

        ## Quick Reference

        | ID | Title | Topic | Consensus | Date |
        |----|-------|-------|-----------|------|
        | [existing-artifact-2026-01-02](patterns/existing.md) | Existing Artifact | patterns | high | 2026-01-02 |
        | [older-artifact-2026-01-01](roles/older.md) | Older Artifact | roles | medium | 2026-01-01 |

        ---

        ## By Topic

        ### Patterns

        | ID | Title | Consensus | Keywords |
        |----|-------|-----------|----------|
        | [existing-artifact-2026-01-02](patterns/existing.md) | Existing Artifact | high | test, example |

        ### Roles

        | ID | Title | Consensus | Keywords |
        |----|-------|-----------|----------|
        | [older-artifact-2026-01-01](roles/older.md) | Older Artifact | medium | test |

        ---

        ## By Consensus

        ### High Consensus

        - [Existing Artifact](patterns/existing.md) — patterns — test, example

        ### Strong Consensus

        _No artifacts yet_

        ### Medium Consensus

        - [Older Artifact](roles/older.md) — roles — test

        ### Partial Consensus (hypothesis under evaluation)

        _No artifacts yet_

        ### Low Consensus (use with caution)

        _No artifacts yet_

        ---

        ## Keyword Index

        ### test
        - [Existing Artifact](patterns/existing.md)
        - [Older Artifact](roles/older.md)

        ### example
        - [Existing Artifact](patterns/existing.md)

        ---

        ## Recently Added

        | Date | Title | Topic |
        |------|-------|-------|
        | 2026-01-02 | [Existing Artifact](patterns/existing.md) | patterns |
        | 2026-01-01 | [Older Artifact](roles/older.md) | roles |

        ---
    """)
    catalog.write_text(content, encoding="utf-8")
    return catalog


def test_find_section_boundaries() -> None:
    """Test finding section boundaries."""
    content = dedent("""\
        # Title

        ## Section One

        Content here.

        ## Section Two

        More content.
    """)

    boundaries = _find_section_boundaries(content, "## Section One")
    assert boundaries is not None
    start, end = boundaries
    section = content[start:end]
    assert "Content here." in section
    assert "Section Two" not in section


def test_find_section_boundaries_not_found() -> None:
    """Test finding non-existent section."""
    content = "# Title\n\n## Section One\n\nContent"

    boundaries = _find_section_boundaries(content, "## Missing Section")
    assert boundaries is None


def test_update_quick_reference(minimal_catalog: Path) -> None:
    """Test updating Quick Reference table."""
    content = minimal_catalog.read_text(encoding="utf-8")

    entry = CatalogEntry(
        id="new-artifact-2026-01-03",
        title="New Artifact",
        date="2026-01-03",
        status="approved",
        topic="foundations",
        keywords=["new", "test", "example"],
        consensus="high",
        sources_count=3,
        path=Path("foundations/new.md"),
    )

    updated = _update_quick_reference(content, entry)

    # Check that new entry is added
    assert "new-artifact-2026-01-03" in updated
    assert "New Artifact" in updated
    assert "foundations" in updated

    # Check date ordering (newest first)
    lines = updated.split("\n")
    quick_ref_lines = []
    in_quick_ref = False
    for line in lines:
        if "## Quick Reference" in line:
            in_quick_ref = True
        elif in_quick_ref and line.startswith("| ["):
            quick_ref_lines.append(line)
        elif in_quick_ref and line.startswith("---"):
            break

    # First entry should be the newest (2026-01-03)
    assert "new-artifact-2026-01-03" in quick_ref_lines[0]
    assert "existing-artifact-2026-01-02" in quick_ref_lines[1]
    assert "older-artifact-2026-01-01" in quick_ref_lines[2]


def test_update_recently_added(minimal_catalog: Path) -> None:
    """Test updating Recently Added section."""
    content = minimal_catalog.read_text(encoding="utf-8")

    entry = CatalogEntry(
        id="new-artifact-2026-01-03",
        title="New Artifact",
        date="2026-01-03",
        status="approved",
        topic="foundations",
        keywords=["new", "test", "example"],
        consensus="high",
        sources_count=3,
        path=Path("foundations/new.md"),
    )

    updated = _update_recently_added(content, entry)

    # Check that new entry is at the top
    lines = updated.split("\n")
    recently_added_lines = []
    in_recently_added = False
    for line in lines:
        if "## Recently Added" in line:
            in_recently_added = True
        elif in_recently_added and line.strip().startswith("| 20"):
            recently_added_lines.append(line)
        elif in_recently_added and line.startswith("---"):
            break

    # First entry should be the new one
    assert "2026-01-03" in recently_added_lines[0]
    assert "New Artifact" in recently_added_lines[0]


def test_update_catalog_full_integration(minimal_catalog: Path) -> None:
    """Test full catalog update (all sections)."""
    entry = CatalogEntry(
        id="new-artifact-2026-01-03",
        title="New Artifact",
        date="2026-01-03",
        status="approved",
        topic="foundations",
        keywords=["new", "test", "validation"],
        consensus="medium",
        sources_count=5,
        path=Path("foundations/new.md"),
    )

    update_catalog(minimal_catalog, entry)

    updated_content = minimal_catalog.read_text(encoding="utf-8")

    # Verify Quick Reference updated
    assert "new-artifact-2026-01-03" in updated_content
    assert "New Artifact" in updated_content

    # Verify metadata updated
    assert "_Total artifacts: 3_" in updated_content
    assert "_Last updated: 2026-01-" in updated_content

    # Verify By Topic section updated (should create new Foundations section)
    assert "### Foundations" in updated_content

    # Verify keywords added to Keyword Index
    assert "### new" in updated_content
    assert "### validation" in updated_content

    # Verify Recently Added updated
    # Extract the Recently Added section more carefully
    assert "## Recently Added" in updated_content
    lines = updated_content.split("\n")
    in_recently = False
    recently_lines = []
    for line in lines:
        if "## Recently Added" in line:
            in_recently = True
        elif in_recently:
            if line.strip().startswith("| 2026-01-03"):
                recently_lines.append(line)
                break
    assert len(recently_lines) > 0, "New entry not found in Recently Added"
    assert "New Artifact" in recently_lines[0]


def test_update_catalog_file_not_found(tmp_path: Path) -> None:
    """Test updating non-existent catalog."""
    entry = CatalogEntry(
        id="new-artifact-2026-01-03",
        title="New Artifact",
        date="2026-01-03",
        status="approved",
        topic="foundations",
        keywords=["new", "test", "example"],
        consensus="high",
        sources_count=3,
        path=Path("foundations/new.md"),
    )

    with pytest.raises(FileNotFoundError):
        update_catalog(tmp_path / "nonexistent.md", entry)
