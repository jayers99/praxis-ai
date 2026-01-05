"""Infrastructure for loading and validating extension manifests."""

from __future__ import annotations

from pathlib import Path

import yaml

from praxis.domain.workspace import (
    AuditCheckContribution,
    AuditContribution,
    ExtensionContributions,
    ExtensionManifest,
    ManifestLoadResult,
    OpinionContribution,
    TemplateContribution,
)

# Supported manifest versions (semver MAJOR.MINOR)
SUPPORTED_MANIFEST_VERSIONS = ["0.1"]


def load_extension_manifest(extension_path: Path, extension_name: str) -> ManifestLoadResult:
    """Load and validate an extension manifest.

    Args:
        extension_path: Path to extension directory
        extension_name: Expected name of the extension

    Returns:
        ManifestLoadResult with parsed manifest or error details
    """
    manifest_path = extension_path / "praxis-extension.yaml"

    # Check if manifest exists
    if not manifest_path.exists():
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error=f"No praxis-extension.yaml found in {extension_path}",
        )

    # Parse YAML
    try:
        with open(manifest_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error=f"Invalid YAML in manifest: {e}",
        )
    except Exception as e:
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error=f"Failed to read manifest: {e}",
        )

    if not isinstance(data, dict):
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error="Manifest must be a YAML dictionary",
        )

    # Validate manifest_version
    manifest_version = data.get("manifest_version")
    if not manifest_version:
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error="Missing required field: manifest_version",
        )

    if manifest_version not in SUPPORTED_MANIFEST_VERSIONS:
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error=f"Unsupported manifest version '{manifest_version}'. "
            f"Supported versions: {', '.join(SUPPORTED_MANIFEST_VERSIONS)}",
        )

    # Validate name matches directory
    manifest_name = data.get("name")
    if not manifest_name:
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error="Missing required field: name",
        )

    if manifest_name != extension_name:
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error=f"Manifest name '{manifest_name}' does not match " f"extension directory name '{extension_name}'",
        )

    # Parse contributions
    try:
        contributions_data = data.get("contributions", {})
        opinions_data = contributions_data.get("opinions", [])
        templates_data = contributions_data.get("templates", [])
        audits_data = contributions_data.get("audits", [])

        opinions = []
        for opinion_data in opinions_data:
            if not isinstance(opinion_data, dict):
                return ManifestLoadResult(
                    success=False,
                    extension_name=extension_name,
                    error=f"Invalid opinion contribution: {opinion_data}",
                )
            opinions.append(OpinionContribution(**opinion_data))

        templates = []
        warnings = []
        for template_data in templates_data:
            if not isinstance(template_data, dict):
                return ManifestLoadResult(
                    success=False,
                    extension_name=extension_name,
                    error=f"Invalid template contribution: {template_data}",
                )

            # Parse the template contribution
            template_contrib = TemplateContribution(**template_data)

            # Validate that the source file exists
            source_path = extension_path / template_contrib.source
            if not source_path.exists():
                warning = (
                    f"Template source not found: {template_contrib.source} "
                    f"(skipping contribution to {template_contrib.target})"
                )
                warnings.append(warning)
                continue  # Skip this invalid contribution

            templates.append(template_contrib)

        # Parse audit contributions
        audits = []
        for audit_data in audits_data:
            if not isinstance(audit_data, dict):
                warning = f"Invalid audit contribution (not a dict): {audit_data}"
                warnings.append(warning)
                continue  # Skip malformed contribution

            try:
                # Parse checks within this audit contribution
                checks_data = audit_data.get("checks", [])
                checks = []
                for check_data in checks_data:
                    if not isinstance(check_data, dict):
                        warning = f"Invalid audit check (not a dict): {check_data}"
                        warnings.append(warning)
                        continue

                    try:
                        check_contrib = AuditCheckContribution(**check_data)
                        checks.append(check_contrib)
                    except Exception as e:
                        warning = f"Malformed audit check '{check_data.get('name', 'unknown')}': {e}"
                        warnings.append(warning)
                        continue

                # Create audit contribution with validated checks
                audit_contrib = AuditContribution(
                    domain=audit_data.get("domain", ""),
                    subtypes=audit_data.get("subtypes", []),
                    checks=checks,
                )
                audits.append(audit_contrib)
            except Exception as e:
                warning = f"Malformed audit contribution: {e}"
                warnings.append(warning)
                continue

        contributions = ExtensionContributions(opinions=opinions, templates=templates, audits=audits)

        manifest = ExtensionManifest(
            manifest_version=manifest_version,
            name=manifest_name,
            description=data.get("description"),
            contributions=contributions,
        )

        result = ManifestLoadResult(
            success=True,
            extension_name=extension_name,
            manifest=manifest,
        )

        # Add warning if any template sources were missing
        if warnings:
            result.warning = "; ".join(warnings)

        return result

    except Exception as e:
        return ManifestLoadResult(
            success=False,
            extension_name=extension_name,
            error=f"Failed to parse manifest: {e}",
        )


def discover_extension_manifests(extensions_path: Path, installed_extensions: list[str]) -> list[ManifestLoadResult]:
    """Discover and load manifests for all installed extensions.

    Args:
        extensions_path: Path to workspace extensions directory
        installed_extensions: List of installed extension names

    Returns:
        List of ManifestLoadResult for each installed extension
    """
    results: list[ManifestLoadResult] = []

    for ext_name in installed_extensions:
        ext_path = extensions_path / ext_name
        if not ext_path.exists():
            results.append(
                ManifestLoadResult(
                    success=False,
                    extension_name=ext_name,
                    error=f"Extension directory not found: {ext_path}",
                )
            )
            continue

        result = load_extension_manifest(ext_path, ext_name)
        results.append(result)

    return results
