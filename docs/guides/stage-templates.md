# Stage Templates

Praxis can scaffold lifecycle stage documents and domain-specific formalize artifacts using deterministic, safe-by-default templates.

## What it generates

- **Stage docs:** `docs/<stage>.md` for each lifecycle stage (Capture → Close)
- **Formalize artifacts:** Domain-specific artifacts when rendering Formalize or later stages:
  - Code domain: `docs/sod.md` (Solution Overview Document)
  - Create domain: `docs/brief.md` (Creative Brief)
  - Write domain: `docs/brief.md` (Writing Brief)
  - Learn domain: `docs/plan.md` (Learning Plan)
  - Observe domain: No formalize artifact (Observe is for raw capture only)

## How to render templates

Render stage docs into the current project:

```bash
praxis templates render
```

Common options:

```bash
praxis templates render --domain code
praxis templates render --subtype api-backend
praxis templates render --stage formalize    # Only render formalize stage + artifact
praxis templates render --stage commit       # Render commit stage doc
praxis templates render --force              # Overwrite existing files
```

## Rendering formalize artifacts

To generate the formalize artifact for your domain:

```bash
praxis templates render --stage formalize
```

This will create:
- The stage doc: `docs/formalize.md`
- The domain artifact (e.g., `docs/sod.md` for Code domain)

The artifact provides structure for:
1. Intent & Outcome — Problem statement, audience, success criteria
2. Scope & Boundaries — What's in/out, assumptions, dependencies
3. Constraints — Domain, environment, privacy, tooling limits
4. Execution Framing — First increment, risks, open questions
5. Commit Criteria — Readiness for execution

Notes:

- Default behavior is non-destructive: existing files are skipped.
- Use `--force` only when you explicitly want to overwrite.
- If you omit `--stage`, Praxis renders all lifecycle stage docs.
- Observe domain has no formalize artifact and shows an informative message.

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
