# Praxis Layer Model — Opinions, Governance, Execution

Version: 0.1.0  
Status: Active  
Last Updated: 2025-12-23

---

## Purpose

This document defines the **three-layer conceptual model** used by Praxis to separate:

- What we believe
- How decisions are arbitrated
- How work is executed

The explicit separation of these layers prevents:

- Principles turning into dogma
- Governance collapsing into bureaucracy
- Execution drifting without intent

This document exists to **clarify authority, responsibility, and interaction** between layers.

---

## The Three Layers

Praxis is intentionally structured into three distinct layers:

```text
Opinions  →  Governance  →  Execution
```

Each layer has a different purpose, lifespan, and authority level.

---

## Layer 1: Opinions

**What it is:**  
Timeless viewpoints, values, and intellectual influences that bias decisions.

**What it is not:**  
Rules, policies, workflows, or enforcement mechanisms.

**Characteristics:**

- Advisory, not binding
- Stable but evolvable
- Context-independent
- Read for alignment, not compliance

**Primary Questions Answered:**

- What do we value?
- How do we think about good software?
- What biases should guide decisions?

**Artifacts:**

- `code/opinions/principles.md`
- Future opinionated essays or manifestos

**Authority:**

- Informational only
- Never enforced mechanically

---

## Layer 2: Governance

**What it is:**  
The mechanism by which conflicts between principles and execution are resolved.

**What it is not:**  
A manifesto, a style guide, or a task list.

**Characteristics:**

- Procedural authority
- Explicit arbitration rules
- Stable but intentionally minimal
- Applies across domains and projects

**Primary Questions Answered:**

- Who decides when principles and execution conflict?
- Where are tradeoffs made explicit?
- How is learning fed back into the system?

**Artifacts:**

- `docs/decision-arbitration.md`
- Lifecycle definitions (Praxis stages)

**Authority:**

- Binding at decision points
- Governs how commitments are made

---

## Layer 3: Execution

**What it is:**  
Concrete rules, guardrails, workflows, and practices used to produce software.

**What it is not:**  
Timeless truth or universal guidance.

**Characteristics:**

- Context-specific
- Explicitly binding
- Expected to change frequently
- Optimized for action and clarity

**Primary Questions Answered:**

- What is allowed right now?
- What constraints are active?
- How should work proceed today?

**Artifacts (future or emerging):**

- `docs/guardrails.md`
- Issue templates
- Workflow definitions
- CLAUDE.md enforcement rules
- Project-specific contracts (SODs)

**Authority:**

- Fully binding during execution
- Constrained by governance
- Informed by opinions

---

## Authority Flow

Authority flows **downward**, learning flows **upward**.

```text
Opinions
  ↓ (bias)
Governance
  ↓ (constraint)
Execution
  ↑ (learning)
```

- Opinions shape governance decisions
- Governance constrains execution
- Execution generates feedback
- Feedback updates opinions and governance over time

This loop is intentionally Deming-inspired (PDCA).

---

## Anti-Patterns This Model Prevents

- Treating principles as immutable rules
- Allowing execution to silently override intent
- Governance without theory
- Opinions without accountability
- One-size-fits-all workflows

---

## Where This Document Lives

**Recommended location:**  
`praxis/docs/layer-model.md`

Rationale:

- This is a **structural clarification**, not an opinion
- It informs how Praxis itself is understood
- It provides context for all other documents

This document should be read before:

- `decision-arbitration.md`
- Any future guardrails or workflows

---

## Status

This document is expected to be stable.

Changes should occur only when:

- The Praxis structure itself evolves
- A new layer is introduced
- Authority boundaries materially change
