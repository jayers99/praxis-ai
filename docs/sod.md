# Solution Overview Document (SOD)

**Project:** Praxis  
**Version:** v0.2  
**Status:** Integrated Draft  
**Date:** 2025-12-21

---

## 1. Problem Statement

AI-assisted work today is powerful but structurally fragile.

Individuals operating across **creative, technical, and regulated domains** lack a coherent system that governs how ideas evolve into durable outcomes while maintaining safety, repeatability, and clarity. The core problems are:

1. **Ad hoc AI usage**  
   Prompts, experiments, and executions are disconnected, non-repeatable, and rarely lifecycle-aware.

2. **Late and manual privacy decisions**  
   Sensitivity is often recognized after artifacts already exist, creating risk, rework, or abandonment.

3. **Context switching friction**  
   Work often begins informally (home, creative) and must later be adapted to conservative or regulated environments.

4. **No end-to-end lifecycle model**  
   Existing tools optimize for isolated tasks, not the full arc from raw capture to sustained maintenance.

5. **No enforceable AI governance layer**  
   Users rely on memory and discipline rather than deterministic controls for storage, collaboration, and AI exposure.

---

## 2. Desired Outcomes

Praxis aims to provide a **governed, reusable system** that:

1. Treats AI as a **policy-constrained collaborator**, not an unbounded assistant.
2. Supports the **full lifecycle of work**, from capture to close.
3. Allows **privacy to evolve safely** at any point in the lifecycle.
4. Separates **thinking from presentation**, enabling late-bound rendering for different environments.
5. Works consistently across **multiple domains of work**.
6. Enables **local-only or air-gapped AI** for highly sensitive projects.

---

## 3. Canonical Dimensions

Praxis behavior is determined by the composition of four dimensions, resolved deterministically.

### 3.1 Domain (What kind of work)

Each artifact belongs to exactly one domain at creation.

- **Build** – functional systems and tools  
- **Create** – aesthetic and expressive output  
- **Write** – structured externalized thought  
- **Observe** – raw capture without interpretation  
- **Learn** – internal model and skill formation  
- **Project Planning** – coordination and sequencing of work  

Domains define:
- allowed artifact types  
- storage expectations  
- AI usage patterns  
- quality bars  

---

### 3.2 Lifecycle Stage (Where the work is)

Praxis defines a single canonical lifecycle:

1. Capture  
2. Sense  
3. Explore  
4. Shape  
5. **Formalize** (structural hinge)  
6. Commit  
7. Execute  
8. Sustain  
9. Close  

Formalize, Commit, and Close form the **non-optional structural spine** that ensures durability and leverage.

A strict **stage → allowed regressions model** prevents unsafe or ambiguous backtracking.

---

### 3.3 Privacy (Cross-cutting control overlay)

Privacy defines **how information may be stored, shared, processed, and externalized**. It is mutable and may be reclassified mid-project.

Canonical levels (least → most restrictive):

1. Public  
2. Public – Trusted Collaborators  
3. Personal  
4. Confidential  
5. Restricted  

Privacy directly constrains:
- storage locations  
- collaboration scope  
- AI tooling  
- artifact specificity  

Higher privacy requires greater abstraction and tighter controls.

---

### 3.4 Environment (Late-bound presentation overlay)

Environment affects **tone, formality, and compliance posture**, not data handling.

- `home`  
- `work`  

Artifacts remain environment-neutral and are rendered safely later without rewriting core intent.

---

## 4. Deterministic Resolution Model

Praxis resolves behavior in a fixed order:

1. **Domain + Stage** → capability and intent  
2. **Privacy** → data, AI, and collaboration constraints  
3. **Environment** → presentation and tone  

This guarantees predictable, auditable AI behavior and prevents unsafe defaults.

---

## 5. Formalize and the Role of the SOD

Formalize is the **structural hinge** between thinking and execution.

For the **Build** domain, the Formalize artifact is the **Solution Overview Document (SOD)**.

The SOD:
- locks intent without over-specifying implementation  
- survives privacy reclassification  
- feeds downstream execution artifacts  
- defines explicit commit readiness  

### 5.1 Required SOD Sections

- Problem Statement  
- Business Context / Drivers  
- Goals  
- Non-Goals  
- Functional Overview  
- High-Level Architecture / Workflow  
- Assumptions  
- Constraints (Technical, Security, Compliance, Operational)  
- Dependencies  
- Phases / Increments  
- Risks & Mitigations  
- Open Questions / Spikes  
- Glossary / Definitions  
- Commit Readiness Checklist  

### 5.2 Explicit Exclusions

- Low-level design  
- Task breakdowns  
- Implementation detail  
- Unframed experimentation  

---

## 6. Privacy and Lifecycle Interaction

- Privacy is declared no later than **Explore**.  
- Enforced during **Shape** and **Formalize**.  
- Honored strictly during **Execute**.  
- Re-evaluated before **Commit**.  

### 6.1 Reclassification Rules

- **Upgrade (less → more restrictive):** mandatory migration, sanitization, and constraint tightening.  
- **Downgrade (more → less restrictive):** discouraged; requires explicit review and redaction.  

---

## 7. Policy Enforcement

Praxis uses **CUE** as its policy and schema backbone to:

- encode domain and lifecycle rules  
- enforce privacy invariants  
- validate reclassification  
- guarantee deterministic composition  

This enables validation-first, order-independent governance of AI behavior.

---

## 8. Summary

Praxis is a **policy-driven AI workflow system** that governs how ideas become maintained reality.

By combining:
- a universal lifecycle  
- domain-aware artifacts  
- mutable but enforceable privacy  
- late-bound environments  
- deterministic policy resolution  

Praxis enables safe, repeatable, and cumulative AI-assisted work across creative and regulated contexts.

