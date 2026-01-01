"""CCR Orchestrator for multi-agent critical challenge review."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from praxis.domain.pipeline.models import (
    AgentOutput,
    PipelineStageResult,
)
from praxis.domain.pipeline.risk_tiers import RiskTier
from praxis.domain.pipeline.stages import PipelineStage
from praxis.infrastructure.pipeline.pipeline_state_repo import (
    get_ccr_critique_path,
    get_stage_output_path,
    load_pipeline_state,
    save_pipeline_state,
)

# Challenger types for CCR
CHALLENGER_TYPES = [
    "architect",
    "security",
    "operations",
    "devil_advocate",
]

# Challengers by risk tier (higher tiers get more challengers)
CHALLENGERS_BY_TIER: dict[RiskTier, list[str]] = {
    RiskTier.TIER_0: [],  # No CCR for tier 0
    RiskTier.TIER_1: [],  # No CCR for tier 1
    RiskTier.TIER_2: ["architect", "security"],
    RiskTier.TIER_3: ["architect", "security", "operations", "devil_advocate"],
}


class CCROrchestrator:
    """
    Coordinates multi-agent critical challenge review.

    Each challenger agent independently critiques specialist outputs
    without seeing other challengers' critiques (prevents groupthink).
    """

    def __init__(self, project_root: Path):
        """Initialize the orchestrator.

        Args:
            project_root: Project directory.
        """
        self.project_root = project_root

    def execute(
        self,
        challenger_types: list[str] | None = None,
    ) -> PipelineStageResult:
        """
        Execute CCR stage.

        1. Validate SAD completed with outputs
        2. Load specialist outputs
        3. Determine challenger agents
        4. Generate critique templates for each challenger
        5. Create consolidated critique summary

        Args:
            challenger_types: Optional override for challenger types.

        Returns:
            PipelineStageResult with execution outcome.
        """
        state = load_pipeline_state(self.project_root)
        if state is None:
            return PipelineStageResult(
                success=False,
                stage=PipelineStage.CCR,
                errors=["No active pipeline"],
            )

        # Validate SAD is completed
        if not state.is_stage_completed(PipelineStage.SAD):
            return PipelineStageResult(
                success=False,
                stage=PipelineStage.CCR,
                errors=["SAD stage must be completed before CCR"],
            )

        config = state.config
        tier = config.risk_tier

        # Mark stage as started
        self._mark_stage_started(state)
        save_pipeline_state(self.project_root, state)

        # Determine challengers
        if challenger_types:
            challengers = challenger_types
        else:
            challengers = self.get_challengers_for_tier(tier)

        if not challengers:
            return PipelineStageResult(
                success=False,
                stage=PipelineStage.CCR,
                errors=[f"CCR not required for tier {tier.value}. Skip to ASR."],
            )

        # Get SAD outputs
        run_dir = self.project_root / "pipeline-runs" / config.pipeline_id
        sad_responses_dir = run_dir / "sad-responses"

        sad_outputs: list[Path] = []
        if sad_responses_dir.exists():
            sad_outputs = list(sad_responses_dir.glob("*.md"))

        # Generate CCR critique templates
        ccr_critiques_dir = run_dir / "ccr-critiques"
        ccr_critiques_dir.mkdir(exist_ok=True)

        agent_outputs: list[AgentOutput] = []
        for challenger in challengers:
            critique_path = get_ccr_critique_path(
                self.project_root, config.pipeline_id, challenger
            )
            critique_content = self._generate_critique_template(
                config, challenger, sad_outputs
            )
            critique_path.write_text(critique_content)
            agent_outputs.append(
                AgentOutput(
                    agent_type=challenger,
                    output_path=critique_path,
                    timestamp=datetime.now(),
                )
            )

        # Generate consolidated CCR output
        output_path = get_stage_output_path(
            self.project_root, config.pipeline_id, PipelineStage.CCR
        )
        consolidated_content = self._generate_consolidated_output(
            config, challengers, sad_outputs
        )
        output_path.write_text(consolidated_content)

        # Mark stage as completed with agent outputs
        self._mark_stage_completed(state, output_path, agent_outputs)
        save_pipeline_state(self.project_root, state)

        return PipelineStageResult(
            success=True,
            stage=PipelineStage.CCR,
            output_path=output_path,
            next_stage=PipelineStage.ASR,
            warnings=[
                f"Created {len(challengers)} challenger critique templates. "
                "Review ccr-critiques/ for each challenger's analysis."
            ],
        )

    def get_challengers_for_tier(self, tier: RiskTier) -> list[str]:
        """Get challenger types for the given risk tier."""
        return CHALLENGERS_BY_TIER.get(tier, [])

    def _mark_stage_started(self, state: object) -> None:
        """Mark CCR stage as started."""
        from praxis.domain.pipeline.models import PipelineState, StageExecution

        if not isinstance(state, PipelineState):
            return

        if PipelineStage.CCR in state.stages:
            state.stages[PipelineStage.CCR].status = "in_progress"
            state.stages[PipelineStage.CCR].started_at = datetime.now()
        else:
            state.stages[PipelineStage.CCR] = StageExecution(
                stage=PipelineStage.CCR,
                status="in_progress",
                started_at=datetime.now(),
            )
        state.config.current_stage = PipelineStage.CCR

    def _mark_stage_completed(
        self,
        state: object,
        output_path: Path,
        agent_outputs: list[AgentOutput],
    ) -> None:
        """Mark CCR stage as completed."""
        from praxis.domain.pipeline.models import PipelineState, StageExecution

        if not isinstance(state, PipelineState):
            return

        if PipelineStage.CCR in state.stages:
            state.stages[PipelineStage.CCR].status = "completed"
            state.stages[PipelineStage.CCR].completed_at = datetime.now()
            state.stages[PipelineStage.CCR].output_path = output_path
            state.stages[PipelineStage.CCR].agent_outputs = agent_outputs
        else:
            state.stages[PipelineStage.CCR] = StageExecution(
                stage=PipelineStage.CCR,
                status="completed",
                completed_at=datetime.now(),
                output_path=output_path,
                agent_outputs=agent_outputs,
            )
        state.config.current_stage = PipelineStage.ASR

    def _generate_critique_template(
        self,
        config: object,
        challenger: str,
        sad_outputs: list[Path],
    ) -> str:
        """Generate a critique template for a challenger."""
        from praxis.domain.pipeline.models import PipelineConfig

        if not isinstance(config, PipelineConfig):
            raise TypeError("config must be a PipelineConfig")

        sad_files = "\n".join(f"- {p.name}" for p in sad_outputs)

        return f"""# {challenger.replace('_', ' ').title()} Critique

