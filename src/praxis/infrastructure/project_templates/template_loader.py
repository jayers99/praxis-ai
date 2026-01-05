"""Load and apply project templates."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def get_template(template_name: str) -> Any | None:
    """Get a project template by name.

    Args:
        template_name: Name of the template (e.g., 'python-cli').

    Returns:
        ProjectTemplate if found, None otherwise.
    """
    if template_name == "python-cli":
        from praxis.infrastructure.project_templates.python_cli import (
            get_python_cli_template,
        )

        return get_python_cli_template()
    return None


def apply_template(
    project_root: Path,
    template: Any,
    project_name: str,
    force: bool = False,
) -> tuple[list[str], list[str]]:
    """Apply a project template to a directory.

    Args:
        project_root: Root directory for the project.
        template: Template to apply.
        project_name: Name of the project (used for substitutions).
        force: If True, overwrite existing files.

    Returns:
        Tuple of (created_files, errors).
    """
    from praxis.infrastructure.file_writer import write_file
    from praxis.infrastructure.slug_helpers import slugify

    created_files: list[str] = []
    errors: list[str] = []

    # Generate slug for package name
    package_name = slugify(project_name).replace("-", "_")

    for template_file in template.files:
        # Substitute placeholders in path and content
        file_path_str = template_file.path.replace("{package_name}", package_name)
        file_content = template_file.content.replace("{package_name}", package_name)
        file_content = file_content.replace("{project_name}", project_name)

        file_path = project_root / file_path_str

        success, err = write_file(file_path, file_content, force)
        if success:
            created_files.append(file_path_str)
        else:
            errors.append(err or f"Failed to write {file_path_str}")

    return created_files, errors
