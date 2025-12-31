# Rationale: Praxis Roles, Core vs Research vs Handoff

<!--
metadata:
  id: roles-rationale-2025-12-28
  title: Rationale for Praxis Roles Architecture
  date: 2025-12-28
  author: research-librarian
  status: approved
  topic: roles
  also_relevant: [foundations]
  keywords: [praxis-roles, accountability, decision-rights, core-research-handoff, scrum, adversarial-collaboration]
  consensus: high
  epistemic_standard: synthesis
  sources_count: 6
  supersedes: null
  related: [roles-decision-hats-2025-12-28, roles-example-flow-2025-12-28]
  approved_by: human
  approved_date: 2025-12-30
-->

## Executive Summary

- Praxis Roles are a **normative control surface** for solo + AI execution
- "Roles" (not "Hats") — conveys accountability, decision authority, ownership
- Three-part separation: **Core** (normative), **Research** (explanatory), **Handoff** (operational)
- Role separation prevents cognitive overload and the "AI firehose" problem
- Scrum accountabilities provide backbone; supporting roles layer around them

## Consensus Rating

**High**: Based on established frameworks (Scrum, Agile principles) and well-documented psychological research (psychological safety, adversarial collaboration).

## Body

### Thesis

Praxis Roles are a **normative control surface** for solo + AI execution: they structure decision rights, enforce short learning loops, and prevent cognitive overload. A clean separation between **core**, **research**, and **handoff** ensures the system remains governable and auditable.

### Why "Roles" (not "Hats")

"Hats" is an effective metaphor during ideation, but it is not an architectural primitive. "Roles" (or "accountabilities") better conveys:

- Decision authority and ownership
- Explicit responsibility boundaries
- Repeatable invocation semantics

Scrum's canonical language emphasizes three accountabilities (Product Owner, Scrum Master, Developers). This provides a stable backbone for your role system, with supporting roles layered around it.

### Why Split Core, Research, and Handoff

#### Core (Normative)

Core defines what the system *is*:

- Role definitions
- Allowed artifacts by phase
- Invocation syntax and matrices
- Kickback standards

Core should be stable, intentionally versioned, and treated as a policy surface.

#### Research (Explanatory)

Research explains why core is shaped the way it is:

- Citations and intellectual lineage
- Competing models and dissent
- Decision history and rejected alternatives

Research is explicitly **non-binding** so it can be expansive without destabilizing operations.

#### Handoff (Operational)

Handoff is written for execution by agents (and future-you):

- Imperative steps
- Acceptance criteria
- Refactor and migration instructions
- Verification checklists

Handoff must conform to core and may reference research for context.

### Team Health Principles This Structure Supports

1. **Clear decision rights** (prevents thrash): Roles isolate authority and avoid consensus traps.
2. **Short learning loops** (prevents over-design): Agile principles reward frequent delivery and adaptation.
3. **Psychological safety with structured dissent**: Red Team and Synthesis institutionalize disagreement without derailment.
4. **Adversarial collaboration**: Challenge and rebuttal become co-designed tests and evidence thresholds, not ego conflicts.

### Practical Benefit: Reducing Overload

Role separation plus layered outputs (executive summary + evidence pack) prevents the "AI firehose" problem:

- Humans get decision-ready summaries
- Agents get full evidence and provenance

## Reusable Artifacts

### Core/Research/Handoff Separation

| Layer | Purpose | Stability | Audience |
|-------|---------|-----------|----------|
| Core | Defines what the system is | Stable, versioned | All |
| Research | Explains why core exists | Expansive, non-binding | Curious humans, future decisions |
| Handoff | Operational instructions | Evolves with work | Agents, future-you |

## Sources

1. [The 2020 Scrum Guide (Schwaber & Sutherland)](https://scrumguides.org/scrum-guide.html)
2. [Scrum.org: Accountability vs Roles](https://www.scrum.org/resources/accountability-responsibility-and-roles)
3. [Agile Manifesto](https://agilemanifesto.org/) and [12 Principles](https://agilealliance.org/agile101/12-principles-behind-the-agile-manifesto/)
4. [Amy Edmondson: Psychological Safety](https://www.bu.edu/ombuds/resources/psychological-safety/)
5. [Daniel Kahneman: Adversarial Collaboration](https://www.edge.org/adversarial-collaboration-daniel-kahneman)
6. [UPenn Adversarial Collaboration Project](https://web.sas.upenn.edu/adcollabproject/)

---

_Migrated from research/roles/rationale.md_
_Approved: 2025-12-30_
