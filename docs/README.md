# Praxis Documentation

## Directory Structure

```
praxis-ai/
├── core/                   # Normative (binding)
│   ├── spec/               # System specifications
│   │   ├── sod.md          # Solution Overview Document
│   │   ├── lifecycle.md    # The nine stages (incl. Formalize & Sustain governance)
│   │   ├── domains.md      # Code, Create, Write, Learn, Observe
│   │   └── privacy.md      # Privacy levels
│   ├── governance/         # Decision surfaces
│   │   ├── layer-model.md
│   │   ├── decision-arbitration.md
│   │   ├── opinions-contract.md
│   │   └── ...
│   ├── ai/                 # AI behavior controls
│   │   ├── ai-guards.md
│   │   ├── model-selection-matrix.md
│   │   └── models/
│   └── roles/              # Praxis Roles subsystem
│       ├── index.md        # Canonical entry point
│       ├── lifecycle-matrix.md
│       └── definitions/    # 12 role definitions
│
├── opinions/               # Advisory (non-binding)
│   ├── code/
│   ├── create/
│   ├── write/
│   ├── learn/
│   └── observe/
|
├── research-library/       # Explanatory (non-binding)
│   ├── foundations/        # Theoretical grounding
│   ├── spec/               # Research behind specs
│   ├── ai-guards/
│   └── roles/
│
├── docs/                   # User-facing
│   └── guides/
│       ├── user-guide.md   # Step-by-step walkthrough
│       ├── ai-setup.md     # Configure AI assistants
│       └── pkdp.md         # Knowledge distillation pipeline
│
├── handoff/                # Operational (for agents)
│   └── roles/
│
└── adr/                    # Architecture decisions
```

## Entry Points

| Starting Point   | Location                    |
| ---------------- | --------------------------- |
| Main spec        | `core/spec/sod.md`          |
| Lifecycle stages | `core/spec/lifecycle.md`    |
| Praxis Roles     | `core/roles/index.md`       |
| User guide       | `docs/guides/user-guide.md` |
| AI setup guide   | `docs/guides/ai-setup.md`   |
| PKDP guide       | `docs/guides/pkdp.md`       |
| Domain opinions  | `opinions/`                 |

## Layer Authority

1. **core/** — Normative, binding
2. **handoff/** — Operational, must conform to core
3. **research/** — Explanatory, non-binding
4. **opinions/** — Advisory, domain-specific
5. **docs/guides/** — Tutorials, user-facing
6. **adr/** — Historical decisions
