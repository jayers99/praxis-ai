"""Tests for pipeline service."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from praxis.application.pipeline.pipeline_service import (
    advance_pipeline_stage,
    get_pipeline_status,
    init_pipeline,
    mark_stage_completed,
    mark_stage_started,
)
from praxis.domain.pipeline import PipelineStage
from praxis.infrastructure.pipeline import load_pipeline_state


@pytest.fixture
def praxis_project(tmp_path: Path) -> Path:
    """Create a valid praxis project."""
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        yaml.dump(
            {
                "domain": "code",
                "stage": "capture",
                "privacy_level": "personal",
                "environment": "Home",
            }
        )
    )
    return tmp_path


@pytest.fixture
def corpus_dir(tmp_path: Path) -> Path:
    """Create a source corpus directory."""
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "notes.md").write_text("# Research Notes\n\nSome content here.")
    return corpus


class TestInitPipeline:
    """Tests for init_pipeline function."""

    def test_requires_praxis_yaml(self, tmp_path: Path, corpus_dir: Path) -> None:
        """Fails without praxis.yaml."""
        result = init_pipeline(tmp_path, risk_tier=2, source_corpus_path=corpus_dir)
        assert not result.success
        assert any("praxis.yaml" in err for err in result.errors)

    def test_validates_risk_tier(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Fails with invalid risk tier."""
        result = init_pipeline(praxis_project, risk_tier=5, source_corpus_path=corpus_dir)
        assert not result.success
        assert any("Invalid risk tier" in err for err in result.errors)

    def test_validates_corpus_exists(self, praxis_project: Path) -> None:
        """Fails when corpus doesn't exist."""
        missing_corpus = Path("/nonexistent/corpus")
        result = init_pipeline(praxis_project, risk_tier=2, source_corpus_path=missing_corpus)
        assert not result.success
        assert any("not found" in err for err in result.errors)

    def test_creates_pipeline_yaml(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Creates pipeline.yaml on success."""
        result = init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        assert result.success
        assert (praxis_project / "pipeline.yaml").exists()

    def test_creates_pipeline_run_directory(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Creates pipeline-runs/{id}/ directory."""
        result = init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        assert result.success
        run_dir = praxis_project / "pipeline-runs" / result.pipeline_id
        assert run_dir.exists()

    def test_returns_required_stages_for_tier(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Returns correct required stages for tier."""
        # Tier 0: RTC, IDAS only
        result = init_pipeline(praxis_project, risk_tier=0, source_corpus_path=corpus_dir)
        assert result.success
        assert result.required_stages == [PipelineStage.RTC, PipelineStage.IDAS]

    def test_prevents_duplicate_pipeline(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Prevents duplicate active pipelines."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        result = init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        assert not result.success
        assert any("Active pipeline exists" in err for err in result.errors)

    def test_force_replaces_existing(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Force flag replaces existing pipeline."""
        first = init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        second = init_pipeline(praxis_project, risk_tier=1, source_corpus_path=corpus_dir, force=True)
        assert second.success
        assert second.pipeline_id != first.pipeline_id

    def test_tier_3_requires_all_stages(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Tier 3 requires all 6 stages."""
        result = init_pipeline(praxis_project, risk_tier=3, source_corpus_path=corpus_dir)
        assert result.success
        assert len(result.required_stages) == 6
        assert PipelineStage.HVA in result.required_stages


class TestGetPipelineStatus:
    """Tests for get_pipeline_status function."""

    def test_returns_error_without_pipeline(self, praxis_project: Path) -> None:
        """Returns error when no pipeline exists."""
        status = get_pipeline_status(praxis_project)
        assert not status.pipeline_id
        assert any("No active pipeline" in err for err in status.errors)

    def test_returns_pipeline_id(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Returns pipeline ID."""
        init_result = init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        status = get_pipeline_status(praxis_project)
        assert status.pipeline_id == init_result.pipeline_id

    def test_returns_stage_progress(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Returns progress for all stages."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        status = get_pipeline_status(praxis_project)
        assert len(status.stage_progress) == 6  # All stages tracked

    def test_shows_required_stages(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Correctly marks required stages."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        status = get_pipeline_status(praxis_project)

        # Find RTC and HVA in progress
        rtc = next(s for s in status.stage_progress if s.stage == PipelineStage.RTC)
        hva = next(s for s in status.stage_progress if s.stage == PipelineStage.HVA)

        assert rtc.required is True  # Tier 2 requires RTC
        assert hva.required is False  # Tier 2 doesn't require HVA

    def test_shows_next_stage(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Shows next stage to execute."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        status = get_pipeline_status(praxis_project)
        assert status.next_stage == PipelineStage.RTC

    def test_not_complete_initially(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Pipeline is not complete initially."""
        init_pipeline(praxis_project, risk_tier=0, source_corpus_path=corpus_dir)
        status = get_pipeline_status(praxis_project)
        assert not status.is_complete


class TestMarkStageStarted:
    """Tests for mark_stage_started function."""

    def test_marks_stage_in_progress(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Marks stage as in_progress."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        success, error = mark_stage_started(praxis_project, PipelineStage.RTC)
        assert success
        assert error is None

        state = load_pipeline_state(praxis_project)
        assert state is not None
        assert state.stages[PipelineStage.RTC].status == "in_progress"
        assert state.stages[PipelineStage.RTC].started_at is not None

    def test_fails_without_pipeline(self, praxis_project: Path) -> None:
        """Fails when no pipeline exists."""
        success, error = mark_stage_started(praxis_project, PipelineStage.RTC)
        assert not success
        assert error == "No active pipeline"


class TestMarkStageCompleted:
    """Tests for mark_stage_completed function."""

    def test_marks_stage_completed(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Marks stage as completed."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        success, error = mark_stage_completed(praxis_project, PipelineStage.RTC)
        assert success
        assert error is None

        state = load_pipeline_state(praxis_project)
        assert state is not None
        assert state.stages[PipelineStage.RTC].status == "completed"
        assert state.stages[PipelineStage.RTC].completed_at is not None

    def test_advances_current_stage(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Advances current stage after completion."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        mark_stage_completed(praxis_project, PipelineStage.RTC)

        state = load_pipeline_state(praxis_project)
        assert state is not None
        assert state.config.current_stage == PipelineStage.IDAS

    def test_stores_output_path(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Stores output path when provided."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        output_path = praxis_project / "output.md"
        mark_stage_completed(praxis_project, PipelineStage.RTC, output_path)

        state = load_pipeline_state(praxis_project)
        assert state is not None
        assert state.stages[PipelineStage.RTC].output_path == output_path


class TestAdvancePipelineStage:
    """Tests for advance_pipeline_stage function."""

    def test_advances_stage(self, praxis_project: Path, corpus_dir: Path) -> None:
        """Advances to specified stage."""
        init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
        success, error = advance_pipeline_stage(praxis_project, PipelineStage.SAD)
        assert success
        assert error is None

        state = load_pipeline_state(praxis_project)
        assert state is not None
        assert state.config.current_stage == PipelineStage.SAD

    def test_fails_without_pipeline(self, praxis_project: Path) -> None:
        """Fails when no pipeline exists."""
        success, error = advance_pipeline_stage(praxis_project, PipelineStage.SAD)
        assert not success
        assert error == "No active pipeline"
