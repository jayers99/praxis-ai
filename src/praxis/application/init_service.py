"""Initialize a new Praxis project."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from praxis.domain.domains import Domain
from praxis.domain.models import InitResult
from praxis.domain.privacy import PrivacyLevel
from praxis.domain.subtypes import SubtypeValidationError, validate_subtype_for_domain
from praxis.infrastructure.file_writer import check_files_exist, write_file
from praxis.infrastructure.templates import render_capture_md, render_claude_md


def init_project(
    path: Path,
    domain: str,
    privacy: str,
    environment: str,
    *,
    subtype: str | None = None,
    force: bool = False,
) -> InitResult:
    """Initialize a Praxis project.

    Args:
        path: Project directory.
        domain: Project domain (code, create, write, observe, learn).
        subtype: Optional subtype (e.g., cli, api, library).
        privacy: Privacy level (public, personal, confidential, restricted).
        environment: Environment (Home, Work).
        force: If True, overwrite existing files.

    Returns:
        InitResult with success status and created files.
    """
    errors: list[str] = []
    created_files: list[str] = []

    # Validate domain
    try:
        domain_enum = Domain(domain)
    except ValueError:
        valid_domains = ", ".join(d.value for d in Domain)
        errors.append(f"Invalid domain: '{domain}'. Valid options: {valid_domains}")
        return InitResult(success=False, errors=errors)

    # Validate privacy
    try:
        privacy_enum = PrivacyLevel(privacy)
    except ValueError:
        valid_privacy = ", ".join(p.value for p in PrivacyLevel)
        errors.append(
            f"Invalid privacy level: '{privacy}'. Valid options: {valid_privacy}"
        )
        return InitResult(success=False, errors=errors)

    # Validate environment
    if environment not in ("Home", "Work"):
        errors.append(
            f"Invalid environment: '{environment}'. Valid options: Home, Work"
        )
        return InitResult(success=False, errors=errors)

    # Validate subtype against domain (if provided)
    if subtype is not None:
        try:
            validate_subtype_for_domain(subtype, domain_enum)
        except SubtypeValidationError as e:
            errors.append(str(e))
            return InitResult(success=False, errors=errors)

    # Resolve paths
    project_root = path.resolve()
    praxis_yaml_path = project_root / "praxis.yaml"
    claude_md_path = project_root / "CLAUDE.md"
    capture_md_path = project_root / "docs" / "capture.md"

    # Check for existing files
    files_to_create = [praxis_yaml_path, claude_md_path, capture_md_path]
    existing_files = check_files_exist(files_to_create)

    if existing_files and not force:
        for f in existing_files:
            errors.append(f"File exists: {f.relative_to(project_root)}")
        errors.append("Use --force to overwrite existing files.")
        return InitResult(success=False, errors=errors)

    # Generate praxis.yaml content
    praxis_config = {
        "domain": domain_enum.value,
        **({"subtype": subtype} if subtype else {}),
        "stage": "capture",
        "privacy_level": privacy_enum.value,
        "environment": environment,
    }
    praxis_yaml_content = yaml.dump(
        praxis_config, default_flow_style=False, sort_keys=False
    )

    # Generate CLAUDE.md content
    project_name = project_root.name
    claude_md_content = render_claude_md(
        project_name=project_name,
        domain=domain_enum.value,
        privacy=privacy_enum.value,
    )

    # Generate capture.md content
    today = date.today().isoformat()
    capture_md_content = render_capture_md(date=today)

    # Write files
    success, err = write_file(praxis_yaml_path, praxis_yaml_content, force)
    if success:
        created_files.append("praxis.yaml")
    else:
        errors.append(err or "Unknown error writing praxis.yaml")

    success, err = write_file(claude_md_path, claude_md_content, force)
    if success:
        created_files.append("CLAUDE.md")
    else:
        errors.append(err or "Unknown error writing CLAUDE.md")

    success, err = write_file(capture_md_path, capture_md_content, force)
    if success:
        created_files.append("docs/capture.md")
    else:
        errors.append(err or "Unknown error writing docs/capture.md")

    return InitResult(
        success=len(errors) == 0,
        files_created=created_files,
        errors=errors,
    )
