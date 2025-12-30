# AI Setup Guide

This guide explains how to configure AI assistants (Claude Code, Cursor, GitHub Copilot, etc.) to work with Praxis governance.

---

## Why AI Configuration Matters

AI assistants generate content faster than humans can verify governance. Without explicit instructions, an AI will:

- Skip stages (jump straight to coding)
- Ignore formalization requirements
- Miss privacy constraints
- Forget to validate

Praxis governance works **with** AI speed by giving the AI explicit rules to follow.

---

## Quick Setup

### Option 1: `praxis init` (Recommended)

```bash
# Interactive mode
praxis init

# Or with flags
praxis init --domain code --privacy personal

# Creates:
# - praxis.yaml
# - CLAUDE.md
# - docs/capture.md
```

### Option 2: Manual Setup

1. Create `praxis.yaml` (see [User Guide](user-guide.md))
2. Create `CLAUDE.md` using the template below
3. Create `docs/capture.md` for the first stage

---

## CLAUDE.md Template

Create this file in your project root. Claude Code reads it automatically.

````markdown
# Project Name — AI Instructions

## Praxis Governance

This project follows Praxis governance. Before taking action:

1. **Read `praxis.yaml`** to understand current domain, stage, and privacy level
2. **Respect the current stage** — don't skip ahead in the lifecycle
3. **Validate before committing** — run `praxis validate` at stage transitions

## Current State

- **Domain:** code
- **Stage:** [read from praxis.yaml]
- **Privacy:** personal

## Stage-Specific Guidance

### Before Formalize (Capture → Shape)
- Focus on discovery and exploration
- It's OK to experiment and change direction
- No permanent artifacts required yet

### At Formalize
- Create `docs/sod.md` (Solution Overview Document)
- Lock scope — document what we're building and what we're NOT building
- This is the "hard boundary" before execution

### After Formalize (Commit → Sustain)
- Scope is locked — work within the SOD constraints
- If scope needs to change, regress to Formalize first
- Run `praxis validate` before commits

## Validation

Always validate at stage transitions:

```bash
poetry run praxis validate .
```

## Key References

- [Praxis Lifecycle](https://github.com/USER/praxis-ai/blob/main/core/spec/lifecycle.md)
- [Domain Definitions](https://github.com/USER/praxis-ai/blob/main/core/spec/domains.md)
- [Privacy Model](https://github.com/USER/praxis-ai/blob/main/core/spec/privacy.md)
````

---

## .cursorrules Template

For Cursor IDE, create `.cursorrules` in your project root:

```
# Praxis Governance Rules

This project uses Praxis governance (praxis-ai).

## Before any action:
1. Read praxis.yaml to check current stage
2. Respect lifecycle boundaries — don't skip stages
3. At stage >= commit, verify docs/sod.md exists

## Stage awareness:
- capture/sense/explore/shape: Discovery mode, experimentation OK
- formalize: Create SOD, lock scope
- commit/execute/sustain: Build mode, stay within SOD scope

## Validation:
Run `praxis validate .` before commits or stage transitions.

## Current project state:
- Domain: code
- Stage: [check praxis.yaml]
- Privacy: personal
```

---

## What the AI Should Read

For full context, the AI should have access to:

### Required
- `praxis.yaml` — Current project state
- `docs/sod.md` — Scope definition (if exists)

### Recommended
- `docs/lifecycle.md` — Stage definitions and allowed transitions
- `docs/domains.md` — Domain → artifact mappings
- `docs/privacy.md` — Privacy constraints

### Optional
- `docs/opinions/{domain}/` — Domain-specific quality guidance
- Previous stage documents (`docs/capture.md`, `docs/sense.md`, etc.)

---

## AI Behavior by Stage

| Stage | AI Should... | AI Should NOT... |
|-------|--------------|------------------|
| Capture | Help collect raw inputs | Start designing |
| Sense | Synthesize and clarify | Make implementation decisions |
| Explore | Investigate options, prototype | Commit to a solution |
| Shape | Define architecture | Write production code |
| Formalize | Create SOD, lock scope | Skip the SOD |
| Commit | Verify readiness | Execute without SOD |
| Execute | Build per SOD spec | Change scope |
| Sustain | Fix bugs, small enhancements | Add features without SOD update |

---

## Validation Integration

### In CI/CD

```yaml
# .github/workflows/validate.yml
- name: Validate Praxis governance
  run: |
    pip install praxis
    praxis validate --strict
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/sh
poetry run praxis validate --strict
if [ $? -ne 0 ]; then
    echo "Praxis validation failed. Fix issues before committing."
    exit 1
fi
```

### AI-Triggered Validation

Instruct the AI to validate at transitions:

```markdown
## In your CLAUDE.md:

When I say "move to [stage]":
1. Update praxis.yaml with the new stage
2. Run `praxis validate .`
3. If validation fails, fix the issue before proceeding
```

---

## Privacy Considerations

The AI should respect privacy levels:

| Privacy Level | AI Can... | AI Should NOT... |
|---------------|-----------|------------------|
| public | Use any cloud AI, share freely | — |
| public-trusted | Share with known collaborators | Post publicly |
| personal | Use cloud AI with care | Share raw content |
| confidential | Use local AI preferred | Use cloud AI with raw data |
| restricted | Local AI only | Send any data to cloud |

---

## Using `praxis init`

The `praxis init` command creates all governance files automatically:

```bash
praxis init

# Interactive prompts:
# Domain? [code/create/write/observe/learn]
# Privacy level? [public/personal/confidential/restricted]

# Generates:
# - praxis.yaml (configured)
# - CLAUDE.md (from template, customized)
# - docs/capture.md (first stage template)
```

You can also use flags to skip prompts:

```bash
praxis init --domain code --privacy personal --env Home
```

---

## Troubleshooting

### AI ignores Praxis rules

1. Verify `CLAUDE.md` or `.cursorrules` exists in project root
2. Explicitly remind the AI: "Read CLAUDE.md and follow Praxis governance"
3. Start prompts with: "Given we're at [stage] stage..."

### AI skips validation

Add to your CLAUDE.md:

```markdown
IMPORTANT: Run `praxis validate .` before ANY commit.
```

### AI doesn't know current stage

Always include in prompts:

```
Current state: domain=code, stage=execute, privacy=personal
```

Or instruct the AI to read `praxis.yaml` first.

---

## See Also

- [User Guide](user-guide.md) — Full lifecycle walkthrough
- [AI Guards](ai-guards.md) — Dynamic AI instruction generation (draft)
- [Lifecycle](lifecycle.md) — Stage definitions
