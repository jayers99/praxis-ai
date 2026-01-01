"""Stage execution logic for pipeline stages."""

from __future__ import annotations

import shutil
from collections.abc import Sequence
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


def execute_sad(
    project_root: Path,
    specialist_types: list[str] | None = None,
) -> PipelineStageResult:
    """
    Execute Specialist Agent Dispatch stage.

    1. Validate IDAS completed
    2. Load IDAS research brief
    3. Determine required specialists
    4. Generate dispatch packets for each specialist
    5. Write sad-dispatch.md

    Args:
        project_root: Project directory.
        specialist_types: Optional override for specialist types.

    Returns:
        PipelineStageResult with execution outcome.
    """
    from praxis.domain.pipeline.specialists import (
        DOMAIN_SPECIALISTS,
        SpecialistType,
        get_specialists_for_domain,
    )
    from praxis.infrastructure.yaml_loader import load_praxis_config

    state = load_pipeline_state(project_root)
    if state is None:
        return PipelineStageResult(
            success=False,
            stage=PipelineStage.SAD,
            errors=["No active pipeline"],
        )

    # Validate IDAS is completed
    if not state.is_stage_completed(PipelineStage.IDAS):
        return PipelineStageResult(
            success=False,
            stage=PipelineStage.SAD,
            errors=["IDAS stage must be completed before SAD"],
        )

    config = state.config

    # Mark stage as started
    _mark_stage_started(state, PipelineStage.SAD)
    save_pipeline_state(project_root, state)

    # Determine specialists
    if specialist_types:
        try:
            specialists = [SpecialistType(s) for s in specialist_types]
        except ValueError as e:
            return PipelineStageResult(
                success=False,
                stage=PipelineStage.SAD,
                errors=[f"Invalid specialist type: {e}"],
            )
    else:
        # Get domain from praxis.yaml
        praxis_result = load_praxis_config(project_root)
        if praxis_result.valid and praxis_result.config:
            domain = praxis_result.config.domain
            specialists = get_specialists_for_domain(domain)
        else:
            specialists = list(DOMAIN_SPECIALISTS.values())[0]

    # Generate SAD output
    run_dir = project_root / "pipeline-runs" / config.pipeline_id
    idas_output = get_stage_output_path(
        project_root, config.pipeline_id, PipelineStage.IDAS
    )
    output_path = get_stage_output_path(
        project_root, config.pipeline_id, PipelineStage.SAD
    )

    output_content = _generate_sad_output(config, idas_output, specialists)
    output_path.write_text(output_content)

    # Create placeholder files for specialist responses
    sad_responses_dir = run_dir / "sad-responses"
    sad_responses_dir.mkdir(exist_ok=True)
    for spec in specialists:
        response_path = sad_responses_dir / f"{spec.value}-response.md"
        if not response_path.exists():
            response_path.write_text(
                f"# {spec.value.title()} Specialist Response\n\n"
                "*Awaiting specialist analysis...*\n"
            )

    # Mark stage as completed
    _mark_stage_completed(state, PipelineStage.SAD, output_path)
    save_pipeline_state(project_root, state)

    return PipelineStageResult(
        success=True,
        stage=PipelineStage.SAD,
        output_path=output_path,
        next_stage=PipelineStage.CCR,
        warnings=[
            f"Dispatched to {len(specialists)} specialists. "
            "Review sad-responses/ for each specialist's analysis."
        ],
    )


def _generate_sad_output(
    config: object,
    idas_output: Path,
    specialists: Sequence[object],
) -> str:
    """Generate SAD dispatch markdown."""
    from praxis.domain.pipeline.models import PipelineConfig
    from praxis.domain.pipeline.specialists import SpecialistType

    if not isinstance(config, PipelineConfig):
        raise TypeError("config must be a PipelineConfig")

    specialist_sections = []
    for spec in specialists:
        if not isinstance(spec, SpecialistType):
            continue
        specialist_sections.append(f"""### {spec.value.title()} Specialist

**Focus:** {spec.description}

**Inquiry Packet:**

1. Review the IDAS analysis at `{idas_output.name}`
2. Apply your specialty lens to the research questions
3. Identify domain-specific risks and opportunities
4. Provide actionable recommendations

**Expected Deliverables:**

- Key observations from your perspective
- Risks and concerns within your domain
- Specific recommendations
- Open questions for clarification

**Output Location:** `sad-responses/{spec.value}-response.md`
""")

    specialists_md = "\n".join(specialist_sections)
    specialist_list = ", ".join(
        s.value for s in specialists if isinstance(s, SpecialistType)
    )

    return f"""# Specialist Agent Dispatch (SAD)

## Metadata

- **Pipeline ID:** {config.pipeline_id}
- **Risk Tier:** {config.risk_tier.value} ({config.risk_tier.description})
- **IDAS Source:** {idas_output}
- **Dispatched At:** {datetime.now().isoformat()}

## Dispatch Summary

**Selected Specialists:** {specialist_list}

This stage delegates bounded inquiry to appropriate specialist agents.
Each specialist reviews the IDAS analysis from their domain perspective.

---

## Specialist Dispatch Packets

{specialists_md}

---

## Next Steps

1. Each specialist completes their analysis in `sad-responses/`
2. Review all specialist outputs for completeness
3. Proceed to CCR (Critical Challenge Review)

*Specialists work independently to prevent groupthink.*
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
