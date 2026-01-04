# Praxis Roles Index
**Canonical Entry Point (v1.2)**

This is the **authoritative entry point** for the Praxis Roles subsystem.
All other READMEs defer to this document.

## Authority
- This document is **normative** as an index.
- Role semantics are defined in individual role definition files.
- If documents conflict, resolve using `../authority-and-change-control.md`.

## Quick Reference

### Core Roles
| Role | Purpose | Definition |
|------|---------|------------|
| Librarian | Query interface to research-library; retrieves and summarizes | `definitions/librarian.md` |
| Product Owner | Value decisions; backlog ordering | `definitions/product-owner.md` |
| Red Team | Constructive adversarial validation | `definitions/red-team.md` |
| Synthesis | Resolves inputs into a single direction | `definitions/synthesis.md` |
| Scrum Master | Cadence, flow, impediment removal | `definitions/scrum-master.md` |
| Developer | Produces "Done" increments | `definitions/developer.md` |

### Supporting Roles (invoked as needed)
| Role | Purpose | Definition |
|------|---------|------------|
| Stakeholder | User needs and acceptance language | `definitions/stakeholder.md` |
| Architect | Coherence and boundaries | `definitions/architect.md` |
| Security | Threats, controls, mitigations | `definitions/security.md` |
| QA | Risk-based validation strategy | `definitions/qa.md` |
| FinOps | Cost drivers and constraints | `definitions/finops.md` |
| SRE | Operability, SLOs, monitoring | `definitions/sre.md` |
| Researcher | Conducts inquiry-driven research; produces draft artifacts | `definitions/researcher.md` |
| Cataloger | Indexes approved artifacts into research-library | `definitions/cataloger.md` |

## Governance Documents

### Core Governance
| Document | Purpose |
|----------|---------|
| `lifecycle-matrix.md` | Which roles are active/forbidden by phase; Praxis stage mapping |
| `invocation-syntax.md` | Grammar for activating roles in prompts |
| `kickback-rubrics.md` | Structured rejection standards by role |
| `system-prompt-bundle.md` | Ready-to-use prompts for each role |
| `../authority-and-change-control.md` | Conflict resolution and change rules |

### Extended Governance
| Document | Purpose |
|----------|---------|
| `role-composition-patterns.md` | Common patterns for combining roles in reviews |
| `subagent-mapping.md` | Mapping roles to AI subagent implementations |
| `domain-variants.md` | Role adaptations for Create, Write, Learn, Observe domains |
| `metrics-framework.md` | Metrics for tracking role effectiveness (advisory) |

## File Layout

```
praxis-ai/
├── core/
│   ├── authority-and-change-control.md
│   └── roles/
│       ├── index.md                    # THIS FILE (canonical entry)
│       ├── README.md                   # Layer description
│       ├── lifecycle-matrix.md         # Phase → role mapping + Praxis stages
│       ├── invocation-syntax.md        # Role activation grammar
│       ├── kickback-rubrics.md         # Rejection standards
│       ├── system-prompt-bundle.md     # Agent prompts
│       ├── role-composition-patterns.md # Multi-role review patterns
│       ├── subagent-mapping.md         # Role → subagent mapping
│       ├── domain-variants.md          # Domain-specific role adaptations
│       ├── metrics-framework.md        # Role effectiveness metrics
│       └── definitions/
│           ├── architect.md              # v1.1
│           ├── cataloger.md              # v1.0
│           ├── developer.md              # v1.1
│           ├── finops.md                 # v1.1
│           ├── librarian.md              # v2.0 (renamed: Librarian)
│           ├── product-owner.md          # v1.1
│           ├── qa.md                     # v1.1
│           ├── red-team.md               # v1.1
│           ├── researcher.md             # v1.0
│           ├── scrum-master.md           # v1.1
│           ├── security.md               # v1.1
│           ├── sre.md                    # v1.1
│           ├── stakeholder.md            # v1.1
│           └── synthesis.md              # v1.1
├── research-library/
│   └── roles/
│       ├── rationale.md
│       ├── decision-hats.md
│       └── example-flow.md
└── handoff/
    └── roles/
        ├── refactor-praxis-roles.md
        └── agent-refactor-prompt.md
```

## Related Documentation
- **Research**: `../../research-library/roles/` — Rationale and design decisions
- **Handoff**: `../../handoff/roles/` — Operational migration docs
