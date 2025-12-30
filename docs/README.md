# Documentation

> **NOTICE**: Documentation has been reorganized into a layered architecture.

## New Locations

| Old Location | New Location | Description |
|--------------|--------------|-------------|
| `docs/sod.md`, `docs/lifecycle.md`, etc. | `core/spec/` | System specifications |
| `docs/layer-model.md`, `docs/decision-arbitration.md`, etc. | `core/governance/` | Governance documents |
| `docs/ai-guards.md`, `docs/model-selection-matrix.md` | `core/ai/` | AI behavior controls |
| `docs/opinions/` | `opinions/` | Advisory domain guidance |
| `docs/research/` | `research/` | Explanatory background |
| `docs/adr/` | `adr/` | Architecture decisions |
| `docs/user-guide.md` | `guides/user-guide.md` | User tutorials |
| `docs/ai-setup.md` | `guides/ai-setup.md` | AI setup guide |

## Entry Points

- **Core specification**: [`core/spec/sod.md`](../core/spec/sod.md)
- **Praxis Roles**: [`core/roles/index.md`](../core/roles/index.md)
- **User guide**: [`guides/user-guide.md`](../guides/user-guide.md)
- **Opinions**: [`opinions/`](../opinions/)

## Layer Authority (Descending)

1. `core/` — Normative, binding
2. `handoff/` — Operational, must conform to core
3. `research/` — Explanatory, non-binding
4. `opinions/` — Advisory, domain-specific
5. `guides/` — Tutorials, user-facing
6. `adr/` — Historical decisions
