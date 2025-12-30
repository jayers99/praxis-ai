"""Extension and example management service."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.workspace import (
    ExampleAddResult,
    ExampleInfo,
    ExampleListResult,
    ExtensionAddResult,
    ExtensionInfo,
    ExtensionListResult,
    ExtensionRemoveResult,
)
from praxis.infrastructure.git_cloner import clone_repo, remove_repo, update_repo
from praxis.infrastructure.registry_loader import (
    load_examples_registry,
    load_extensions_registry,
)
from praxis.infrastructure.workspace_config_repo import (
    add_installed_example,
    add_installed_extension,
    load_workspace_config,
    remove_installed_extension,
)


def _get_registry_path(workspace_path: Path, filename: str) -> Path:
    """Get path to a registry file in praxis-ai directory."""
    praxis_ai_path = workspace_path / "praxis-ai"
    return praxis_ai_path / filename


def list_extensions(workspace_path: Path) -> ExtensionListResult:
    """List available and installed extensions.

    Args:
        workspace_path: Path to workspace root

    Returns:
        ExtensionListResult with available and installed extensions
    """
    registry_path = _get_registry_path(workspace_path, "extensions.yaml")

    try:
        available = load_extensions_registry(registry_path)
    except FileNotFoundError:
        available = []

    try:
        config = load_workspace_config(workspace_path)
        installed = config.installed_extensions
    except FileNotFoundError:
        installed = []

    # Mark installed extensions
    for ext in available:
        ext.installed = ext.name in installed

    return ExtensionListResult(available=available, installed=installed)


def add_extension(workspace_path: Path, extension_name: str) -> ExtensionAddResult:
    """Add (clone) an extension to the workspace.

    Args:
        workspace_path: Path to workspace root
        extension_name: Name of the extension to add

    Returns:
        ExtensionAddResult indicating success or failure
    """
    registry_path = _get_registry_path(workspace_path, "extensions.yaml")

    # Load registry to find extension
    try:
        extensions = load_extensions_registry(registry_path)
    except FileNotFoundError:
        return ExtensionAddResult(
            success=False,
            name=extension_name,
            error="Extensions registry not found. Is praxis-ai cloned?",
        )

    # Find the extension
    ext_info: ExtensionInfo | None = None
    for ext in extensions:
        if ext.name == extension_name:
            ext_info = ext
            break

    if ext_info is None:
        return ExtensionAddResult(
            success=False,
            name=extension_name,
            error=f"Extension '{extension_name}' not found in registry",
        )

    # Clone the extension
    target_path = workspace_path / "extensions" / extension_name
    result = clone_repo(ext_info.repo, target_path)

    if not result.success:
        return ExtensionAddResult(
            success=False,
            name=extension_name,
            error=result.error,
        )

    # Update workspace config
    try:
        add_installed_extension(workspace_path, extension_name)
    except Exception as e:
        return ExtensionAddResult(
            success=False,
            name=extension_name,
            path=target_path,
            error=f"Cloned but failed to update config: {e}",
        )

    return ExtensionAddResult(
        success=True,
        name=extension_name,
        path=target_path,
    )


def remove_extension(
    workspace_path: Path, extension_name: str
) -> ExtensionRemoveResult:
    """Remove an extension from the workspace.

    Args:
        workspace_path: Path to workspace root
        extension_name: Name of the extension to remove

    Returns:
        ExtensionRemoveResult indicating success or failure
    """
    target_path = workspace_path / "extensions" / extension_name

    # Remove the directory
    result = remove_repo(target_path)

    if not result.success:
        return ExtensionRemoveResult(
            success=False,
            name=extension_name,
            error=result.error,
        )

    # Update workspace config
    try:
        remove_installed_extension(workspace_path, extension_name)
    except Exception as e:
        return ExtensionRemoveResult(
            success=False,
            name=extension_name,
            error=f"Removed directory but failed to update config: {e}",
        )

    return ExtensionRemoveResult(
        success=True,
        name=extension_name,
    )


def update_extension(workspace_path: Path, extension_name: str) -> ExtensionAddResult:
    """Update (git pull) an extension.

    Args:
        workspace_path: Path to workspace root
        extension_name: Name of the extension to update

    Returns:
        ExtensionAddResult indicating success or failure
    """
    target_path = workspace_path / "extensions" / extension_name

    if not target_path.exists():
        return ExtensionAddResult(
            success=False,
            name=extension_name,
            error=f"Extension '{extension_name}' is not installed",
        )

    result = update_repo(target_path)

    return ExtensionAddResult(
        success=result.success,
        name=extension_name,
        path=target_path,
        error=result.error,
    )


def update_all_extensions(workspace_path: Path) -> list[ExtensionAddResult]:
    """Update all installed extensions.

    Args:
        workspace_path: Path to workspace root

    Returns:
        List of ExtensionAddResult for each extension
    """
    try:
        config = load_workspace_config(workspace_path)
    except FileNotFoundError:
        return []

    results = []
    for ext_name in config.installed_extensions:
        result = update_extension(workspace_path, ext_name)
        results.append(result)

    return results


def list_examples(workspace_path: Path) -> ExampleListResult:
    """List available and installed examples.

    Args:
        workspace_path: Path to workspace root

    Returns:
        ExampleListResult with available and installed examples
    """
    registry_path = _get_registry_path(workspace_path, "examples.yaml")

    try:
        available = load_examples_registry(registry_path)
    except FileNotFoundError:
        available = []

    try:
        config = load_workspace_config(workspace_path)
        installed = config.installed_examples
    except FileNotFoundError:
        installed = []

    # Mark installed examples
    for ex in available:
        ex.installed = ex.name in installed

    return ExampleListResult(available=available, installed=installed)


def add_example(workspace_path: Path, example_name: str) -> ExampleAddResult:
    """Add (clone) an example to the workspace.

    Args:
        workspace_path: Path to workspace root
        example_name: Name of the example to add

    Returns:
        ExampleAddResult indicating success or failure
    """
    registry_path = _get_registry_path(workspace_path, "examples.yaml")

    # Load registry to find example
    try:
        examples = load_examples_registry(registry_path)
    except FileNotFoundError:
        return ExampleAddResult(
            success=False,
            name=example_name,
            error="Examples registry not found. Is praxis-ai cloned?",
        )

    # Find the example
    ex_info: ExampleInfo | None = None
    for ex in examples:
        if ex.name == example_name:
            ex_info = ex
            break

    if ex_info is None:
        return ExampleAddResult(
            success=False,
            name=example_name,
            error=f"Example '{example_name}' not found in registry",
        )

    # Clone the example (into domain subfolder)
    target_path = workspace_path / "examples" / ex_info.domain.value / example_name
    result = clone_repo(ex_info.repo, target_path)

    if not result.success:
        return ExampleAddResult(
            success=False,
            name=example_name,
            error=result.error,
        )

    # Update workspace config
    try:
        add_installed_example(workspace_path, example_name)
    except Exception as e:
        return ExampleAddResult(
            success=False,
            name=example_name,
            path=target_path,
            error=f"Cloned but failed to update config: {e}",
        )

    return ExampleAddResult(
        success=True,
        name=example_name,
        path=target_path,
    )
