"""Stage execution logic for pipeline stages."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from praxis.domain.pipeline.models import PipelineStageResult, PipelineState
from praxis.domain.pipeline.stages import PipelineStage
from praxis.infrastructure.pipeline.pipeline_state_repo import (
    get_stage_output_path,
    load_pipeline_state,
    save_pipeline_state,
)


def execute_rtc(project_root: Path) -> PipelineStageResult:
    """
    Execute Raw Thought Capture stage.

    1. Validate source corpus exists at config.source_corpus_path
    2. Copy/link corpus to pipeline-runs/{id}/rtc-corpus/
    3. Create rtc-output.md with metadata header
    4. Update stage status to completed

    Args:
        project_root: Project directory.

    Returns:
        PipelineStageResult with execution outcome.
    """
    state = load_pipeline_state(project_root)
    if state is None:
        return PipelineStageResult(
            success=False,
            stage=PipelineStage.RTC,
            errors=["No active pipeline"],
        )

    config = state.config
    corpus_path = config.source_corpus_path

    # Validate corpus exists
    if not corpus_path.exists():
        return PipelineStageResult(
            success=False,
            stage=PipelineStage.RTC,
            errors=[f"Source corpus not found: {corpus_path}"],
        )

    # Mark stage as started
    _mark_stage_started(state, PipelineStage.RTC)
    save_pipeline_state(project_root, state)

    # Create RTC corpus directory in pipeline run
    run_dir = project_root / "pipeline-runs" / config.pipeline_id
    rtc_corpus_dir = run_dir / "rtc-corpus"

    # Copy corpus to pipeline run directory
    if corpus_path.is_dir():
        if rtc_corpus_dir.exists():
            shutil.rmtree(rtc_corpus_dir)
        shutil.copytree(corpus_path, rtc_corpus_dir)
    else:
        rtc_corpus_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(corpus_path, rtc_corpus_dir / corpus_path.name)

    # Create rtc-output.md with metadata
    output_path = get_stage_output_path(
        project_root, config.pipeline_id, PipelineStage.RTC
    )
    output_content = _generate_rtc_output(config, corpus_path, rtc_corpus_dir)
    output_path.write_text(output_content)

    # Mark stage as completed
    _mark_stage_completed(state, PipelineStage.RTC, output_path)
    save_pipeline_state(project_root, state)

    return PipelineStageResult(
        success=True,
        stage=PipelineStage.RTC,
        output_path=output_path,
        next_stage=PipelineStage.IDAS,
    )


def execute_idas(project_root: Path) -> PipelineStageResult:
    """
    Execute Inquiry-Driven Analytical Synthesis stage.

    1. Validate RTC completed
    2. Load RTC corpus
    3. Generate IDAS research brief template
    4. Write idas-output.md

    Args:
        project_root: Project directory.

    Returns:
        PipelineStageResult with execution outcome.
    """
    state = load_pipeline_state(project_root)
    if state is None:
        return PipelineStageResult(
            success=False,
            stage=PipelineStage.IDAS,
            errors=["No active pipeline"],
        )

    # Validate RTC is completed
    if not state.is_stage_completed(PipelineStage.RTC):
        return PipelineStageResult(
            success=False,
            stage=PipelineStage.IDAS,
            errors=["RTC stage must be completed before IDAS"],
        )

    config = state.config

    # Mark stage as started
    _mark_stage_started(state, PipelineStage.IDAS)
    save_pipeline_state(project_root, state)

    # Generate IDAS output
    run_dir = project_root / "pipeline-runs" / config.pipeline_id
    rtc_corpus_dir = run_dir / "rtc-corpus"
    output_path = get_stage_output_path(
        project_root, config.pipeline_id, PipelineStage.IDAS
    )

    output_content = _generate_idas_output(config, rtc_corpus_dir)
    output_path.write_text(output_content)

    # Mark stage as completed
    _mark_stage_completed(state, PipelineStage.IDAS, output_path)
    save_pipeline_state(project_root, state)

    return PipelineStageResult(
        success=True,
        stage=PipelineStage.IDAS,
        output_path=output_path,
        next_stage=PipelineStage.SAD,
        warnings=["IDAS output is a template. Please review and refine."],
    )


def _mark_stage_started(state: PipelineState, stage: PipelineStage) -> None:
    """Mark a stage as in_progress in the state."""
    from praxis.domain.pipeline.models import StageExecution

    if stage in state.stages:
        state.stages[stage].status = "in_progress"
        state.stages[stage].started_at = datetime.now()
    else:
        state.stages[stage] = StageExecution(
            stage=stage,
            status="in_progress",
            started_at=datetime.now(),
        )
    state.config.current_stage = stage


def _mark_stage_completed(
    state: PipelineState,
    stage: PipelineStage,
    output_path: Path | None,
) -> None:
    """Mark a stage as completed in the state."""
    from praxis.domain.pipeline.models import StageExecution

    if stage in state.stages:
        state.stages[stage].status = "completed"
        state.stages[stage].completed_at = datetime.now()
        state.stages[stage].output_path = output_path
    else:
        state.stages[stage] = StageExecution(
            stage=stage,
            status="completed",
            completed_at=datetime.now(),
            output_path=output_path,
        )

    # Advance current stage
    next_stage = stage.next_stage()
    if next_stage:
        state.config.current_stage = next_stage


def _generate_rtc_output(
    config: object,
    source_path: Path,
    corpus_dir: Path,
) -> str:
    """Generate RTC output markdown with metadata."""
    from praxis.domain.pipeline.models import PipelineConfig

    if not isinstance(config, PipelineConfig):
        raise TypeError("config must be a PipelineConfig")

    # List files in corpus
    if corpus_dir.is_dir():
        files = list(corpus_dir.rglob("*"))
        file_list = "\n".join(
            f"- {f.relative_to(corpus_dir)}" for f in files if f.is_file()
        )
    else:
        file_list = f"- {corpus_dir.name}"

    return f"""# Raw Thought Capture (RTC)

