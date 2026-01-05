"""Step definitions for pipeline_precheck.feature."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, scenarios, then, when

from praxis.application.pipeline.pipeline_service import init_pipeline
from praxis.infrastructure.librarian import search_library

scenarios("../features/pipeline_precheck.feature")


@given("I am in a temporary directory")
def setup_temp_dir(tmp_path: Path, context: dict[str, Any], request: pytest.FixtureRequest) -> None:
    """Set up temporary directory with cleanup."""
    context["project_root"] = tmp_path
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    # Ensure we restore the original directory even if test fails
    def restore_cwd() -> None:
        os.chdir(original_dir)

    request.addfinalizer(restore_cwd)


@given("I have a valid praxis.yaml")
def create_praxis_yaml(context: dict[str, Any]) -> None:
    """Create a valid praxis.yaml file."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given('the research library contains artifacts with keyword "roles"')
def create_research_library_with_roles(context: dict[str, Any]) -> None:
    """Create a research library with role-related artifacts."""
    project_root = context["project_root"]
    research_lib = project_root / "research-library"
    research_lib.mkdir(exist_ok=True)

    catalog_md = research_lib / "CATALOG.md"
    catalog_md.write_text(
        """# Research Library Catalog

_Last updated: 2026-01-03_
_Total artifacts: 2_

---

## Quick Reference

| ID | Title | Topic | Consensus | Date |
|----|-------|-------|-----------|------|
| [roles-rationale-2025-12-28](roles/rationale.md) | Rationale for Praxis Roles Architecture | roles | High | 2025-12-28 |
| [roles-scrum-master-2026-01-02](roles/scrum-master-role.md) | Scrum Master Role in Scrum Teams | roles | High | 2026-01-02 |

---

## By Topic

### Roles

| ID | Title | Consensus | Keywords |
|----|-------|-----------|----------|
| [roles-rationale-2025-12-28](roles/rationale.md) | Rationale for Praxis Roles Architecture | High | praxis-roles, accountability, decision-rights, scrum |
| [roles-scrum-master-2026-01-02](roles/scrum-master-role.md) | Scrum Master Role in Scrum Teams | High | scrum-master, servant-leadership, facilitation, coaching, self-management |
"""
    )

    context["catalog_path"] = catalog_md


@given('the research library contains no artifacts matching "quantum-computing"')
def create_research_library_without_quantum(context: dict[str, Any]) -> None:
    """Create a research library without quantum computing artifacts."""
    project_root = context["project_root"]
    research_lib = project_root / "research-library"
    research_lib.mkdir(exist_ok=True)

    catalog_md = research_lib / "CATALOG.md"
    catalog_md.write_text(
        """# Research Library Catalog

_Last updated: 2026-01-03_
_Total artifacts: 1_

---

## Quick Reference

| ID | Title | Topic | Consensus | Date |
|----|-------|-------|-----------|------|
| [foundations-classical-roots-2025-12-28](foundations/classical-roots.md) | Classical Roots of Praxis-AI | foundations | High | 2025-12-28 |

---

## By Topic

### Foundations

| ID | Title | Consensus | Keywords |
|----|-------|-----------|----------|
| [foundations-classical-roots-2025-12-28](foundations/classical-roots.md) | Classical Roots of Praxis-AI | High | philosophy, aristotle, plato, socrates, praxis, phronesis |
"""
    )

    context["catalog_path"] = catalog_md


@given("the research library contains matching artifacts")
def create_research_library_with_matches(context: dict[str, Any]) -> None:
    """Create a research library with some artifacts."""
    # Reuse the roles library creation
    create_research_library_with_roles(context)


@given('a completed research run exists for topic "ai-guards"')
def create_prior_run(context: dict[str, Any]) -> None:
    """Create a prior pipeline run for ai-guards."""
    project_root = context["project_root"]
    corpus_path = project_root / "corpus" / "ai-guards-input.md"
    corpus_path.parent.mkdir(exist_ok=True)
    corpus_path.write_text("AI guards research input")

    # Initialize a pipeline
    result = init_pipeline(
        project_root=project_root,
        risk_tier=1,
        source_corpus_path=corpus_path,
        run_precheck=False,  # Disable precheck for the prior run
    )

    context["prior_run_id"] = result.pipeline_id


@given("the research library catalog exists")
def catalog_exists(context: dict[str, Any]) -> None:
    """Ensure catalog exists with some content."""
    create_research_library_with_matches(context)


@given("the research library catalog is empty")
def create_empty_catalog(context: dict[str, Any]) -> None:
    """Create an empty catalog."""
    project_root = context["project_root"]
    research_lib = project_root / "research-library"
    research_lib.mkdir(exist_ok=True)

    catalog_md = research_lib / "CATALOG.md"
    catalog_md.write_text(
        """# Research Library Catalog

_Last updated: 2026-01-03_
_Total artifacts: 0_

---

## Quick Reference

| ID | Title | Topic | Consensus | Date |
|----|-------|-------|-----------|------|
"""
    )

    context["catalog_path"] = catalog_md


@when('a new research run is initiated with topic "scrum roles"')
def init_pipeline_with_topic(context: dict[str, Any]) -> None:
    """Initialize a pipeline with scrum roles topic."""
    project_root = context["project_root"]
    corpus_path = project_root / "corpus" / "scrum-roles.md"
    corpus_path.parent.mkdir(exist_ok=True)
    corpus_path.write_text("Research on scrum roles")

    result = init_pipeline(
        project_root=project_root,
        risk_tier=1,
        source_corpus_path=corpus_path,
        run_precheck=True,
    )

    context["init_result"] = result


