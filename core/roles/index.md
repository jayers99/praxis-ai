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
| Librarian | Query interface to research-library; retrieves and summarizes | `definitions/00-research-librarian.md` |
| Product Owner | Value decisions; backlog ordering | `definitions/01-product-owner.md` |
| Red Team | Constructive adversarial validation | `definitions/02-red-team.md` |
| Synthesis | Resolves inputs into a single direction | `definitions/03-synthesis.md` |
| Scrum Master | Cadence, flow, impediment removal | `definitions/04-scrum-master.md` |
| Developer | Produces "Done" increments | `definitions/05-developer.md` |

### Supporting Roles (invoked as needed)
| Role | Purpose | Definition |
|------|---------|------------|
| Stakeholder | User needs and acceptance language | `definitions/06-stakeholder.md` |
| Architect | Coherence and boundaries | `definitions/07-architect.md` |
| Security | Threats, controls, mitigations | `definitions/08-security.md` |
| QA | Risk-based validation strategy | `definitions/09-qa.md` |
| FinOps | Cost drivers and constraints | `definitions/10-finops.md` |
| SRE | Operability, SLOs, monitoring | `definitions/11-sre.md` |
| Researcher | Conducts inquiry-driven research; produces draft artifacts | `definitions/12-researcher.md` |
| Cataloger | Indexes approved artifacts into research-library | `definitions/13-cataloger.md` |

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
│           ├── 00-research-librarian.md  # v2.0 (renamed: Librarian)
│           ├── 01-product-owner.md       # v1.1
│           ├── 02-red-team.md            # v1.1
│           ├── 03-synthesis.md           # v1.1
│           ├── 04-scrum-master.md        # v1.1
│           ├── 05-developer.md           # v1.1
│           ├── 06-stakeholder.md         # v1.1
│           ├── 07-architect.md           # v1.1
│           ├── 08-security.md            # v1.1
│           ├── 09-qa.md                  # v1.1
│           ├── 10-finops.md              # v1.1
│           ├── 11-sre.md                 # v1.1
│           ├── 12-researcher.md          # v1.0
│           └── 13-cataloger.md           # v1.0
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