## Metadata

- **Pipeline ID:** {config.pipeline_id}
- **Risk Tier:** {config.risk_tier.value} ({config.risk_tier.description})
- **Started:** {config.started_at.isoformat()}
- **Source Path:** {source_path}
- **Captured At:** {datetime.now().isoformat()}

## Corpus Contents

{file_list}

## Notes

This stage preserves unstructured thought without judgment or loss.
The corpus has been copied to `rtc-corpus/` for analysis in subsequent stages.

---

*Stage completed. Proceed to IDAS (Inquiry-Driven Analytical Synthesis).*
"""


def _generate_idas_output(
    config: object,
    corpus_dir: Path,
) -> str:
    """Generate IDAS output markdown template."""
    from praxis.domain.pipeline.models import PipelineConfig

    if not isinstance(config, PipelineConfig):
        raise TypeError("config must be a PipelineConfig")

    return f"""# Inquiry-Driven Analytical Synthesis (IDAS)

## Metadata

- **Pipeline ID:** {config.pipeline_id}
- **Risk Tier:** {config.risk_tier.value} ({config.risk_tier.description})
- **Corpus Location:** {corpus_dir}
- **Analyzed At:** {datetime.now().isoformat()}

## Dominant Themes

<!-- Rank themes by relevance to the research goal -->

1. **Theme 1:** [Description]
   - Evidence: [Reference to corpus content]
   - Relevance: [Why this matters]

2. **Theme 2:** [Description]
   - Evidence: [Reference to corpus content]
   - Relevance: [Why this matters]

3. **Theme 3:** [Description]
   - Evidence: [Reference to corpus content]
   - Relevance: [Why this matters]

## Identified Gaps and Unknowns

<!-- What's missing or unclear? -->

- [ ] Gap 1: [What we don't know]
- [ ] Gap 2: [Missing information]
- [ ] Unknown 1: [Uncertainty to resolve]

## Well-Formed Research Questions

<!-- Questions suitable for specialist investigation -->

1. **Primary Question:** [Main research question]
2. **Secondary Question:** [Supporting question]
3. **Exploratory Question:** [Open-ended inquiry]

## Surfaced Assumptions and Constraints

### Assumptions Made

- Assumption 1: [What we're taking for granted]
- Assumption 2: [Implicit belief]

### Constraints Identified

- Constraint 1: [Limitation on the research]
- Constraint 2: [Boundary condition]

---

## Next Steps

1. Review and refine the themes above
2. Validate research questions with stakeholders
3. Proceed to SAD (Specialist Agent Dispatch)

*This is a template. Edit to reflect your actual analysis.*
"""
