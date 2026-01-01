"""Tests for pipeline state repository."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from praxis.domain.pipeline import (
    PipelineConfig,
    PipelineStage,
    PipelineState,
    RiskTier,
    StageExecution,
)
from praxis.infrastructure.pipeline import (
    create_pipeline_run_directory,
    get_stage_output_path,
    load_pipeline_state,
    save_pipeline_state,
)
from praxis.infrastructure.pipeline.pipeline_state_repo import (
    get_ccr_critique_path,
    get_sad_response_path,
)


@pytest.fixture
def sample_pipeline_state() -> PipelineState:
    """Create a sample pipeline state for testing."""
    config = PipelineConfig(
        pipeline_id="test-pipeline-123",
        risk_tier=RiskTier.TIER_2,
        current_stage=PipelineStage.IDAS,
        started_at=datetime(2025, 1, 1, 10, 0, 0),
        source_corpus_path=Path("/tmp/corpus"),
    )
    return PipelineState(
        config=config,
        stages={
            PipelineStage.RTC: StageExecution(
                stage=PipelineStage.RTC,
                status="completed",
                started_at=datetime(2025, 1, 1, 10, 0, 0),
                completed_at=datetime(2025, 1, 1, 10, 5, 0),
                output_path=Path("pipeline-runs/test-pipeline-123/rtc-output.md"),
            ),
            PipelineStage.IDAS: StageExecution(
                stage=PipelineStage.IDAS,
                status="in_progress",
                started_at=datetime(2025, 1, 1, 10, 10, 0),
            ),
        },
    )


class TestLoadPipelineState:
    """Tests for load_pipeline_state function."""

    def test_returns_none_for_missing_file(self, tmp_path: Path) -> None:
        """Returns None when pipeline.yaml doesn't exist."""
        result = load_pipeline_state(tmp_path)
        assert result is None

    def test_returns_none_for_invalid_yaml(self, tmp_path: Path) -> None:
        """Returns None for malformed YAML."""
        yaml_path = tmp_path / "pipeline.yaml"
        yaml_path.write_text("invalid: yaml: content: [")
        result = load_pipeline_state(tmp_path)
        assert result is None

    def test_returns_none_for_empty_file(self, tmp_path: Path) -> None:
        """Returns None for empty file."""
        yaml_path = tmp_path / "pipeline.yaml"
        yaml_path.write_text("")
        result = load_pipeline_state(tmp_path)
        assert result is None

    def test_loads_valid_pipeline_state(
        self,
        tmp_path: Path,
        sample_pipeline_state: PipelineState,
    ) -> None:
        """Successfully loads valid pipeline state."""
        save_pipeline_state(tmp_path, sample_pipeline_state)
        result = load_pipeline_state(tmp_path)

        assert result is not None
        assert result.config.pipeline_id == "test-pipeline-123"
        assert result.config.risk_tier == RiskTier.TIER_2
        assert result.config.current_stage == PipelineStage.IDAS
        assert result.is_stage_completed(PipelineStage.RTC)
        assert result.get_stage_status(PipelineStage.IDAS) == "in_progress"


class TestSavePipelineState:
    """Tests for save_pipeline_state function."""

    def test_creates_pipeline_yaml(
        self,
        tmp_path: Path,
        sample_pipeline_state: PipelineState,
    ) -> None:
        """Creates pipeline.yaml file."""
        save_pipeline_state(tmp_path, sample_pipeline_state)
        assert (tmp_path / "pipeline.yaml").exists()

    def test_creates_backup_on_overwrite(
        self,
        tmp_path: Path,
        sample_pipeline_state: PipelineState,
    ) -> None:
        """Creates backup when overwriting existing file."""
        # Save initial state
        save_pipeline_state(tmp_path, sample_pipeline_state)

        # Modify and save again
        sample_pipeline_state.config.current_stage = PipelineStage.SAD
        save_pipeline_state(tmp_path, sample_pipeline_state)

        assert (tmp_path / "pipeline.yaml.backup").exists()

    def test_roundtrip_preserves_data(
        self,
        tmp_path: Path,
        sample_pipeline_state: PipelineState,
    ) -> None:
        """Save and load preserves all data."""
        save_pipeline_state(tmp_path, sample_pipeline_state)
        loaded = load_pipeline_state(tmp_path)

        assert loaded is not None
        assert loaded.config.pipeline_id == sample_pipeline_state.config.pipeline_id
        assert loaded.config.risk_tier == sample_pipeline_state.config.risk_tier
        assert loaded.config.started_at == sample_pipeline_state.config.started_at
        assert loaded.config.source_corpus_path == Path("/tmp/corpus")


