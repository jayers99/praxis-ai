"""Domain model for next steps guidance in praxis status."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Types of actions that can be recommended as next steps."""

    CREATE = "create"  # + Generate new artifact
    EDIT = "edit"  # ~ Modify existing content
    RUN = "run"  # ▶ Execute CLI command
    REVIEW = "review"  # ? Human inspection required
    FIX = "fix"  # ! Address blocking error


# Icon mapping for human-readable output
ACTION_ICONS: dict[ActionType, str] = {
    ActionType.CREATE: "+",
    ActionType.EDIT: "~",
    ActionType.RUN: "▶",
    ActionType.REVIEW: "?",
    ActionType.FIX: "!",
}

# Priority order for sorting: fix > create > edit > run > review
ACTION_PRIORITY_ORDER: dict[ActionType, int] = {
    ActionType.FIX: 1,
    ActionType.CREATE: 2,
    ActionType.EDIT: 3,
    ActionType.RUN: 4,
    ActionType.REVIEW: 5,
}


class NextStep(BaseModel):
    """A single recommended next step."""

    action: ActionType
    priority: int = Field(ge=1, le=3, description="Priority level (1=highest)")
    description: str = Field(description="Human-readable description of the step")
    target: str | None = Field(
        default=None,
        description="File path or target for the action",
    )
    reason: str | None = Field(
        default=None,
        description="Explanation of why this step is needed",
    )
    command: str | None = Field(
        default=None,
        description="CLI command for 'run' actions",
    )

    def format_human(self) -> str:
        """Format step for human-readable output.

        Format: `<icon> <Action> <path> (<reason>)`
        """
        icon = ACTION_ICONS[self.action]
        action_word = self.action.value.capitalize()

        if self.action == ActionType.RUN and self.command:
            return f"{icon} {action_word} `{self.command}` ({self.description})"
        elif self.target:
            return f"{icon} {action_word} {self.target} ({self.description})"
        else:
            return f"{icon} {action_word} ({self.description})"
