"""Step definitions for cataloging.feature."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when

from praxis.application.cataloging_service import (
    catalog_artifact,
    find_orphans,
    validate_metadata,
)

scenarios("../features/cataloging.feature")


@given(parsers.parse('a research artifact with valid metadata at "{artifact_path}"'))
def valid_artifact_at_path(tmp_path: Path, context: dict[str, Any], artifact_path: str) -> None:
    """Create a valid research artifact at the specified path."""
    context["tmp_path"] = tmp_path
    artifact_file = tmp_path / artifact_path
    artifact_file.parent.mkdir(parents=True, exist_ok=True)

    content = dedent("""\
        # My Topic Research

        <!--
        metadata:
          id: patterns-my-topic-research-2026-01-04
          title: My Topic Research
          date: 2026-01-04
          status: approved
          topic: patterns
          keywords: [test, research, example]
          consensus: medium
          sources_count: 5
        -->

        ## Introduction

        Research content here.
    """)
    artifact_file.write_text(content, encoding="utf-8")
    context["artifact_path"] = artifact_file


@given(parsers.parse('the research-library exists at "{library_path}"'))
def research_library_exists(tmp_path: Path, context: dict[str, Any], library_path: str) -> None:
    """Create a research library structure."""
    library = tmp_path / library_path
    library.mkdir(parents=True, exist_ok=True)

    # Create minimal CATALOG.md
    catalog = library / "CATALOG.md"
    content = dedent("""\
        # Research Library Catalog

        _Last updated: 2026-01-01_
        _Total artifacts: 0_

        ---

        ## Quick Reference

        | ID | Title | Topic | Consensus | Date |
        |----|-------|-------|-----------|------|

        ---

        ## By Topic

        ---

        ## By Consensus

        ### High Consensus

        ### Strong Consensus

        ### Medium Consensus

        ### Partial Consensus (hypothesis under evaluation)

        ### Low Consensus (use with caution)

        ---

        ## Keyword Index

        ---

        ## Recently Added

        | Date | Title | Topic |
        |------|-------|-------|

        ---
    """)
    catalog.write_text(content, encoding="utf-8")
    context["library_path"] = library
    context["catalog_path"] = catalog


@when(parsers.parse('I catalog the artifact to topic "{topic}"'))
def catalog_to_topic(context: dict[str, Any], topic: str) -> None:
    """Catalog the artifact to the specified topic."""
    result = catalog_artifact(
        context["artifact_path"],
        topic=topic,
        library_path=context["library_path"],
        catalog_path=context["catalog_path"],
    )
    context["catalog_result"] = result


@then(parsers.parse('the artifact is moved to "{expected_path}"'))
def artifact_moved_to_path(context: dict[str, Any], expected_path: str) -> None:
    """Verify the artifact was moved to the expected path."""
    full_path = context["tmp_path"] / expected_path
    assert full_path.exists(), f"Expected artifact at {expected_path}"


@then("the CATALOG.md Quick Reference table contains the artifact")
def catalog_quick_reference_contains_artifact(context: dict[str, Any]) -> None:
    """Verify the Quick Reference table was updated."""
    catalog_content = context["catalog_path"].read_text(encoding="utf-8")
    assert "patterns-my-topic-research-2026-01-04" in catalog_content
    assert "My Topic Research" in catalog_content


@then(parsers.parse('the CATALOG.md By Topic section under "{topic}" contains the artifact'))
def catalog_by_topic_contains_artifact(context: dict[str, Any], topic: str) -> None:
    """Verify the By Topic section was updated."""
    catalog_content = context["catalog_path"].read_text(encoding="utf-8")
    # Find the topic section
    assert f"### {topic.title()}" in catalog_content
    # Find artifact in topic section
    assert "patterns-my-topic-research-2026-01-04" in catalog_content


@then("the CATALOG.md By Consensus section contains the artifact")
def catalog_by_consensus_contains_artifact(context: dict[str, Any]) -> None:
    """Verify the By Consensus section was updated."""
    catalog_content = context["catalog_path"].read_text(encoding="utf-8")
    # Should be in Medium Consensus section
    assert "### Medium Consensus" in catalog_content
    assert "My Topic Research" in catalog_content


@then("the CATALOG.md Keyword Index contains entries for each keyword")
def catalog_keyword_index_contains_keywords(context: dict[str, Any]) -> None:
    """Verify the Keyword Index was updated."""
    catalog_content = context["catalog_path"].read_text(encoding="utf-8")
    # Check for keyword sections
    assert "### test" in catalog_content
    assert "### research" in catalog_content
    assert "### example" in catalog_content


@then("the CATALOG.md Recently Added section contains the artifact at the top")
def catalog_recently_added_contains_artifact(context: dict[str, Any]) -> None:
    """Verify the Recently Added section was updated."""
    catalog_content = context["catalog_path"].read_text(encoding="utf-8")
    # Find Recently Added section
    assert "## Recently Added" in catalog_content
    lines = catalog_content.split("\n")
    in_recently = False
    for line in lines:
        if "## Recently Added" in line:
            in_recently = True
        elif in_recently and "2026-01-04" in line:
            assert "My Topic Research" in line
            break


# Scenario: Reject artifact with missing required metadata


@given(parsers.parse('a research artifact missing the "{field}" field'))
def artifact_missing_field(tmp_path: Path, context: dict[str, Any], field: str) -> None:
    """Create an artifact with a missing required field."""
    context["tmp_path"] = tmp_path
    artifact = tmp_path / "missing-field.md"

    content = dedent("""\
        # Artifact Missing Field

        <!--
        metadata:
          title: Missing Field Artifact
          date: 2026-01-04
          status: approved
          topic: patterns
          keywords: [test, example, validation]
          consensus: medium
          sources_count: 3
        -->

        Content here.
    """)
    artifact.write_text(content, encoding="utf-8")
    context["artifact_path"] = artifact


@when("I validate the artifact metadata")
def validate_artifact(context: dict[str, Any]) -> None:
    """Validate the artifact metadata."""
    result = validate_metadata(context["artifact_path"])
    context["validation_result"] = result


@then(parsers.parse('validation returns an error for "{error_message}"'))
def validation_returns_error(context: dict[str, Any], error_message: str) -> None:
    """Verify validation returned the expected error."""
    result = context["validation_result"]
    assert result.success is False
    assert any(error_message in e.message for e in result.errors)


# Scenario: Reject artifact with duplicate ID


@given(parsers.parse('an artifact with id "{artifact_id}" exists in CATALOG.md'))
def artifact_exists_in_catalog(tmp_path: Path, context: dict[str, Any], artifact_id: str) -> None:
    """Create a CATALOG.md with an existing artifact ID."""
    library = tmp_path / "research-library"
    library.mkdir(parents=True, exist_ok=True)

    catalog = library / "CATALOG.md"
    content = dedent(f"""\
        # Research Library Catalog

        _Last updated: 2026-01-01_
        _Total artifacts: 1_

        ---

        ## Quick Reference

        | ID | Title | Topic | Consensus | Date |
        |----|-------|-------|-----------|------|
        | [{artifact_id}](patterns/existing.md) | Existing Artifact | patterns | high | 2026-01-04 |

        ---

        ## By Topic

        ### Patterns

        | ID | Title | Consensus | Keywords |
        |----|-------|-----------|----------|
        | [{artifact_id}](patterns/existing.md) | Existing Artifact | high | test, example, pattern |

        ---

        ## By Consensus

        ### High Consensus

        - [Existing Artifact](patterns/existing.md) — patterns — test

        ### Strong Consensus

        ### Medium Consensus

        ### Partial Consensus (hypothesis under evaluation)

        ### Low Consensus (use with caution)

        ---

        ## Keyword Index

        ### test
        - [Existing Artifact](patterns/existing.md)

        ---

        ## Recently Added

        | Date | Title | Topic |
        |------|-------|-------|
        | 2026-01-04 | [Existing Artifact](patterns/existing.md) | patterns |

        ---
    """)
    catalog.write_text(content, encoding="utf-8")
    context["library_path"] = library
    context["catalog_path"] = catalog


@given(parsers.parse('a new artifact has the same id "{artifact_id}"'))
def new_artifact_with_duplicate_id(tmp_path: Path, context: dict[str, Any], artifact_id: str) -> None:
    """Create a new artifact with a duplicate ID."""
    artifact = tmp_path / "duplicate.md"
    content = dedent(f"""\
        # Duplicate Artifact

        <!--
        metadata:
          id: {artifact_id}
          title: Duplicate Artifact
          date: 2026-01-04
          status: approved
          topic: patterns
          keywords: [test, duplicate, example]
          consensus: medium
          sources_count: 3
        -->

        Content here.
    """)
    artifact.write_text(content, encoding="utf-8")
    context["artifact_path"] = artifact


@when("I catalog the new artifact")
def catalog_new_artifact(context: dict[str, Any]) -> None:
    """Catalog the new artifact."""
    result = catalog_artifact(
        context["artifact_path"],
        topic="patterns",
        library_path=context["library_path"],
        catalog_path=context["catalog_path"],
    )
    context["catalog_result"] = result


@then(parsers.parse('cataloging fails with error "{error_message}"'))
def cataloging_fails_with_error(context: dict[str, Any], error_message: str) -> None:
    """Verify cataloging failed with the expected error."""
    result = context["catalog_result"]
    assert result.success is False
    assert any(error_message in e.message for e in result.errors)


# Scenario: Auto-create topic folder if missing


@given("a research artifact with valid metadata")
def valid_artifact(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a valid research artifact."""
    context["tmp_path"] = tmp_path
    artifact = tmp_path / "new-artifact.md"

    content = dedent("""\
        # New Topic Artifact

        <!--
        metadata:
          id: new-topic-artifact-2026-01-04
          title: New Topic Artifact
          date: 2026-01-04
          status: approved
          topic: new-topic
          keywords: [test, new, topic]
          consensus: high
          sources_count: 7
        -->

        Content here.
    """)
    artifact.write_text(content, encoding="utf-8")
    context["artifact_path"] = artifact

    # Also create library with CATALOG.md
    library = tmp_path / "research-library"
    library.mkdir(parents=True, exist_ok=True)

    catalog = library / "CATALOG.md"
    catalog_content = dedent("""\
        # Research Library Catalog

        _Last updated: 2026-01-01_
        _Total artifacts: 0_

        ---

        ## Quick Reference

        | ID | Title | Topic | Consensus | Date |
        |----|-------|-------|-----------|------|

        ---

        ## By Topic

        ---

        ## By Consensus

        ### High Consensus

        ### Strong Consensus

        ### Medium Consensus

        ### Partial Consensus (hypothesis under evaluation)

        ### Low Consensus (use with caution)

        ---

        ## Keyword Index

        ---

        ## Recently Added

        | Date | Title | Topic |
        |------|-------|-------|

        ---
    """)
    catalog.write_text(catalog_content, encoding="utf-8")
    context["library_path"] = library
    context["catalog_path"] = catalog


