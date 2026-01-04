"""Slug generation and normalization helpers."""

from __future__ import annotations

import re


def slugify(text: str) -> str:
    """Convert text to kebab-case slug.

    Args:
        text: Input text to convert.

    Returns:
        Kebab-case slug (lowercase, alphanumeric and hyphens only).
        Returns 'unnamed-project' if slug would be empty.

    Examples:
        >>> slugify("My Project")
        'my-project'
        >>> slugify("my_project")
        'my-project'
        >>> slugify("My-CLI-Tool!")
        'my-cli-tool'
        >>> slugify("   ")
        'unnamed-project'
    """
    # Convert to lowercase
    slug = text.lower()
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip leading and trailing hyphens
    slug = slug.strip("-")
    # Fallback for empty slugs
    return slug or "unnamed-project"


def title_case_name(text: str) -> str:
    """Convert slug/dirname to title case name.

    Args:
        text: Input text (typically a slug or directory name).

    Returns:
        Title-cased name with spaces instead of hyphens/underscores.

    Examples:
        >>> title_case_name("my-project")
        'My Project'
        >>> title_case_name("my_cli_tool")
        'My Cli Tool'
        >>> title_case_name("api-backend")
        'Api Backend'
    """
    # Replace hyphens and underscores with spaces
    name = text.replace("-", " ").replace("_", " ")
    # Apply title case
    return name.title()
