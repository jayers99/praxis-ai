"""Unit tests for domain layer components.

These tests cover core enums, models, and domain logic without file I/O.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from praxis.domain.domains import ARTIFACT_PATHS, Domain
from praxis.domain.models import PraxisConfig, ValidationIssue
from praxis.domain.pipeline import (
    REQUIRED_STAGES,
    AgentOutput,
    PipelineConfig,
    PipelineStage,
    PipelineStageResult,
    PipelineState,
    RiskTier,
    StageExecution,
)
from praxis.domain.pipeline.risk_tiers import get_next_required_stage, is_stage_required
from praxis.domain.privacy import PrivacyLevel
from praxis.domain.stages import ALLOWED_REGRESSIONS, REQUIRES_ARTIFACT, Stage


class TestStageEnum:
    """Tests for Stage enum and comparison operators."""

    def test_stage_ordering(self) -> None:
        """Stages are ordered from capture to close."""
        expected_order = [
            Stage.CAPTURE,
            Stage.SENSE,
            Stage.EXPLORE,
            Stage.SHAPE,
            Stage.FORMALIZE,
            Stage.COMMIT,
            Stage.EXECUTE,
            Stage.SUSTAIN,
            Stage.CLOSE,
        ]
        assert list(Stage) == expected_order

    def test_stage_count(self) -> None:
        """There are exactly 9 stages."""
        assert len(Stage) == 9

    def test_less_than(self) -> None:
        """Earlier stages are less than later stages."""
        assert Stage.CAPTURE < Stage.SENSE
        assert Stage.SENSE < Stage.EXPLORE
        assert Stage.FORMALIZE < Stage.COMMIT
        assert Stage.EXECUTE < Stage.SUSTAIN

    def test_less_than_not_equal(self) -> None:
        """Same stage is not less than itself."""
        assert not (Stage.CAPTURE < Stage.CAPTURE)
        assert not (Stage.EXECUTE < Stage.EXECUTE)

    def test_greater_than(self) -> None:
        """Later stages are greater than earlier stages."""
        assert Stage.CLOSE > Stage.SUSTAIN
        assert Stage.EXECUTE > Stage.COMMIT
        assert Stage.FORMALIZE > Stage.SHAPE

    def test_greater_than_not_equal(self) -> None:
        """Same stage is not greater than itself."""
        assert not (Stage.CLOSE > Stage.CLOSE)

    def test_less_than_or_equal(self) -> None:
        """Less than or equal works correctly."""
        assert Stage.CAPTURE <= Stage.CAPTURE
        assert Stage.CAPTURE <= Stage.SENSE
        assert not (Stage.SENSE <= Stage.CAPTURE)

    def test_greater_than_or_equal(self) -> None:
        """Greater than or equal works correctly."""
        assert Stage.CLOSE >= Stage.CLOSE
        assert Stage.CLOSE >= Stage.SUSTAIN
        assert not (Stage.SUSTAIN >= Stage.CLOSE)

    def test_comparison_with_non_stage_returns_not_implemented(self) -> None:
        """Comparing with non-Stage returns NotImplemented."""
        assert Stage.CAPTURE.__lt__("capture") is NotImplemented
        assert Stage.CAPTURE.__le__("capture") is NotImplemented
        assert Stage.CAPTURE.__gt__("capture") is NotImplemented
        assert Stage.CAPTURE.__ge__("capture") is NotImplemented

    def test_stage_string_values(self) -> None:
        """Stage values are lowercase strings."""
        assert Stage.CAPTURE.value == "capture"
        assert Stage.FORMALIZE.value == "formalize"
        assert Stage.CLOSE.value == "close"


class TestRequiresArtifact:
    """Tests for REQUIRES_ARTIFACT set."""

    def test_commit_and_later_require_artifact(self) -> None:
        """Commit, execute, sustain, close require artifacts."""
        assert Stage.COMMIT in REQUIRES_ARTIFACT
        assert Stage.EXECUTE in REQUIRES_ARTIFACT
        assert Stage.SUSTAIN in REQUIRES_ARTIFACT
        assert Stage.CLOSE in REQUIRES_ARTIFACT

    def test_pre_commit_stages_do_not_require_artifact(self) -> None:
        """Capture through formalize do not require artifacts."""
        assert Stage.CAPTURE not in REQUIRES_ARTIFACT
        assert Stage.SENSE not in REQUIRES_ARTIFACT
        assert Stage.EXPLORE not in REQUIRES_ARTIFACT
        assert Stage.SHAPE not in REQUIRES_ARTIFACT
        assert Stage.FORMALIZE not in REQUIRES_ARTIFACT

    def test_requires_artifact_count(self) -> None:
        """Exactly 4 stages require artifacts."""
        assert len(REQUIRES_ARTIFACT) == 4


class TestAllowedRegressions:
    """Tests for ALLOWED_REGRESSIONS table."""

    def test_execute_can_regress_to_commit_or_formalize(self) -> None:
        """Execute stage can regress to commit or formalize."""
        allowed = ALLOWED_REGRESSIONS[Stage.EXECUTE]
        assert Stage.COMMIT in allowed
        assert Stage.FORMALIZE in allowed
        assert len(allowed) == 2

    def test_sustain_can_regress_to_execute_or_commit(self) -> None:
        """Sustain stage can regress to execute or commit."""
        allowed = ALLOWED_REGRESSIONS[Stage.SUSTAIN]
        assert Stage.EXECUTE in allowed
        assert Stage.COMMIT in allowed
        assert len(allowed) == 2

    def test_close_can_regress_to_capture(self) -> None:
        """Close stage can only regress to capture (new iteration)."""
        allowed = ALLOWED_REGRESSIONS[Stage.CLOSE]
        assert Stage.CAPTURE in allowed
        assert len(allowed) == 1

    def test_early_stages_not_in_regression_table(self) -> None:
        """Early stages have no explicit regression rules."""
        assert Stage.CAPTURE not in ALLOWED_REGRESSIONS
        assert Stage.SENSE not in ALLOWED_REGRESSIONS
        assert Stage.EXPLORE not in ALLOWED_REGRESSIONS
        assert Stage.SHAPE not in ALLOWED_REGRESSIONS
        assert Stage.FORMALIZE not in ALLOWED_REGRESSIONS
        assert Stage.COMMIT not in ALLOWED_REGRESSIONS


class TestPrivacyLevelEnum:
    """Tests for PrivacyLevel enum and comparison operators."""

    def test_privacy_ordering(self) -> None:
        """Privacy levels ordered from least to most restrictive."""
        expected_order = [
            PrivacyLevel.PUBLIC,
            PrivacyLevel.PUBLIC_TRUSTED,
            PrivacyLevel.PERSONAL,
            PrivacyLevel.CONFIDENTIAL,
            PrivacyLevel.RESTRICTED,
        ]
        assert list(PrivacyLevel) == expected_order

    def test_privacy_count(self) -> None:
        """There are exactly 5 privacy levels."""
        assert len(PrivacyLevel) == 5

    def test_less_restrictive_is_less_than(self) -> None:
        """Less restrictive levels are less than more restrictive."""
        assert PrivacyLevel.PUBLIC < PrivacyLevel.PERSONAL
        assert PrivacyLevel.PERSONAL < PrivacyLevel.CONFIDENTIAL
        assert PrivacyLevel.CONFIDENTIAL < PrivacyLevel.RESTRICTED

    def test_more_restrictive_is_greater_than(self) -> None:
        """More restrictive levels are greater than less restrictive."""
        assert PrivacyLevel.RESTRICTED > PrivacyLevel.CONFIDENTIAL
        assert PrivacyLevel.CONFIDENTIAL > PrivacyLevel.PERSONAL

    def test_comparison_with_non_privacy_returns_not_implemented(self) -> None:
        """Comparing with non-PrivacyLevel returns NotImplemented."""
        assert PrivacyLevel.PUBLIC.__lt__("public") is NotImplemented
        assert PrivacyLevel.PUBLIC.__le__("public") is NotImplemented
        assert PrivacyLevel.PUBLIC.__gt__("public") is NotImplemented
        assert PrivacyLevel.PUBLIC.__ge__("public") is NotImplemented


class TestDomainEnum:
    """Tests for Domain enum."""

    def test_all_domains_exist(self) -> None:
        """All 5 domains are defined."""
        assert Domain.CODE.value == "code"
        assert Domain.CREATE.value == "create"
        assert Domain.WRITE.value == "write"
        assert Domain.OBSERVE.value == "observe"
        assert Domain.LEARN.value == "learn"

    def test_domain_count(self) -> None:
        """There are exactly 5 domains."""
        assert len(Domain) == 5


class TestArtifactPaths:
    """Tests for ARTIFACT_PATHS mapping."""

    def test_code_domain_requires_sod(self) -> None:
        """Code domain requires docs/sod.md."""
        assert ARTIFACT_PATHS[Domain.CODE] == Path("docs/sod.md")

    def test_create_domain_requires_brief(self) -> None:
        """Create domain requires docs/brief.md."""
        assert ARTIFACT_PATHS[Domain.CREATE] == Path("docs/brief.md")

    def test_write_domain_requires_brief(self) -> None:
        """Write domain requires docs/brief.md."""
        assert ARTIFACT_PATHS[Domain.WRITE] == Path("docs/brief.md")

    def test_learn_domain_requires_plan(self) -> None:
        """Learn domain requires docs/plan.md."""
        assert ARTIFACT_PATHS[Domain.LEARN] == Path("docs/plan.md")

    def test_observe_domain_has_no_artifact(self) -> None:
        """Observe domain has no required artifact."""
        assert ARTIFACT_PATHS[Domain.OBSERVE] is None

    def test_all_domains_have_mapping(self) -> None:
        """Every domain has an entry in ARTIFACT_PATHS."""
        for domain in Domain:
            assert domain in ARTIFACT_PATHS


class TestPraxisConfig:
    """Tests for PraxisConfig Pydantic model."""

    def test_valid_config(self) -> None:
        """Valid config creates successfully."""
        config = PraxisConfig(
            domain=Domain.CODE,
            stage=Stage.EXECUTE,
            privacy_level=PrivacyLevel.PERSONAL,
            environment="Home",
        )
        assert config.domain == Domain.CODE
        assert config.stage == Stage.EXECUTE
        assert config.privacy_level == PrivacyLevel.PERSONAL
        assert config.environment == "Home"

    def test_default_environment(self) -> None:
        """Environment defaults to Home."""
        config = PraxisConfig(
            domain=Domain.CODE,
            stage=Stage.CAPTURE,
            privacy_level=PrivacyLevel.PUBLIC,
        )
        assert config.environment == "Home"

    def test_work_environment(self) -> None:
        """Work environment is valid."""
        config = PraxisConfig(
            domain=Domain.CODE,
            stage=Stage.CAPTURE,
            privacy_level=PrivacyLevel.CONFIDENTIAL,
            environment="Work",
        )
        assert config.environment == "Work"

    def test_invalid_environment_rejected(self) -> None:
        """Invalid environment raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            PraxisConfig(
                domain=Domain.CODE,
                stage=Stage.CAPTURE,
                privacy_level=PrivacyLevel.PUBLIC,
                environment="InvalidEnv",
            )
        assert "environment" in str(exc_info.value)

    def test_string_coercion_for_enums(self) -> None:
        """String values are coerced to enums."""
        config = PraxisConfig(
            domain="code",
            stage="execute",
            privacy_level="personal",
        )
        assert config.domain == Domain.CODE
        assert config.stage == Stage.EXECUTE
        assert config.privacy_level == PrivacyLevel.PERSONAL

    def test_invalid_domain_rejected(self) -> None:
        """Invalid domain raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            PraxisConfig(
                domain="invalid",
                stage=Stage.CAPTURE,
                privacy_level=PrivacyLevel.PUBLIC,
            )
        assert "domain" in str(exc_info.value)

    def test_invalid_stage_rejected(self) -> None:
        """Invalid stage raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            PraxisConfig(
                domain=Domain.CODE,
                stage="invalid",
                privacy_level=PrivacyLevel.PUBLIC,
            )
        assert "stage" in str(exc_info.value)


