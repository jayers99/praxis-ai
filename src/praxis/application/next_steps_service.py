"""Service for generating next step recommendations based on project state."""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from praxis.domain.domains import ARTIFACT_PATHS, Domain
from praxis.domain.models import PraxisConfig, ValidationResult
from praxis.domain.next_steps import (
    ACTION_PRIORITY_ORDER,
    ActionType,
    NextStep,
)
from praxis.domain.stages import Stage

# Maximum number of next steps to show
MAX_NEXT_STEPS = 3


class StepGuidance(TypedDict, total=False):
    """Type definition for stage guidance entries."""

    action: ActionType
    description: str
    target: str | None
    reason: str | None
    command: str | None
    artifact: bool  # Mark as domain artifact


def _artifact_exists(project_root: Path, domain: Domain) -> bool:
    """Check if the domain artifact exists."""
    artifact_path = ARTIFACT_PATHS.get(domain)
    if artifact_path is None:
        return True  # Observe domain has no required artifact
    return (project_root / artifact_path).exists()


def _get_artifact_path(domain: Domain) -> str | None:
    """Get the artifact path for a domain."""
    path = ARTIFACT_PATHS.get(domain)
    return str(path) if path else None


def _get_artifact_description(domain: Domain) -> str:
    """Get human-readable description for domain artifact."""
    descriptions = {
        Domain.CODE: "Solution Overview Document",
        Domain.CREATE: "Creative Brief",
        Domain.WRITE: "Writing Brief",
        Domain.LEARN: "Learning Plan",
    }
    return descriptions.get(domain, "Formalize artifact")


# Stage-specific next steps by domain
# Mapping: (domain, stage) -> list of potential next steps
# Steps are generated conditionally based on project state
STAGE_GUIDANCE: dict[tuple[Domain, Stage], list[StepGuidance]] = {
    # Code domain - Capture through Formalize
    (Domain.CODE, Stage.CAPTURE): [
        {
            "action": ActionType.CREATE,
            "description": "Capture document",
            "target": "docs/capture.md",
            "reason": "Record initial ideas, requirements, or problem statement",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Sense stage",
            "command": "praxis stage sense",
            "reason": "Ready when raw inputs are captured",
        },
    ],
    (Domain.CODE, Stage.SENSE): [
        {
            "action": ActionType.EDIT,
            "description": "Organize and tag captured inputs",
            "target": "docs/capture.md",
            "reason": "Add context and structure to raw notes",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Explore stage",
            "command": "praxis stage explore",
            "reason": "Ready when inputs have meaning and problem is articulated",
        },
    ],
    (Domain.CODE, Stage.EXPLORE): [
        {
            "action": ActionType.CREATE,
            "description": "Document exploration options",
            "target": "docs/exploration.md",
            "reason": "Capture 2-3 possible directions",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Shape stage",
            "command": "praxis stage shape",
            "reason": "Ready when multiple viable directions exist",
        },
    ],
    (Domain.CODE, Stage.SHAPE): [
        {
            "action": ActionType.EDIT,
            "description": "Refine selected direction",
            "target": "docs/exploration.md",
            "reason": "Converge on single approach with rough scope",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Formalize stage",
            "command": "praxis stage formalize",
            "reason": "Ready when direction chosen and major tradeoffs resolved",
        },
    ],
    (Domain.CODE, Stage.FORMALIZE): [
        {
            "action": ActionType.CREATE,
            "description": "Solution Overview Document",
            "target": "docs/sod.md",
            "reason": "Lock intent, scope, constraints, and success criteria",
            "artifact": True,  # Mark as domain artifact
        },
        {
            "action": ActionType.REVIEW,
            "description": "Review SOD completeness",
            "target": "docs/sod.md",
            "reason": "Ensure all sections are complete before commit",
        },
        {
            "action": ActionType.RUN,
            "description": "Validate configuration",
            "command": "praxis validate",
            "reason": "Check project is ready to advance",
        },
    ],
    # Write domain - Capture through Formalize
    (Domain.WRITE, Stage.CAPTURE): [
        {
            "action": ActionType.CREATE,
            "description": "Capture document",
            "target": "docs/capture.md",
            "reason": "Record initial thesis, audience notes, or topic ideas",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Sense stage",
            "command": "praxis stage sense",
            "reason": "Ready when raw inputs are captured",
        },
    ],
    (Domain.WRITE, Stage.SENSE): [
        {
            "action": ActionType.EDIT,
            "description": "Organize and tag captured inputs",
            "target": "docs/capture.md",
            "reason": "Add structure and identify patterns",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Explore stage",
            "command": "praxis stage explore",
            "reason": "Ready when argument can be articulated",
        },
    ],
    (Domain.WRITE, Stage.EXPLORE): [
        {
            "action": ActionType.CREATE,
            "description": "Document exploration options",
            "target": "docs/exploration.md",
            "reason": "Outline 2-3 possible angles or structures",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Shape stage",
            "command": "praxis stage shape",
            "reason": "Ready when multiple directions exist",
        },
    ],
    (Domain.WRITE, Stage.SHAPE): [
        {
            "action": ActionType.EDIT,
            "description": "Refine selected direction",
            "target": "docs/exploration.md",
            "reason": "Converge on thesis and structure",
        },
        {
            "action": ActionType.RUN,
            "description": "Advance to Formalize stage",
            "command": "praxis stage formalize",
            "reason": "Ready when thesis and audience are clear",
        },
    ],
    (Domain.WRITE, Stage.FORMALIZE): [
        {
            "action": ActionType.CREATE,
            "description": "Writing Brief",
            "target": "docs/brief.md",
            "reason": "Fix thesis, audience, and scope before drafting",
            "artifact": True,  # Mark as domain artifact
        },
        {
            "action": ActionType.REVIEW,
            "description": "Review brief completeness",
            "target": "docs/brief.md",
            "reason": "Ensure all sections are complete before commit",
        },
        {
            "action": ActionType.RUN,
            "description": "Validate configuration",
            "command": "praxis validate",
            "reason": "Check project is ready to advance",
        },
    ],
}