@when('a new research run is initiated with topic "quantum computing"')
def init_pipeline_with_quantum_topic(context: dict[str, Any]) -> None:
    """Initialize a pipeline with quantum computing topic."""
    project_root = context["project_root"]
    corpus_path = project_root / "corpus" / "quantum-computing.md"
    corpus_path.parent.mkdir(exist_ok=True)
    corpus_path.write_text("Research on quantum computing")

    result = init_pipeline(
        project_root=project_root,
        risk_tier=1,
        source_corpus_path=corpus_path,
        run_precheck=True,
    )

    context["init_result"] = result


@when("a precheck is performed")
def perform_precheck(context: dict[str, Any]) -> None:
    """Perform a precheck."""
    project_root = context["project_root"]
    corpus_path = project_root / "corpus" / "test-topic.md"
    corpus_path.parent.mkdir(exist_ok=True)
    corpus_path.write_text("Test topic research")

    result = init_pipeline(
        project_root=project_root,
        risk_tier=1,
        source_corpus_path=corpus_path,
        run_precheck=True,
    )

    context["init_result"] = result


@when("a rerun is initiated with changed assumptions")
def init_rerun(context: dict[str, Any]) -> None:
    """Initialize a rerun with changed assumptions."""
    project_root = context["project_root"]
    prior_run_id = context["prior_run_id"]
    corpus_path = project_root / "corpus" / "ai-guards-rerun.md"
    corpus_path.parent.mkdir(exist_ok=True)
    corpus_path.write_text("AI guards research - revised assumptions")

    result = init_pipeline(
        project_root=project_root,
        risk_tier=1,
        source_corpus_path=corpus_path,
        run_precheck=True,
        prior_run_id=prior_run_id,
        rerun_reason="Changed assumptions about AI memory lifecycle",
        force=True,  # Replace the prior run
    )

    context["rerun_result"] = result


@when('the librarian is queried with "knowledge distillation"')
def query_librarian_knowledge(context: dict[str, Any]) -> None:
    """Query the librarian for knowledge distillation."""
    catalog_path = context.get("catalog_path")
    if catalog_path:
        matches = search_library(
            query="knowledge distillation",
            catalog_path=catalog_path,
        )
        context["librarian_matches"] = matches


@when("the librarian is queried with any topic")
def query_librarian_any_topic(context: dict[str, Any]) -> None:
    """Query the librarian with any topic."""
    catalog_path = context.get("catalog_path")
    if catalog_path:
        matches = search_library(
            query="test topic",
            catalog_path=catalog_path,
        )
        context["librarian_matches"] = matches


@then("the precheck returns a list of matching artifacts")
def verify_precheck_has_matches(context: dict[str, Any]) -> None:
    """Verify precheck returned matching artifacts."""
    result = context["init_result"]
    assert result.success, "Pipeline init should succeed"
    assert len(result.precheck_matches) > 0, "Should have precheck matches"


@then("each artifact includes path, date, and title")
def verify_artifact_metadata(context: dict[str, Any]) -> None:
    """Verify each artifact has required metadata."""
    result = context["init_result"]
    for match in result.precheck_matches:
        assert "path" in match, "Match should have path"
        assert "date" in match, "Match should have date"
        assert "title" in match, "Match should have title"
        assert "id" in match, "Match should have id"
        assert "relevance_score" in match, "Match should have relevance score"


@then('the precheck returns "No relevant prior artifacts found"')
def verify_no_precheck_matches(context: dict[str, Any]) -> None:
    """Verify precheck returned no matches."""
    result = context["init_result"]
    assert result.success, "Pipeline init should succeed"
    assert len(result.precheck_matches) == 0, "Should have no precheck matches"


@then("the output includes structured metadata (path, date, title, keywords)")
def verify_structured_metadata(context: dict[str, Any]) -> None:
    """Verify output has structured metadata."""
    result = context["init_result"]
    if result.precheck_matches:
        match = result.precheck_matches[0]
        assert "path" in match
        assert "date" in match
        assert "title" in match
        assert "keywords" in match


@then("the rerun metadata includes a reference to the prior run")
def verify_prior_run_reference(context: dict[str, Any]) -> None:
    """Verify rerun references the prior run."""
    context["rerun_result"]
    # Check that we can load the pipeline state and find prior_run_id
    from praxis.infrastructure.pipeline.pipeline_state_repo import load_pipeline_state

    project_root = context["project_root"]
    state = load_pipeline_state(project_root)

    assert state is not None
    assert state.config.prior_run_id is not None
    assert state.config.prior_run_id == context["prior_run_id"]


@then("the changed assumptions are recorded")
def verify_rerun_reason(context: dict[str, Any]) -> None:
    """Verify rerun reason is recorded."""
    from praxis.infrastructure.pipeline.pipeline_state_repo import load_pipeline_state

    project_root = context["project_root"]
    state = load_pipeline_state(project_root)

    assert state is not None
    assert state.config.rerun_reason is not None
    assert "assumptions" in state.config.rerun_reason.lower()


@then("it returns artifacts ranked by relevance")
def verify_librarian_ranked_results(context: dict[str, Any]) -> None:
    """Verify librarian returns ranked results."""
    matches = context.get("librarian_matches", [])
    # Check that matches are sorted by relevance (if multiple)
    if len(matches) > 1:
        scores = [m.relevance_score for m in matches]
        assert scores == sorted(scores, reverse=True), "Matches should be sorted by relevance"


@then("it returns an empty list without error")
def verify_librarian_empty_result(context: dict[str, Any]) -> None:
    """Verify librarian returns empty list for empty catalog."""
    matches = context.get("librarian_matches", [])
    assert matches == [], "Should return empty list for empty catalog"
