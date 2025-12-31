# Spec Research Index

_Artifacts: 3_
_Last updated: 2025-12-30_

## Purpose

Research behind Praxis specifications. Technical deep-dives, implementation options, and design rationale for core specs.

## Contents

| Title | Consensus | Keywords | Summary |
|-------|-----------|----------|---------|
| [Lifecycle Stage Research](lifecycle-research.md) | High | lifecycle, stages, formalize, stage-gate | All 9 stages mapped to established frameworks (GTD, Weick, Shape Up, Stage-Gate, ITIL, PMI). Unique contributions: Formalize hinge, two iteration modes. |
| [Domain Definitions Research](domains-research.md) | High | domains, code, create, write, observe, learn | 5 domains with 28 subtypes, AI permission matrix, transition patterns, boundary resolution. |
| [Worked Example: Iteration vs Sustain](sustain-worked-example.md) | Medium | sustain, iteration, governance | CLI ideals as quality overlay, not scope change. Decision criteria for Sustain vs Iteration. |

## Key Themes

### The Formalize Hinge

Most frameworks blur exploration and execution. Praxis makes Formalize an explicit structural hinge:

- **Before Formalize:** Discovery iteration (cheap to change what)
- **After Formalize:** Refinement iteration (improve how)

### AI Governance by Stage

Novel contribution — no prior art found. Praxis restricts AI operations based on lifecycle stage and domain.

### Domain Transitions

Artifacts can move between domains (Observe → Write, Write → Code) but each artifact belongs to exactly one domain at a time. Transition requires explicit recognition.

## Related Topics

- [Foundations](../foundations/_index.md) — theoretical grounding
- [Patterns](../patterns/_index.md) — implementation patterns
- [Domain](../domain/_index.md) — domain-specific research

---

_Maintained by: research-librarian (librarian function)_
