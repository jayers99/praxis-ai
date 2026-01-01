"""Template renderer with safe-by-default semantics."""

from __future__ import annotations

import string
from pathlib import Path
from typing import Any

from praxis.infrastructure.file_writer import write_file


class _SafeFormatter(string.Formatter):
    """A safe template formatter.

    Design choice: missing keys are left as the original placeholder (e.g. `{unknown}`)
    instead of raising.

    Rationale: stage templates may contain placeholders that are populated later, or
    braces that are meaningful to other tools. Treating missing keys as an error would
    make template rendering brittle.
    """

    def get_value(self, key: Any, args: tuple[Any, ...], kwargs: dict[str, Any]) -> Any:
        if isinstance(key, str) and key not in kwargs:
            return "{" + key + "}"
        return super().get_value(key, args, kwargs)


def render_template_text(template_text: str, context: dict[str, Any]) -> str:
    """Render a template string with partial rendering semantics.

    Any placeholder missing from `context` is preserved as-is.
    """
    formatter = _SafeFormatter()
    return formatter.vformat(template_text, args=(), kwargs=context)


def render_template_to_file(
    *,
    template_path: Path,
    destination: Path,
    context: dict[str, Any],
    force: bool,
) -> tuple[bool, str | None, str]:
    """Render a template to destination.

    Returns: (success, error, status) where status is created/skipped/overwritten.
    """

    existed = destination.exists()
    if existed and not force:
        return True, None, "skipped"

    template_text = template_path.read_text()
    content = render_template_text(template_text, context)

    ok, err = write_file(destination, content, force=force)
    if not ok:
        return False, err, "error"

    if existed and force:
        return True, None, "overwritten"
    return True, None, "created"
