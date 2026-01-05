# praxis-ai — AI Instructions

## Praxis Governance

This project follows Praxis governance. Before taking action:

1. **Read `praxis.yaml`** to understand current domain, stage, and privacy level
2. **Respect the current stage** — don't skip ahead in the lifecycle
3. **Validate before committing** — run `praxis validate` at stage transitions

## Current State

- **Domain:** code
- **Stage:** capture
- **Privacy:** public-trusted

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

## Privacy: public-trusted

Respect the declared privacy level in all AI interactions and data handling.
