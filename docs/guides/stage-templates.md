# Stage Templates

Praxis can scaffold lifecycle stage documents (and a small set of domain artifacts) using deterministic, safe-by-default templates.

## What it generates

- Stage docs: `docs/<stage>.md` for lifecycle stages (Capture → Close)
- Minimal domain artifacts when applicable (example: Code `docs/sod.md` at Formalize+)

## How to render templates

Render stage docs into the current project:

```bash
praxis templates render
```

Common options:

```bash
praxis templates render --domain code
praxis templates render --subtype api-backend
praxis templates render --stage formalize
praxis templates render --force
```

Notes:
- Default behavior is non-destructive: existing files are skipped.
- Use `--force` only when you explicitly want to overwrite.

## Template locations (roots)

Praxis searches an ordered list of template roots (highest precedence first):

1. Project-local overrides: `.praxis/templates/`
2. Optional extra roots provided via CLI (advanced)
3. Core templates shipped with Praxis-AI

## Template layout

Within a template root, templates are organized like this:

```text
stage/<stage>.md

domain/<domain>/stage/<stage>.md

domain/<domain>/subtype/<subtype>/stage/<stage>.md

domain/<domain>/artifact/<name>.md

domain/<domain>/subtype/<subtype>/artifact/<name>.md
```

## Resolution order (deterministic)

For a given `domain`, optional `subtype`, and `stage`, Praxis tries candidates in this order:

1. `domain/<domain>/subtype/<subtype>/stage/<stage>.md` (if `subtype` is set)
2. `domain/<domain>/stage/<stage>.md`
3. `stage/<stage>.md` (global fallback)

The resolver is deterministic: the same inputs and the same ordered roots produce the same selected template.

## Safe rendering semantics

- If the destination file does not exist: create it.
- If it already exists: skip it.
- With `--force`: overwrite.

## Stage transitions

When you run `praxis stage <next>`, Praxis will attempt to render the new stage document (`docs/<next>.md`) as a best-effort step.

This keeps projects moving forward without bulk-generating all docs up front.

## Subtype validation

Subtype values are validated (allowlist) to prevent path traversal. Use lowercase letters, numbers, and dashes (example: `api-backend`).