class TestValidationIssue:
    """Tests for ValidationIssue model."""

    def test_error_severity(self) -> None:
        """Error severity issue creates successfully."""
        issue = ValidationIssue(
            rule="test_rule",
            severity="error",
            message="Something failed",
        )
        assert issue.rule == "test_rule"
        assert issue.severity == "error"
        assert issue.message == "Something failed"

    def test_warning_severity(self) -> None:
        """Warning severity issue creates successfully."""
        issue = ValidationIssue(
            rule="test_rule",
            severity="warning",
            message="Something is not ideal",
        )
        assert issue.severity == "warning"

    def test_invalid_severity_rejected(self) -> None:
        """Invalid severity raises ValidationError."""
        with pytest.raises(ValidationError):
            ValidationIssue(
                rule="test_rule",
                severity="info",
                message="Not allowed",
            )


# ============================================================================
# Pipeline Domain Tests
# ============================================================================


class TestPipelineStageEnum:
    """Tests for PipelineStage enum and comparison operators."""

    def test_stage_ordering(self) -> None:
        """Pipeline stages are ordered RTC → HVA."""
        expected_order = [
            PipelineStage.RTC,
            PipelineStage.IDAS,
            PipelineStage.SAD,
            PipelineStage.CCR,
            PipelineStage.ASR,
            PipelineStage.HVA,
        ]
        assert list(PipelineStage) == expected_order

    def test_stage_count(self) -> None:
        """There are exactly 6 pipeline stages."""
        assert len(PipelineStage) == 6

    def test_less_than(self) -> None:
        """Earlier stages are less than later stages."""
        assert PipelineStage.RTC < PipelineStage.IDAS
        assert PipelineStage.IDAS < PipelineStage.SAD
        assert PipelineStage.SAD < PipelineStage.CCR
        assert PipelineStage.CCR < PipelineStage.ASR
        assert PipelineStage.ASR < PipelineStage.HVA

    def test_greater_than(self) -> None:
        """Later stages are greater than earlier stages."""
        assert PipelineStage.HVA > PipelineStage.ASR
        assert PipelineStage.ASR > PipelineStage.CCR

    def test_less_than_or_equal(self) -> None:
        """Less than or equal works correctly."""
        assert PipelineStage.RTC <= PipelineStage.RTC
        assert PipelineStage.RTC <= PipelineStage.IDAS

    def test_greater_than_or_equal(self) -> None:
        """Greater than or equal works correctly."""
        assert PipelineStage.HVA >= PipelineStage.HVA
        assert PipelineStage.HVA >= PipelineStage.ASR

    def test_comparison_with_non_stage_returns_not_implemented(self) -> None:
        """Comparing with non-PipelineStage returns NotImplemented."""
        assert PipelineStage.RTC.__lt__("rtc") is NotImplemented
        assert PipelineStage.RTC.__le__("rtc") is NotImplemented
        assert PipelineStage.RTC.__gt__("rtc") is NotImplemented
        assert PipelineStage.RTC.__ge__("rtc") is NotImplemented

    def test_next_stage(self) -> None:
        """next_stage returns the following stage or None."""
        assert PipelineStage.RTC.next_stage() == PipelineStage.IDAS
        assert PipelineStage.ASR.next_stage() == PipelineStage.HVA
        assert PipelineStage.HVA.next_stage() is None

    def test_previous_stage(self) -> None:
        """previous_stage returns the preceding stage or None."""
        assert PipelineStage.IDAS.previous_stage() == PipelineStage.RTC
        assert PipelineStage.HVA.previous_stage() == PipelineStage.ASR
        assert PipelineStage.RTC.previous_stage() is None

    def test_full_name(self) -> None:
        """full_name returns the descriptive name."""
        assert PipelineStage.RTC.full_name == "Raw Thought Capture"
        assert PipelineStage.CCR.full_name == "Critical Challenge Review"
        assert PipelineStage.HVA.full_name == "Human Validation & Acceptance"


