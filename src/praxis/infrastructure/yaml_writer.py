"""Update praxis.yaml fields."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def update_praxis_yaml(
    project_root: Path, **updates: Any
) -> tuple[bool, str | None]:
    """Update specific fields in praxis.yaml while preserving structure.

    Args:
        project_root: Project directory containing praxis.yaml.
        **updates: Field names and values to update.

    Returns:
        Tuple of (success, error_message). error_message is None on success.
    """
    yaml_path = project_root / "praxis.yaml"

    if not yaml_path.exists():
        return False, f"praxis.yaml not found at {project_root}"

    try:
        content = yaml.safe_load(yaml_path.read_text())

        # Apply updates
        for key, value in updates.items():
            if hasattr(value, "value"):  # Enum
                content[key] = value.value
            elif isinstance(value, list):
                # Handle list of items (potentially Pydantic models)
                content[key] = [
                    item.model_dump(mode="python", exclude_none=True)
                    if hasattr(item, "model_dump")
                    else item
                    for item in value
                ]
            elif hasattr(value, "model_dump"):  # Pydantic model
                content[key] = value.model_dump(mode="python", exclude_none=True)
            else:
                content[key] = value

        # Write back
        yaml_path.write_text(
            yaml.safe_dump(content, default_flow_style=False, sort_keys=False)
        )
        return True, None
    except Exception as e:
        return False, f"Failed to update praxis.yaml: {e}"
