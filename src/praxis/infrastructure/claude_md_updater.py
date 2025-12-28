"""Update CLAUDE.md with new stage."""

from __future__ import annotations

import re
from pathlib import Path

from praxis.domain.stages import Stage


def update_claude_md_stage(project_root: Path, new_stage: Stage) -> bool:
    """Update the stage line in CLAUDE.md.

    Looks for patterns like "**Stage:** capture" and updates the stage value.

    Args:
        project_root: Project directory containing CLAUDE.md.
        new_stage: The new stage to set.

    Returns:
        True if updated, False if CLAUDE.md doesn't exist or no match found.
    """
    claude_md = project_root / "CLAUDE.md"
    if not claude_md.exists():
        return False

    content = claude_md.read_text()

    # Replace stage line: "- **Stage:** capture" → "- **Stage:** sense"
    # Also handles without the leading "- " for flexibility
    updated = re.sub(
        r"(\*\*Stage:\*\*\s*)\w+",
        rf"\g<1>{new_stage.value}",
        content,
    )

    if updated == content:
        # No match found
        return False

    claude_md.write_text(updated)
    return True