class TestRiskTierEnum:
    """Tests for RiskTier enum."""

    def test_tier_ordering(self) -> None:
        """Risk tiers are ordered 0 → 3."""
        assert RiskTier.TIER_0 < RiskTier.TIER_1
        assert RiskTier.TIER_1 < RiskTier.TIER_2
        assert RiskTier.TIER_2 < RiskTier.TIER_3

    def test_tier_count(self) -> None:
        """There are exactly 4 risk tiers."""
        assert len(RiskTier) == 4

    def test_tier_descriptions(self) -> None:
        """Each tier has a description."""
        assert RiskTier.TIER_0.description == "Disposable / Personal Notes"
        assert RiskTier.TIER_3.description == "Foundational / Long-Lived Knowledge"


class TestRequiredStages:
    """Tests for REQUIRED_STAGES mapping."""

    def test_tier_0_requires_rtc_and_idas(self) -> None:
        """Tier 0 requires only RTC and IDAS."""
        required = REQUIRED_STAGES[RiskTier.TIER_0]
        assert required == [PipelineStage.RTC, PipelineStage.IDAS]

    def test_tier_1_skips_ccr(self) -> None:
        """Tier 1 includes SAD but skips CCR."""
        required = REQUIRED_STAGES[RiskTier.TIER_1]
        assert PipelineStage.SAD in required
        assert PipelineStage.CCR not in required
        assert PipelineStage.ASR in required

    def test_tier_2_includes_ccr_but_not_hva(self) -> None:
        """Tier 2 includes CCR but not HVA."""
        required = REQUIRED_STAGES[RiskTier.TIER_2]
        assert PipelineStage.CCR in required
        assert PipelineStage.HVA not in required

    def test_tier_3_requires_all_stages(self) -> None:
        """Tier 3 requires all 6 stages."""
        required = REQUIRED_STAGES[RiskTier.TIER_3]
        assert len(required) == 6
        assert required == list(PipelineStage)

    def test_is_stage_required(self) -> None:
        """is_stage_required correctly checks stage requirements."""
        assert is_stage_required(RiskTier.TIER_0, PipelineStage.RTC)
        assert is_stage_required(RiskTier.TIER_0, PipelineStage.IDAS)
        assert not is_stage_required(RiskTier.TIER_0, PipelineStage.SAD)
        assert not is_stage_required(RiskTier.TIER_1, PipelineStage.CCR)
        assert is_stage_required(RiskTier.TIER_2, PipelineStage.CCR)

    def test_get_next_required_stage(self) -> None:
        """get_next_required_stage returns next required stage."""
        # From None, get first required stage
        assert get_next_required_stage(RiskTier.TIER_0, None) == PipelineStage.RTC
        # After RTC in tier 0, get IDAS
        assert (
            get_next_required_stage(RiskTier.TIER_0, PipelineStage.RTC)
            == PipelineStage.IDAS
        )
        # After IDAS in tier 0, get None (complete)
        assert get_next_required_stage(RiskTier.TIER_0, PipelineStage.IDAS) is None
        # Tier 1 skips CCR: after SAD, get ASR
        assert (
            get_next_required_stage(RiskTier.TIER_1, PipelineStage.SAD)
            == PipelineStage.ASR
        )


