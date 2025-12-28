"""Templates for praxis init generated files."""

from __future__ import annotations

CLAUDE_MD_TEMPLATE = '''# {project_name} — AI Instructions

## Praxis Governance

This project follows Praxis governance. Before taking action:

1. **Read `praxis.yaml`** to understand current domain, stage, and privacy level
2. **Respect the current stage** — don't skip ahead in the lifecycle
3. **Validate before committing** — run `praxis validate` at stage transitions

## Current State

- **Domain:** {domain}
- **Stage:** capture
- **Privacy:** {privacy}

## Stage-Specific Guidance

### Before Formalize (Capture → Shape)
- Focus on discovery and exploration
- It's OK to experiment and change direction
- No permanent artifacts required yet

### At Formalize
- Create the formalization artifact (e.g., `docs/sod.md` for Code domain)
- Lock scope — document what we're building and what we're NOT building
- This is the "hard boundary" before execution

### After Formalize (Commit → Sustain)
- Scope is locked — work within the formalized constraints
- If scope needs to change, regress to Formalize first
- Run `praxis validate` before commits

## Validation

Always validate at stage transitions:

```bash
praxis validate .
```

## Privacy: {privacy}

Respect the declared privacy level in all AI interactions and data handling.
'''

CAPTURE_MD_TEMPLATE = '''# Capture

**Stage:** Capture
**Date:** {date}

---

## Raw Inputs

### Intent

<!-- What are you trying to build? Why? -->

### Constraints

<!-- Known limitations, requirements, or boundaries -->

### Initial Ideas

<!-- First thoughts, sketches, or brainstorms -->

---

## Next Steps

Move to **Sense** to organize these inputs into a coherent understanding.
'''


def render_claude_md(project_name: str, domain: str, privacy: str) -> str:
    """Render CLAUDE.md template with values."""
    return CLAUDE_MD_TEMPLATE.format(
        project_name=project_name,
        domain=domain,
        privacy=privacy,
    )


def render_capture_md(date: str) -> str:
    """Render capture.md template with date."""
    return CAPTURE_MD_TEMPLATE.format(date=date)
