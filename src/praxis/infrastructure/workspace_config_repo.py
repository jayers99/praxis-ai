"""Repository for reading and writing workspace configuration."""

from __future__ import annotations

from pathlib import Path

import yaml

from praxis.domain.privacy import PrivacyLevel
from praxis.domain.workspace import WorkspaceConfig, WorkspaceDefaults

WORKSPACE_CONFIG_FILENAME = "workspace-config.yaml"


def load_workspace_config(workspace_path: Path) -> WorkspaceConfig:
    """Load workspace configuration from workspace-config.yaml.

    Args:
        workspace_path: Path to workspace root directory

    Returns:
        WorkspaceConfig object

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If config file is malformed
    """
    config_path = workspace_path / WORKSPACE_CONFIG_FILENAME

    if not config_path.exists():
        raise FileNotFoundError(f"Workspace config not found: {config_path}")

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Empty workspace config: {config_path}")

    # Parse workspace section
    workspace_data = data.get("workspace", {})
    projects_path = workspace_data.get("projects_path", "./projects")

    # Parse installed items
    installed_extensions = data.get("installed_extensions", [])
    installed_examples = data.get("installed_examples", [])

    # Parse defaults
    defaults_data = data.get("defaults", {})
    privacy_str = defaults_data.get("privacy", "personal")
    try:
        privacy = PrivacyLevel(privacy_str)
    except ValueError:
        privacy = PrivacyLevel.PERSONAL

    defaults = WorkspaceDefaults(
        privacy=privacy,
        environment=defaults_data.get("environment", "Home"),
    )

    return WorkspaceConfig(
        projects_path=projects_path,
        installed_extensions=installed_extensions,
        installed_examples=installed_examples,
        defaults=defaults,
    )


def save_workspace_config(workspace_path: Path, config: WorkspaceConfig) -> None:
    """Save workspace configuration to workspace-config.yaml.

    Args:
        workspace_path: Path to workspace root directory
        config: WorkspaceConfig object to save
    """
    config_path = workspace_path / WORKSPACE_CONFIG_FILENAME

    data = {
        "workspace": {
            "projects_path": config.projects_path,
        },
        "installed_extensions": config.installed_extensions,
        "installed_examples": config.installed_examples,
        "defaults": {
            "privacy": config.defaults.privacy.value,
            "environment": config.defaults.environment,
        },
    }

    with open(config_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def create_default_workspace_config(workspace_path: Path) -> WorkspaceConfig:
    """Create a default workspace configuration file.

    Args:
        workspace_path: Path to workspace root directory

    Returns:
        The created WorkspaceConfig object
    """
    config = WorkspaceConfig()
    save_workspace_config(workspace_path, config)
    return config


def add_installed_extension(workspace_path: Path, extension_name: str) -> None:
    """Add an extension to the installed list.

    Args:
        workspace_path: Path to workspace root directory
        extension_name: Name of extension to add
    """
    config = load_workspace_config(workspace_path)
    if extension_name not in config.installed_extensions:
        config.installed_extensions.append(extension_name)
        save_workspace_config(workspace_path, config)


def remove_installed_extension(workspace_path: Path, extension_name: str) -> None:
    """Remove an extension from the installed list.

    Args:
        workspace_path: Path to workspace root directory
        extension_name: Name of extension to remove
    """
    config = load_workspace_config(workspace_path)
    if extension_name in config.installed_extensions:
        config.installed_extensions.remove(extension_name)
        save_workspace_config(workspace_path, config)


def add_installed_example(workspace_path: Path, example_name: str) -> None:
    """Add an example to the installed list.

    Args:
        workspace_path: Path to workspace root directory
        example_name: Name of example to add
    """
    config = load_workspace_config(workspace_path)
    if example_name not in config.installed_examples:
        config.installed_examples.append(example_name)
        save_workspace_config(workspace_path, config)
