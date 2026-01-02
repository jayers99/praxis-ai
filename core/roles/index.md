# Praxis Roles Index
**Canonical Entry Point (v1.0)**

This is the **authoritative entry point** for the Praxis Roles subsystem.
All other READMEs defer to this document.

## Authority
- This document is **normative** as an index.
- Role semantics are defined in individual role definition files.
- If documents conflict, resolve using `../authority-and-change-control.md`.

## Quick Reference

### Core Roles (always active)
| Role | Purpose | Definition |
|------|---------|------------|
| Research Librarian | Epistemic backbone; curates truth and provenance | `definitions/00-research-librarian.md` |
| Product Owner | Value decisions; backlog ordering | `definitions/01-product-owner.md` |
| Red Team | Constructive adversarial validation | `definitions/02-red-team.md` |
| Synthesis | Resolves inputs into a single direction | `definitions/03-synthesis.md` |
| Scrum Master | Cadence, flow, impediment removal | `definitions/04-scrum-master.md` |
| Developer | Produces "Done" increments | `definitions/05-developer.md` |

### Supporting Roles (invoked as needed)
| Role | Purpose | Definition |
|------|---------|------------|
| Stakeholder Proxy | User needs and acceptance language | `definitions/06-stakeholder-proxy.md` |
| Architect | Coherence and boundaries | `definitions/07-architect.md` |
| Security | Threats, controls, mitigations | `definitions/08-security.md` |
| QA | Risk-based validation strategy | `definitions/09-qa.md` |
| FinOps | Cost drivers and constraints | `definitions/10-finops.md` |
| SRE | Operability, SLOs, monitoring | `definitions/11-sre.md` |

## Governance Documents
| Document | Purpose |
|----------|---------|
| `lifecycle-matrix.md` | Which roles are active/forbidden by phase |
| `invocation-syntax.md` | Grammar for activating roles in prompts |
| `kickback-rubrics.md` | Structured rejection standards by role |
| `system-prompt-bundle.md` | Ready-to-use prompts for each role |
| `../authority-and-change-control.md` | Conflict resolution and change rules |

## File Layout

```
praxis-ai/
├── core/
│   ├── authority-and-change-control.md
│   └── roles/
│       ├── index.md               # THIS FILE (canonical entry)
│       ├── README.md              # Layer description
│       ├── lifecycle-matrix.md    # Phase → role mapping
│       ├── invocation-syntax.md   # Role activation grammar
│       ├── kickback-rubrics.md    # Rejection standards
│       ├── system-prompt-bundle.md# Agent prompts
│       └── definitions/
│           ├── 00-research-librarian.md
│           ├── 01-product-owner.md
│           ├── 02-red-team.md
│           ├── 03-synthesis.md
│           ├── 04-scrum-master.md
│           ├── 05-developer.md
│           ├── 06-stakeholder-proxy.md
│           ├── 07-architect.md
│           ├── 08-security.md
│           ├── 09-qa.md
│           ├── 10-finops.md
│           └── 11-sre.md
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
