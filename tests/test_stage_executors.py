"""Tests for stage executors."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from praxis.application.pipeline import (
    execute_idas,
    execute_rtc,
    execute_sad,
    init_pipeline,
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
    (corpus / "ideas.txt").write_text("Idea 1\nIdea 2\nIdea 3")
    return corpus


@pytest.fixture
def initialized_pipeline(praxis_project: Path, corpus_dir: Path) -> Path:
    """Create an initialized pipeline."""
    init_pipeline(praxis_project, risk_tier=2, source_corpus_path=corpus_dir)
    return praxis_project


class TestExecuteRTC:
    """Tests for execute_rtc function."""

    def test_fails_without_pipeline(self, praxis_project: Path) -> None:
        """Fails when no pipeline exists."""
        result = execute_rtc(praxis_project)
        assert not result.success
        assert "No active pipeline" in result.errors

    def test_copies_corpus_to_run_directory(
        self, initialized_pipeline: Path, corpus_dir: Path
    ) -> None:
        """Copies corpus to pipeline-runs/{id}/rtc-corpus/."""
        state = load_pipeline_state(initialized_pipeline)
        assert state is not None

        result = execute_rtc(initialized_pipeline)
        assert result.success

        rtc_corpus = (
            initialized_pipeline
            / "pipeline-runs"
            / state.config.pipeline_id
            / "rtc-corpus"
        )
        assert rtc_corpus.exists()
        assert (rtc_corpus / "notes.md").exists()
        assert (rtc_corpus / "ideas.txt").exists()

    def test_creates_rtc_output_file(self, initialized_pipeline: Path) -> None:
        """Creates rtc-output.md file."""
        result = execute_rtc(initialized_pipeline)
        assert result.success
        assert result.output_path is not None
        assert result.output_path.exists()
        assert result.output_path.name == "rtc-output.md"

    def test_marks_stage_completed(self, initialized_pipeline: Path) -> None:
        """Marks RTC stage as completed."""
        execute_rtc(initialized_pipeline)

        state = load_pipeline_state(initialized_pipeline)
        assert state is not None
        assert state.is_stage_completed(PipelineStage.RTC)

    def test_returns_next_stage(self, initialized_pipeline: Path) -> None:
        """Returns IDAS as next stage."""
        result = execute_rtc(initialized_pipeline)
        assert result.next_stage == PipelineStage.IDAS

    def test_rtc_output_contains_metadata(self, initialized_pipeline: Path) -> None:
        """RTC output contains pipeline metadata."""
        result = execute_rtc(initialized_pipeline)
        assert result.output_path is not None

        content = result.output_path.read_text()
        assert "Pipeline ID:" in content
        assert "Risk Tier:" in content
        assert "Source Path:" in content


class TestExecuteIDAS:
    """Tests for execute_idas function."""

    def test_fails_without_pipeline(self, praxis_project: Path) -> None:
        """Fails when no pipeline exists."""
        result = execute_idas(praxis_project)
        assert not result.success
        assert "No active pipeline" in result.errors

    def test_fails_without_rtc_completion(self, initialized_pipeline: Path) -> None:
        """Fails when RTC is not completed."""
        result = execute_idas(initialized_pipeline)
        assert not result.success
        assert "RTC stage must be completed" in result.errors[0]

    def test_succeeds_after_rtc(self, initialized_pipeline: Path) -> None:
        """Succeeds after RTC is completed."""
        execute_rtc(initialized_pipeline)
        result = execute_idas(initialized_pipeline)
        assert result.success

    def test_creates_idas_output_file(self, initialized_pipeline: Path) -> None:
        """Creates idas-output.md file."""
        execute_rtc(initialized_pipeline)
        result = execute_idas(initialized_pipeline)

        assert result.output_path is not None
        assert result.output_path.exists()
        assert result.output_path.name == "idas-output.md"

    def test_marks_stage_completed(self, initialized_pipeline: Path) -> None:
        """Marks IDAS stage as completed."""
        execute_rtc(initialized_pipeline)
        execute_idas(initialized_pipeline)

        state = load_pipeline_state(initialized_pipeline)
        assert state is not None
        assert state.is_stage_completed(PipelineStage.IDAS)

    def test_returns_next_stage(self, initialized_pipeline: Path) -> None:
        """Returns SAD as next stage."""
        execute_rtc(initialized_pipeline)
        result = execute_idas(initialized_pipeline)
        assert result.next_stage == PipelineStage.SAD

    def test_idas_output_contains_sections(self, initialized_pipeline: Path) -> None:
        """IDAS output contains expected sections."""
        execute_rtc(initialized_pipeline)
        result = execute_idas(initialized_pipeline)
        assert result.output_path is not None

        content = result.output_path.read_text()
        assert "Dominant Themes" in content
        assert "Identified Gaps" in content
        assert "Research Questions" in content
        assert "Assumptions" in content

    def test_idas_returns_template_warning(self, initialized_pipeline: Path) -> None:
        """IDAS returns warning about template nature."""
        execute_rtc(initialized_pipeline)
        result = execute_idas(initialized_pipeline)
        assert len(result.warnings) > 0
        assert "template" in result.warnings[0].lower()


class TestExecuteSAD:
    """Tests for execute_sad function."""

    def test_fails_without_pipeline(self, praxis_project: Path) -> None:
        """Fails when no pipeline exists."""
        result = execute_sad(praxis_project)
        assert not result.success
        assert "No active pipeline" in result.errors

    def test_fails_without_idas_completion(self, initialized_pipeline: Path) -> None:
        """Fails when IDAS is not completed."""
        execute_rtc(initialized_pipeline)
        result = execute_sad(initialized_pipeline)
        assert not result.success
        assert "IDAS stage must be completed" in result.errors[0]

    def test_succeeds_after_idas(self, initialized_pipeline: Path) -> None:
        """Succeeds after IDAS is completed."""
        execute_rtc(initialized_pipeline)
        execute_idas(initialized_pipeline)
        result = execute_sad(initialized_pipeline)
        assert result.success

    def test_creates_sad_dispatch_file(self, initialized_pipeline: Path) -> None:
        """Creates sad-dispatch.md file."""
        execute_rtc(initialized_pipeline)
        execute_idas(initialized_pipeline)
        result = execute_sad(initialized_pipeline)

        assert result.output_path is not None
        assert result.output_path.exists()
        assert result.output_path.name == "sad-dispatch.md"

    def test_creates_specialist_response_placeholders(
        self, initialized_pipeline: Path
    ) -> None:
        """Creates placeholder files for specialist responses."""
        execute_rtc(initialized_pipeline)
        execute_idas(initialized_pipeline)
        execute_sad(initialized_pipeline)

        state = load_pipeline_state(initialized_pipeline)
        assert state is not None

        sad_responses = (
            initialized_pipeline
            / "pipeline-runs"
            / state.config.pipeline_id
            / "sad-responses"
        )
        assert sad_responses.exists()
        # Code domain should have architect, security, testing, operations
        assert (sad_responses / "architect-response.md").exists()

    def test_marks_stage_completed(self, initialized_pipeline: Path) -> None:
        """Marks SAD stage as completed."""
        execute_rtc(initialized_pipeline)
        execute_idas(initialized_pipeline)
        execute_sad(initialized_pipeline)

        state = load_pipeline_state(initialized_pipeline)
        assert state is not None
        assert state.is_stage_completed(PipelineStage.SAD)

    def test_returns_next_stage(self, initialized_pipeline: Path) -> None:
        """Returns CCR as next stage."""
        execute_rtc(initialized_pipeline)
        execute_idas(initialized_pipeline)
        result = execute_sad(initialized_pipeline)
        assert result.next_stage == PipelineStage.CCR

    def test_accepts_custom_specialists(self, initialized_pipeline: Path) -> None:
        """Accepts custom specialist types."""
        execute_rtc(initialized_pipeline)
        execute_idas(initialized_pipeline)
        result = execute_sad(initialized_pipeline, specialist_types=["researcher"])
        assert result.success

        state = load_pipeline_state(initialized_pipeline)
        assert state is not None

        sad_responses = (
            initialized_pipeline
            / "pipeline-runs"
            / state.config.pipeline_id
            / "sad-responses"
        )
        assert (sad_responses / "researcher-response.md").exists()


class TestSingleFileCorpus:
    """Tests for single-file corpus handling."""

    @pytest.fixture
    def single_file_corpus(self, tmp_path: Path) -> Path:
        """Create a single-file corpus."""
        corpus_file = tmp_path / "research.md"
        corpus_file.write_text("# My Research\n\nContent here.")
        return corpus_file

    def test_handles_single_file_corpus(
        self, praxis_project: Path, single_file_corpus: Path
    ) -> None:
        """Handles single file as corpus."""
        init_pipeline(
            praxis_project, risk_tier=2, source_corpus_path=single_file_corpus
        )
        result = execute_rtc(praxis_project)
        assert result.success

        state = load_pipeline_state(praxis_project)
        assert state is not None

        rtc_corpus = (
            praxis_project
            / "pipeline-runs"
            / state.config.pipeline_id
            / "rtc-corpus"
        )
        assert rtc_corpus.exists()
        assert (rtc_corpus / "research.md").exists()
