"""Domain creation service - guided journey for defining new domains."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import questionary
import yaml

from praxis.domain.domain_spec import (
    AIConstraint,
    DomainCreationResult,
    DomainMenuOption,
    DomainSpecification,
)


# Predefined domain templates for opinionated menu
DOMAIN_MENU_OPTIONS: list[DomainMenuOption] = [
    DomainMenuOption(
        key="research",
        name="research",
        display_name="Research",
        description="Academic and exploratory investigation",
        formalize_artifact_name="Research Brief",
        formalize_artifact_path="docs/research-brief.md",
        default_privacy="personal",
        ai_permissions={
            "suggest": "allowed",
            "complete": "allowed",
            "generate": "ask",
            "transform": "ask",
            "execute": "blocked",
        },
        subtypes=["academic", "market", "user", "technical", "competitive"],
    ),
    DomainMenuOption(
        key="design",
        name="design",
        display_name="Design",
        description="Product and system design work",
        formalize_artifact_name="Design Brief",
        formalize_artifact_path="docs/design-brief.md",
        default_privacy="personal",
        ai_permissions={
            "suggest": "allowed",
            "complete": "allowed",
            "generate": "allowed",
            "transform": "allowed",
            "execute": "blocked",
        },
        subtypes=["ux", "ui", "system", "service", "product"],
    ),
    DomainMenuOption(
        key="data",
        name="data",
        display_name="Data",
        description="Data analysis and modeling work",
        formalize_artifact_name="Data Analysis Plan",
        formalize_artifact_path="docs/analysis-plan.md",
        default_privacy="confidential",
        ai_permissions={
            "suggest": "allowed",
            "complete": "ask",
            "generate": "ask",
            "transform": "ask",
            "execute": "ask",
        },
        subtypes=["analysis", "modeling", "visualization", "pipeline", "quality"],
    ),
    DomainMenuOption(
        key="custom",
        name="",  # Will be filled in by user
        display_name="Custom Domain",
        description="Define your own domain from scratch",
    ),
]


def get_domain_menu_options() -> list[DomainMenuOption]:
    """Get predefined domain template options for menu selection."""
    return DOMAIN_MENU_OPTIONS


def create_domain_guided(
    workspace_path: Path | None = None,
    interactive: bool = True,
) -> DomainCreationResult:
    """Create a new domain using guided Q&A.

    Args:
        workspace_path: Optional workspace path (defaults to PRAXIS_HOME)
        interactive: If True, use interactive prompts. If False, return error.

    Returns:
        DomainCreationResult with success status and created files
    """
    if not interactive:
        return DomainCreationResult(
            success=False,
            errors=["Interactive mode required for domain creation"],
        )

    # Determine workspace path
    if workspace_path is None:
        praxis_home = os.environ.get("PRAXIS_HOME")
        if not praxis_home:
            return DomainCreationResult(
                success=False,
                errors=["PRAXIS_HOME not set and --workspace not provided"],
            )
        workspace_path = Path(praxis_home)

    if not workspace_path.exists():
        return DomainCreationResult(
            success=False,
            errors=[f"Workspace not found: {workspace_path}"],
        )

    # Step 1: Show menu of predefined options
    menu_choices = [
        questionary.Choice(
            title=f"{opt.display_name} - {opt.description}",
            value=opt.key,
        )
        for opt in DOMAIN_MENU_OPTIONS
    ]

    selected_key = questionary.select(
        "Select a domain template:",
        choices=menu_choices,
    ).ask()

    if selected_key is None:
        return DomainCreationResult(
            success=False,
            errors=["Domain creation cancelled"],
        )

    # Find selected option
    selected_option = next(
        (opt for opt in DOMAIN_MENU_OPTIONS if opt.key == selected_key),
        None,
    )

    if selected_option is None:
        return DomainCreationResult(
            success=False,
            errors=["Invalid menu selection"],
        )

    # Step 2: Customize based on selection
    if selected_key == "custom":
        spec = _create_custom_domain_interactive()
    else:
        spec = _create_from_template_interactive(selected_option)

    if spec is None:
        return DomainCreationResult(
            success=False,
            errors=["Domain creation cancelled"],
        )

    # Step 3: Add metadata
    spec.author = os.environ.get("USER", "unknown")
    spec.created_at = datetime.utcnow().isoformat() + "Z"

    # Step 4: Save domain specification
    domains_dir = workspace_path / "domains"
    domains_dir.mkdir(exist_ok=True)

    spec_path = domains_dir / f"{spec.name}.yaml"
    if spec_path.exists():
        overwrite = questionary.confirm(
            f"Domain '{spec.name}' already exists. Overwrite?",
            default=False,
        ).ask()
        if not overwrite:
            return DomainCreationResult(
                success=False,
                errors=["Domain creation cancelled - file exists"],
            )

    # Write specification file
    with open(spec_path, "w") as f:
        yaml.safe_dump(
            spec.model_dump(exclude_none=True),
            f,
            default_flow_style=False,
            sort_keys=False,
        )

    return DomainCreationResult(
        success=True,
        domain_name=spec.name,
        spec_path=str(spec_path),
        files_created=[str(spec_path)],
    )


def _create_custom_domain_interactive() -> DomainSpecification | None:
    """Create a custom domain through interactive Q&A."""
    # Domain identity
    name = questionary.text(
        "Domain identifier (lowercase, alphanumeric, dashes):",
        validate=lambda text: len(text) > 0
        and text.replace("-", "").replace("_", "").isalnum()
        and text[0].isalpha(),
    ).ask()

    if name is None:
        return None

    display_name = questionary.text(
        "Display name:",
        default=name.title(),
    ).ask()

    if display_name is None:
        return None

    description = questionary.text(
        "Description (what kind of work does this domain cover?):",
    ).ask()

    if description is None:
        return None

    # Formalize artifact
    needs_artifact = questionary.confirm(
        "Does this domain require a formalize artifact?",
        default=True,
    ).ask()

    formalize_artifact_name = None
    formalize_artifact_path = None

    if needs_artifact:
        formalize_artifact_name = questionary.text(
            "Formalize artifact name (e.g., 'Solution Overview Document'):",
        ).ask()

        if formalize_artifact_name is None:
            return None

        default_path = f"docs/{name}-brief.md"
        formalize_artifact_path = questionary.text(
            "Formalize artifact path:",
            default=default_path,
        ).ask()

        if formalize_artifact_path is None:
            return None

    # Privacy default
    privacy_choices = ["public", "public-trusted", "personal", "confidential", "restricted"]
    default_privacy = questionary.select(
        "Default privacy level for new projects:",
        choices=privacy_choices,
        default="personal",
    ).ask()

    if default_privacy is None:
        return None

    # AI permissions
    ai_permissions = _configure_ai_permissions_interactive()
    if ai_permissions is None:
        return None

    # Subtypes
    subtypes = _configure_subtypes_interactive()
    if subtypes is None:
        return None

    return DomainSpecification(
        name=name,
        display_name=display_name,
        description=description,
        formalize_artifact_name=formalize_artifact_name,
        formalize_artifact_path=formalize_artifact_path,
        default_privacy=default_privacy,
        ai_permissions=ai_permissions,
        subtypes=subtypes,
    )


def _create_from_template_interactive(
    template: DomainMenuOption,
) -> DomainSpecification | None:
    """Create a domain from a template with customization."""
    # Allow customization of name
    name = questionary.text(
        "Domain identifier:",
        default=template.name,
    ).ask()

    if name is None:
        return None

    # Allow customization of display name
    display_name = questionary.text(
        "Display name:",
        default=template.display_name,
    ).ask()

    if display_name is None:
        return None

    # Allow customization of description
    description = questionary.text(
        "Description:",
        default=template.description,
    ).ask()

    if description is None:
        return None

    # Allow customization of privacy
    privacy_choices = ["public", "public-trusted", "personal", "confidential", "restricted"]
    default_privacy = questionary.select(
        "Default privacy level:",
        choices=privacy_choices,
        default=template.default_privacy,
    ).ask()

    if default_privacy is None:
        return None

    # Offer to customize AI permissions
    customize_ai = questionary.confirm(
        "Customize AI permissions?",
        default=False,
    ).ask()

    ai_permissions = template.ai_permissions
    if customize_ai:
        custom_permissions = _configure_ai_permissions_interactive()
        if custom_permissions is not None:
            ai_permissions = custom_permissions

    # Offer to customize subtypes
    customize_subtypes = questionary.confirm(
        "Customize subtypes?",
        default=False,
    ).ask()

    subtypes = template.subtypes
    if customize_subtypes:
        custom_subtypes = _configure_subtypes_interactive()
        if custom_subtypes is not None:
            subtypes = custom_subtypes

    return DomainSpecification(
        name=name,
        display_name=display_name,
        description=description,
        formalize_artifact_name=template.formalize_artifact_name,
        formalize_artifact_path=template.formalize_artifact_path,
        default_privacy=default_privacy,
        ai_permissions=ai_permissions,
        subtypes=subtypes,
    )


def _configure_ai_permissions_interactive() -> dict[str, str] | None:
    """Configure AI permissions interactively."""
    permissions = {}

    operations = ["suggest", "complete", "generate", "transform", "execute"]
    permission_choices = ["allowed", "ask", "blocked"]

    for op in operations:
        perm = questionary.select(
            f"AI permission for '{op}':",
            choices=permission_choices,
            default="allowed" if op == "suggest" else "ask",
        ).ask()

        if perm is None:
            return None

        permissions[op] = perm

    return permissions


def _configure_subtypes_interactive() -> list[str] | None:
    """Configure subtypes interactively."""
    add_subtypes = questionary.confirm(
        "Add subtypes for this domain?",
        default=True,
    ).ask()

    if not add_subtypes:
        return []

    subtypes = []
    while True:
        subtype = questionary.text(
            "Subtype name (or leave blank to finish):",
            validate=lambda text: len(text) == 0
            or (text.replace("-", "").replace("_", "").isalnum()),
        ).ask()

        if subtype is None:
            return None

        if not subtype:
            break

        subtypes.append(subtype)

    return subtypes


def list_custom_domains(workspace_path: Path | None = None) -> list[DomainSpecification]:
    """List all custom domains defined in the workspace.

    Args:
        workspace_path: Optional workspace path (defaults to PRAXIS_HOME)

    Returns:
        List of DomainSpecification objects
    """
    if workspace_path is None:
        praxis_home = os.environ.get("PRAXIS_HOME")
        if not praxis_home:
            return []
        workspace_path = Path(praxis_home)

    domains_dir = workspace_path / "domains"
    if not domains_dir.exists():
        return []

    domains = []
    for spec_file in domains_dir.glob("*.yaml"):
        try:
            with open(spec_file) as f:
                data = yaml.safe_load(f)
                spec = DomainSpecification(**data)
                domains.append(spec)
        except Exception:
            # Skip invalid specifications
            continue

    return domains


def load_domain_specification(
    domain_name: str,
    workspace_path: Path | None = None,
) -> DomainSpecification | None:
    """Load a domain specification by name.

    Args:
        domain_name: Name of the domain to load
        workspace_path: Optional workspace path (defaults to PRAXIS_HOME)

    Returns:
        DomainSpecification if found, None otherwise
    """
    if workspace_path is None:
        praxis_home = os.environ.get("PRAXIS_HOME")
        if not praxis_home:
            return None
        workspace_path = Path(praxis_home)

    spec_path = workspace_path / "domains" / f"{domain_name}.yaml"
    if not spec_path.exists():
        return None

    try:
        with open(spec_path) as f:
            data = yaml.safe_load(f)
            return DomainSpecification(**data)
    except Exception:
        return None
