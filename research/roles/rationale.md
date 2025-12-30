# Rationale: Praxis Roles, Core vs Research vs Handoff
**Research Reference (v1.0)**

## Thesis
Praxis Roles are a **normative control surface** for solo + AI execution: they structure decision rights, enforce short learning loops, and prevent cognitive overload. A clean separation between **core**, **research**, and **handoff** ensures the system remains governable and auditable.

## Why “Roles” (not “Hats”)
“Hats” is an effective metaphor during ideation, but it is not an architectural primitive. “Roles” (or “accountabilities”) better conveys:
- decision authority and ownership
- explicit responsibility boundaries
- repeatable invocation semantics

Scrum’s canonical language emphasizes three accountabilities (Product Owner, Scrum Master, Developers). This provides a stable backbone for your role system, with supporting roles layered around it.

## Why split Core, Research, and Handoff
### Core (normative)
Core defines what the system *is*:
- role definitions
- allowed artifacts by phase
- invocation syntax and matrices
- kickback standards

Core should be stable, intentionally versioned, and treated as a policy surface.

### Research (explanatory)
Research explains why core is shaped the way it is:
- citations and intellectual lineage
- competing models and dissent
- decision history and rejected alternatives

Research is explicitly **non-binding** so it can be expansive without destabilizing operations.

### Handoff (operational)
Handoff is written for execution by agents (and future-you):
- imperative steps
- acceptance criteria
- refactor and migration instructions
- verification checklists

Handoff must conform to core and may reference research for context.

## Team health principles this structure supports
1. **Clear decision rights** (prevents thrash): roles isolate authority and avoid consensus traps.
2. **Short learning loops** (prevents over-design): agile principles reward frequent delivery and adaptation.
3. **Psychological safety with structured dissent**: Red Team and Synthesis institutionalize disagreement without derailment.
4. **Adversarial collaboration**: challenge and rebuttal become co-designed tests and evidence thresholds, not ego conflicts.

## Practical benefit: reducing overload
Role separation plus layered outputs (executive summary + evidence pack) prevents the “AI firehose” problem:
- humans get decision-ready summaries
- agents get full evidence and provenance

## Bibliography (URLs in code blocks)
- The 2020 Scrum Guide (Schwaber & Sutherland)
```text
https://scrumguides.org/scrum-guide.html
```
- Scrum.org: Accountability vs Roles (context on “accountabilities” terminology)
```text
https://www.scrum.org/resources/accountability-responsibility-and-roles
```
- Agile Manifesto (values) and principles
```text
https://agilemanifesto.org/
https://agilealliance.org/agile101/12-principles-behind-the-agile-manifesto/
```
- Amy Edmondson definition of psychological safety (interpersonal risk taking)
```text
https://www.bu.edu/ombuds/resources/psychological-safety/
```
- Daniel Kahneman on adversarial collaboration (Edge lecture)
```text
https://www.edge.org/adversarial-collaboration-daniel-kahneman
```
- UPenn Adversarial Collaboration Project (institutionalization of the method)
```text
https://web.sas.upenn.edu/adcollabproject/
```