class TestPipelineModels:
    """Tests for pipeline Pydantic models."""

    def test_agent_output_model(self) -> None:
        """AgentOutput model creates successfully."""
        output = AgentOutput(
            agent_type="architect",
            output_path=Path("/tmp/output.md"),
            timestamp=datetime(2025, 1, 1, 12, 0, 0),
        )
        assert output.agent_type == "architect"
        assert output.output_path == Path("/tmp/output.md")

    def test_stage_execution_model(self) -> None:
        """StageExecution model creates with defaults."""
        execution = StageExecution(
            stage=PipelineStage.RTC,
            status="pending",
        )
        assert execution.stage == PipelineStage.RTC
        assert execution.status == "pending"
        assert execution.started_at is None
        assert execution.agent_outputs == []

    def test_pipeline_config_model(self) -> None:
        """PipelineConfig model creates successfully."""
        config = PipelineConfig(
            pipeline_id="test-123",
            risk_tier=RiskTier.TIER_2,
            current_stage=PipelineStage.IDAS,
            started_at=datetime(2025, 1, 1, 10, 0, 0),
            source_corpus_path=Path("/tmp/corpus"),
        )
        assert config.pipeline_id == "test-123"
        assert config.risk_tier == RiskTier.TIER_2
        assert config.current_stage == PipelineStage.IDAS

    def test_pipeline_state_model(self) -> None:
        """PipelineState model tracks stage statuses."""
        config = PipelineConfig(
            pipeline_id="test-456",
            risk_tier=RiskTier.TIER_1,
            current_stage=PipelineStage.RTC,
            started_at=datetime(2025, 1, 1, 10, 0, 0),
            source_corpus_path=Path("/tmp/corpus"),
        )
        state = PipelineState(
            config=config,
            stages={
                PipelineStage.RTC: StageExecution(
                    stage=PipelineStage.RTC,
                    status="completed",
                    completed_at=datetime(2025, 1, 1, 10, 5, 0),
                )
            },
        )
        assert state.is_stage_completed(PipelineStage.RTC)
        assert not state.is_stage_completed(PipelineStage.IDAS)
        assert state.get_stage_status(PipelineStage.RTC) == "completed"
        assert state.get_stage_status(PipelineStage.IDAS) == "pending"
        assert state.get_completed_stages() == [PipelineStage.RTC]

    def test_pipeline_stage_result_model(self) -> None:
        """PipelineStageResult model creates successfully."""
        result = PipelineStageResult(
            success=True,
            stage=PipelineStage.RTC,
            output_path=Path("/tmp/output.md"),
            next_stage=PipelineStage.IDAS,
        )
        assert result.success
        assert result.stage == PipelineStage.RTC
        assert result.next_stage == PipelineStage.IDAS
        assert result.errors == []