def _get_fix_steps(validation: ValidationResult) -> list[NextStep]:
    """Generate fix steps from validation errors."""
    fix_steps = []
    for issue in validation.errors:
        fix_steps.append(
            NextStep(
                action=ActionType.FIX,
                priority=1,  # Fix errors are highest priority
                description=issue.message,
                target="praxis.yaml",
                reason=f"Validation error: {issue.rule}",
            )
        )
    return fix_steps


def _sort_steps(steps: list[NextStep]) -> list[NextStep]:
    """Sort steps by priority order: fix > create > edit > run > review."""
    return sorted(
        steps,
        key=lambda s: (s.priority, ACTION_PRIORITY_ORDER.get(s.action, 99)),
    )


def get_next_steps(
    config: PraxisConfig | None,
    validation: ValidationResult,
    project_root: Path,
) -> list[NextStep]:
    """Generate next step recommendations based on project state.

    Args:
        config: The parsed praxis.yaml configuration (None if invalid).
        validation: Validation result for the project.
        project_root: Path to the project root directory.

    Returns:
        List of 1-3 NextStep recommendations, sorted by priority.
    """
    steps: list[NextStep] = []

    # If config is invalid, show fix steps
    if config is None:
        fix_steps = _get_fix_steps(validation)
        if fix_steps:
            return fix_steps[:MAX_NEXT_STEPS]
        # Fallback if no specific errors
        return [
            NextStep(
                action=ActionType.FIX,
                priority=1,
                description="Fix praxis.yaml configuration",
                target="praxis.yaml",
                reason="Configuration is invalid",
            )
        ]

    # Check for validation errors first (highest priority)
    fix_steps = _get_fix_steps(validation)
    steps.extend(fix_steps)

    # Get stage-specific guidance
    domain = config.domain
    stage = config.stage

    # Only provide guidance for supported domains and stages
    # MVP: Code and Write domains, Capture through Formalize
    guidance_key = (domain, stage)
    stage_guidance = STAGE_GUIDANCE.get(guidance_key, [])

    for guidance in stage_guidance:
        target = guidance.get("target")
        is_artifact = guidance.get("artifact", False)

        # For artifact steps, check if it already exists
        if is_artifact:
            if _artifact_exists(project_root, domain):
                # Artifact exists - suggest edit instead of create
                steps.append(
                    NextStep(
                        action=ActionType.EDIT,
                        priority=2,
                        description=guidance["description"],
                        target=target,
                        reason="Complete and review before advancing",
                    )
                )
            else:
                # Artifact missing - suggest create
                steps.append(
                    NextStep(
                        action=ActionType.CREATE,
                        priority=1,
                        description=guidance["description"],
                        target=target,
                        reason=guidance.get("reason"),
                    )
                )
        elif guidance["action"] == ActionType.CREATE:
            # For non-artifact create steps, check if file exists
            if target and (project_root / target).exists():
                # File exists - suggest edit instead
                steps.append(
                    NextStep(
                        action=ActionType.EDIT,
                        priority=2,
                        description=guidance["description"],
                        target=target,
                        reason=guidance.get("reason"),
                    )
                )
            else:
                steps.append(
                    NextStep(
                        action=ActionType.CREATE,
                        priority=2,
                        description=guidance["description"],
                        target=target,
                        reason=guidance.get("reason"),
                    )
                )
        else:
            # Other actions (run, review, edit)
            steps.append(
                NextStep(
                    action=guidance["action"],
                    priority=2 if guidance["action"] != ActionType.RUN else 3,
                    description=guidance["description"],
                    target=target,
                    reason=guidance.get("reason"),
                    command=guidance.get("command"),
                )
            )

    # Sort by priority and action type
    sorted_steps = _sort_steps(steps)

    # Limit to MAX_NEXT_STEPS
    return sorted_steps[:MAX_NEXT_STEPS]


def format_next_steps_human(steps: list[NextStep]) -> str:
    """Format next steps for human-readable output.

    Returns:
        Formatted string with next steps and legend.
    """
    if not steps:
        return "Next Steps:\n  ✓ Ready to advance (no blockers)"

    lines = ["Next Steps:"]
    for step in steps:
        lines.append(f"  {step.format_human()}")

    # Add legend
    lines.append("")
    lines.append("Legend: + create  ~ edit  ▶ run  ? review  ! fix")

    return "\n".join(lines)