## Metadata

- **Pipeline ID:** {config.pipeline_id}
- **Challenger Type:** {challenger}
- **Created At:** {datetime.now().isoformat()}

## Specialist Outputs to Review

{sad_files}

## Your Task

As a {challenger.replace('_', ' ')} challenger, critically review the specialist
outputs and challenge their conclusions.

## Challenged Assumptions

<!-- What assumptions did the specialists make that should be questioned? -->

1. Assumption: [What was taken for granted]
   - Challenge: [Why this is problematic]
   - Evidence: [What supports your challenge]

## Identified Risks

<!-- What risks or concerns did the specialists overlook? -->

1. Risk: [Overlooked concern]
   - Severity: [High/Medium/Low]
   - Mitigation: [Suggested approach]

## Alternative Interpretations

<!-- Are there other ways to read the data? -->

1. Alternative: [Different interpretation]
   - Support: [Evidence for this view]

## Recommendations

<!-- How can the analysis be strengthened? -->

1. Recommendation: [Actionable suggestion]

---

*Be constructive, not destructive. Provide evidence for challenges.*
"""

    def _generate_consolidated_output(
        self,
        config: object,
        challengers: list[str],
        sad_outputs: list[Path],
    ) -> str:
        """Generate consolidated CCR output."""
        from praxis.domain.pipeline.models import PipelineConfig

        if not isinstance(config, PipelineConfig):
            raise TypeError("config must be a PipelineConfig")

        challenger_list = ", ".join(challengers)
        sad_files = "\n".join(f"- {p.name}" for p in sad_outputs)

        return f"""# Critical Challenge Review (CCR) — Consolidated

## Metadata

- **Pipeline ID:** {config.pipeline_id}
- **Risk Tier:** {config.risk_tier.value} ({config.risk_tier.description})
- **Challengers:** {challenger_list}
- **Reviewed At:** {datetime.now().isoformat()}

## Specialist Outputs Reviewed

{sad_files}

## Challenger Critiques

Each challenger has independently reviewed the specialist outputs.
See `ccr-critiques/` for individual critiques.

### Summary of Challenges

<!-- Aggregate the challenges from all challengers -->

| Category | Challenge | Challenger | Severity |
|----------|-----------|------------|----------|
| Assumptions | [TBD] | [TBD] | [TBD] |
| Risks | [TBD] | [TBD] | [TBD] |
| Gaps | [TBD] | [TBD] | [TBD] |

### Risk/Weakness Matrix

| Area | Identified Issues | Recommended Actions |
|------|-------------------|---------------------|
| Architecture | [TBD] | [TBD] |
| Security | [TBD] | [TBD] |
| Operations | [TBD] | [TBD] |

## Recommendations for ASR

Based on the critical challenges, the ASR stage should address:

1. [Key issue to resolve]
2. [Conflicting viewpoints to arbitrate]
3. [Open questions to answer]

---

## Next Steps

1. Review all challenger critiques in `ccr-critiques/`
2. Update this consolidated summary
3. Proceed to ASR (Adjudicated Synthesis & Resolution)

*Challengers worked independently to prevent groupthink.*
"""


def execute_ccr(
    project_root: Path,
    challenger_types: list[str] | None = None,
) -> PipelineStageResult:
    """
    Execute Critical Challenge Review stage.

    Convenience function that creates a CCROrchestrator and executes.

    Args:
        project_root: Project directory.
        challenger_types: Optional override for challenger types.

    Returns:
        PipelineStageResult with execution outcome.
    """
    orchestrator = CCROrchestrator(project_root)
    return orchestrator.execute(challenger_types)