class TestCreatePipelineRunDirectory:
    """Tests for create_pipeline_run_directory function."""

    def test_creates_run_directory(self, tmp_path: Path) -> None:
        """Creates the pipeline-runs/{id}/ directory."""
        run_dir = create_pipeline_run_directory(tmp_path, "my-pipeline")
        assert run_dir.exists()
        assert run_dir == tmp_path / "pipeline-runs" / "my-pipeline"

    def test_creates_ccr_critiques_subdirectory(self, tmp_path: Path) -> None:
        """Creates ccr-critiques subdirectory."""
        run_dir = create_pipeline_run_directory(tmp_path, "my-pipeline")
        assert (run_dir / "ccr-critiques").exists()

    def test_creates_sad_responses_subdirectory(self, tmp_path: Path) -> None:
        """Creates sad-responses subdirectory."""
        run_dir = create_pipeline_run_directory(tmp_path, "my-pipeline")
        assert (run_dir / "sad-responses").exists()

    def test_idempotent_creation(self, tmp_path: Path) -> None:
        """Multiple calls don't fail."""
        create_pipeline_run_directory(tmp_path, "my-pipeline")
        run_dir = create_pipeline_run_directory(tmp_path, "my-pipeline")
        assert run_dir.exists()


class TestGetStageOutputPath:
    """Tests for get_stage_output_path function."""

    def test_rtc_output_path(self, tmp_path: Path) -> None:
        """RTC stage has correct output path."""
        path = get_stage_output_path(tmp_path, "my-pipeline", PipelineStage.RTC)
        assert path == tmp_path / "pipeline-runs" / "my-pipeline" / "rtc-output.md"

    def test_idas_output_path(self, tmp_path: Path) -> None:
        """IDAS stage has correct output path."""
        path = get_stage_output_path(tmp_path, "my-pipeline", PipelineStage.IDAS)
        assert path == tmp_path / "pipeline-runs" / "my-pipeline" / "idas-output.md"

    def test_sad_output_path(self, tmp_path: Path) -> None:
        """SAD stage has correct output path."""
        path = get_stage_output_path(tmp_path, "my-pipeline", PipelineStage.SAD)
        assert path == tmp_path / "pipeline-runs" / "my-pipeline" / "sad-dispatch.md"

    def test_ccr_output_path(self, tmp_path: Path) -> None:
        """CCR stage has correct output path."""
        path = get_stage_output_path(tmp_path, "my-pipeline", PipelineStage.CCR)
        expected = tmp_path / "pipeline-runs" / "my-pipeline" / "ccr-consolidated.md"
        assert path == expected

    def test_asr_output_path(self, tmp_path: Path) -> None:
        """ASR stage has correct output path."""
        path = get_stage_output_path(tmp_path, "my-pipeline", PipelineStage.ASR)
        assert path == tmp_path / "pipeline-runs" / "my-pipeline" / "asr-synthesis.md"

    def test_hva_output_path(self, tmp_path: Path) -> None:
        """HVA stage has correct output path."""
        path = get_stage_output_path(tmp_path, "my-pipeline", PipelineStage.HVA)
        assert path == tmp_path / "pipeline-runs" / "my-pipeline" / "hva-decision.md"


class TestCCRCritiquePath:
    """Tests for get_ccr_critique_path function."""

    def test_architect_critique_path(self, tmp_path: Path) -> None:
        """Architect critique has correct path."""
        path = get_ccr_critique_path(tmp_path, "my-pipeline", "architect")
        expected = (
            tmp_path
            / "pipeline-runs"
            / "my-pipeline"
            / "ccr-critiques"
            / "architect-critique.md"
        )
        assert path == expected

    def test_security_critique_path(self, tmp_path: Path) -> None:
        """Security critique has correct path."""
        path = get_ccr_critique_path(tmp_path, "my-pipeline", "security")
        expected = (
            tmp_path
            / "pipeline-runs"
            / "my-pipeline"
            / "ccr-critiques"
            / "security-critique.md"
        )
        assert path == expected


class TestSADResponsePath:
    """Tests for get_sad_response_path function."""

    def test_specialist_response_path(self, tmp_path: Path) -> None:
        """Specialist response has correct path."""
        path = get_sad_response_path(tmp_path, "my-pipeline", "researcher")
        expected = (
            tmp_path
            / "pipeline-runs"
            / "my-pipeline"
            / "sad-responses"
            / "researcher-response.md"
        )
        assert path == expected