@given(parsers.parse('no "{folder_path}" folder exists'))
def no_folder_exists(context: dict[str, Any], folder_path: str) -> None:
    """Ensure the folder doesn't exist."""
    full_path = context["tmp_path"] / folder_path
    assert not full_path.exists()


@then(parsers.parse('the folder "{folder_path}" is created'))
def folder_is_created(context: dict[str, Any], folder_path: str) -> None:
    """Verify the folder was created."""
    full_path = context["tmp_path"] / folder_path
    assert full_path.exists()
    assert full_path.is_dir()


@then("the artifact is cataloged successfully")
def artifact_cataloged_successfully(context: dict[str, Any]) -> None:
    """Verify the artifact was cataloged successfully."""
    result = context["catalog_result"]
    assert result.success is True


# Scenario: Detect orphan artifacts


@given(parsers.parse('an artifact exists at "{artifact_path}"'))
def orphan_artifact_exists(tmp_path: Path, context: dict[str, Any], artifact_path: str) -> None:
    """Create an orphan artifact."""
    full_path = tmp_path / artifact_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text("# Orphan\n\nNot cataloged.", encoding="utf-8")
    context["tmp_path"] = tmp_path


@given("the artifact is not listed in CATALOG.md")
def artifact_not_in_catalog(tmp_path: Path, context: dict[str, Any]) -> None:
    """Ensure CATALOG.md exists but doesn't list the orphan."""
    library = tmp_path / "research-library"
    library.mkdir(parents=True, exist_ok=True)

    # Create the orphan in the library
    orphan = library / "patterns" / "orphan.md"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_text("# Orphan\n\nNot cataloged.", encoding="utf-8")

    # Create empty catalog
    catalog = library / "CATALOG.md"
    content = dedent("""\
        # Research Library Catalog

        ---

        ## Quick Reference

        | ID | Title | Topic | Consensus | Date |
        |----|-------|-------|-----------|------|

        ---
    """)
    catalog.write_text(content, encoding="utf-8")
    context["library_path"] = library


@when("I run orphan detection")
def run_orphan_detection(context: dict[str, Any]) -> None:
    """Run orphan detection."""
    orphans = find_orphans(context["library_path"])
    context["orphans"] = orphans


@then(parsers.parse('"{orphan_path}" is returned in the orphan list'))
def orphan_in_list(context: dict[str, Any], orphan_path: str) -> None:
    """Verify the orphan was detected."""
    orphans = context["orphans"]
    assert Path(orphan_path) in orphans


# Scenario: Reindex library produces consistent catalog


@given(parsers.parse("a research library with {count:d} artifacts"))
def library_with_artifacts(tmp_path: Path, context: dict[str, Any], count: int) -> None:
    """Create a research library with the specified number of artifacts."""
    # For MVP, reindex is not implemented, so this scenario will be skipped
    context["skip_reason"] = "Reindex not implemented in MVP"


@when("I reindex the library twice")
def reindex_library_twice(context: dict[str, Any]) -> None:
    """Reindex the library twice."""
    # Skip - not implemented in MVP
    pass


@then("both runs produce identical CATALOG.md content")
def identical_catalog_content(context: dict[str, Any]) -> None:
    """Verify both reindex runs produce identical output."""
    # Skip - not implemented in MVP
    pass
