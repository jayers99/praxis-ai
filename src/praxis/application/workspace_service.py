"""Workspace management service - orchestrates workspace operations."""

from __future__ import annotations

import os
from pathlib import Path

from praxis.domain.workspace import (
    WorkspaceConfig,
    WorkspaceInfo,
    WorkspaceInitResult,
)
from praxis.infrastructure.workspace_config_repo import (
    load_workspace_config,
)


def get_praxis_home() -> Path | None:
    """Get the PRAXIS_HOME path from environment.

    Returns:
        Path to workspace root, or None if not set
    """
    praxis_home = os.environ.get("PRAXIS_HOME")
    if praxis_home:
        return Path(praxis_home).expanduser()
    return None


def require_praxis_home() -> Path:
    """Get PRAXIS_HOME or raise error if not set.

    Returns:
        Path to workspace root

    Raises:
        ValueError: If PRAXIS_HOME is not set
    """
    path = get_praxis_home()
    if path is None:
        raise ValueError(
            "PRAXIS_HOME environment variable is not set.\n\n"
            "Set it to your workspace root:\n"
            "  export PRAXIS_HOME=~/praxis-workspace\n\n"
            "Or run 'praxis workspace init' to create a new workspace."
        )
    return path


def get_praxis_ai_path(workspace_path: Path) -> Path | None:
    """Find the praxis-ai directory within a workspace.

    Args:
        workspace_path: Path to workspace root

    Returns:
        Path to praxis-ai directory, or None if not found
    """
    praxis_ai_path = workspace_path / "praxis-ai"
    if praxis_ai_path.exists():
        return praxis_ai_path
    return None


def init_workspace(
    workspace_path: Path,
    extensions_to_install: list[str] | None = None,
    examples_to_install: list[str] | None = None,
) -> WorkspaceInitResult:
    """Initialize a new Praxis workspace.

    Creates directory structure and workspace-config.yaml.
    Does not clone praxis-ai (assumes it's already present).

    Args:
        workspace_path: Path where workspace should be created
        extensions_to_install: List of extension names to install
        examples_to_install: List of example names to install

    Returns:
        WorkspaceInitResult with details of what was created
    """
    extensions_to_install = extensions_to_install or []
    examples_to_install = examples_to_install or []

    files_created: list[str] = []
    dirs_created: list[str] = []
    errors: list[str] = []
    warnings: list[str] = []
    extensions_installed: list[str] = []
    examples_installed: list[str] = []

    # Create workspace root if needed
    if not workspace_path.exists():
        try:
            workspace_path.mkdir(parents=True)
            dirs_created.append(str(workspace_path))
        except Exception as e:
            errors.append(f"Failed to create workspace directory: {e}")
            return WorkspaceInitResult(
                success=False,
                workspace_path=workspace_path,
                errors=errors,
            )

    # Create subdirectories
    for subdir in ["extensions", "examples", "projects"]:
        dir_path = workspace_path / subdir
        if not dir_path.exists():
            try:
                dir_path.mkdir()
                dirs_created.append(subdir)
            except Exception as e:
                errors.append(f"Failed to create {subdir}/: {e}")

    # Create workspace-config.yaml
    config_path = workspace_path / "workspace-config.yaml"
    if not config_path.exists():
        try:
            config = WorkspaceConfig(
                installed_extensions=extensions_to_install,
                installed_examples=examples_to_install,
            )
            from praxis.infrastructure.workspace_config_repo import (
                save_workspace_config,
            )

            save_workspace_config(workspace_path, config)
            files_created.append("workspace-config.yaml")
        except Exception as e:
            errors.append(f"Failed to create workspace-config.yaml: {e}")

    # Check for praxis-ai
    praxis_ai_path = get_praxis_ai_path(workspace_path)
    if praxis_ai_path is None:
        warnings.append(
            "praxis-ai directory not found in workspace. "
            "Clone it with: git clone https://github.com/jayers99/praxis-ai.git"
        )

    # Install extensions if requested
    if extensions_to_install and praxis_ai_path:
        from praxis.application.extension_service import add_extension

        for ext_name in extensions_to_install:
            result = add_extension(workspace_path, ext_name)
            if result.success:
                extensions_installed.append(ext_name)
            else:
                msg = f"Failed to install extension '{ext_name}': {result.error}"
                warnings.append(msg)

    # Install examples if requested
    if examples_to_install and praxis_ai_path:
        from praxis.application.extension_service import add_example

        for ex_name in examples_to_install:
            ex_result = add_example(workspace_path, ex_name)
            if ex_result.success:
                examples_installed.append(ex_name)
            else:
                msg = f"Failed to install example '{ex_name}': {ex_result.error}"
                warnings.append(msg)

    return WorkspaceInitResult(
        success=len(errors) == 0,
        workspace_path=workspace_path,
        files_created=files_created,
        dirs_created=dirs_created,
        extensions_installed=extensions_installed,
        examples_installed=examples_installed,
        errors=errors,
        warnings=warnings,
    )


def get_workspace_info(workspace_path: Path) -> WorkspaceInfo:
    """Get information about a workspace.

    Args:
        workspace_path: Path to workspace root

    Returns:
        WorkspaceInfo with workspace details

    Raises:
        FileNotFoundError: If workspace config doesn't exist
    """
    config = load_workspace_config(workspace_path)

    return WorkspaceInfo(
        path=workspace_path,
        config=config,
        extensions_path=workspace_path / "extensions",
        examples_path=workspace_path / "examples",
        projects_path=workspace_path / config.projects_path,
        praxis_ai_path=get_praxis_ai_path(workspace_path),
    )
