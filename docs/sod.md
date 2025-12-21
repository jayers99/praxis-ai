# Solution Overview Document (SOD)

**Project:** Praxis  
**Version:** v0.1 (Draft)  
**Artifact:** sod-draft.md

---

## 1. Problem Statement

Modern AI usage is powerful but structurally weak.

Individuals working across **creative, technical, and regulated domains** face persistent challenges when attempting to use AI responsibly and repeatably:

1. **AI interactions are ad hoc and non-repeatable**  
   Prompts are created opportunistically, with little structure, no lifecycle awareness, and no consistent handoff between ideation, execution, and maintenance.

2. **Privacy and security are treated as afterthoughts**  
   Users must rely on memory and discipline to decide when to redact data, abstract inputs, switch execution targets, or avoid collaboration. This creates unacceptable risk as projects evolve in sensitivity.

3. **Environment mismatch creates friction**  
   Ideas often originate in informal or creative contexts (e.g., at home) but must later be rewritten to meet conservative, compliance-oriented work standards.

4. **No coherent end-to-end model exists for AI-assisted work**  
   Existing prompt libraries focus on isolated tasks rather than supporting the full lifecycle from raw idea to maintained deliverable.

5. **There is no policy-driven control plane for AI usage**  
   Users lack deterministic guarantees that AI collaboration, data exposure, storage, and execution targets remain aligned with a project’s evolving privacy posture.

---

## 2. Desired Outcomes

Praxis is designed to provide a **structured, enforceable system** that:

1. **Treats AI as a governed collaborator**  
   AI behavior is constrained by explicit policy and validation, not user memory or best intentions.

2. **Supports the full lifecycle of work**  
   From idea capture through long-term maintenance, with clear stage boundaries and handoffs.

3. **Allows privacy to evolve safely**  
   Projects may be reclassified at any point, with constraints tightening automatically and globally.

4. **Separates thinking from presentation**  
   Core artifacts remain environment-neutral and can be re-rendered for different contexts (e.g., home to work).

5. **Works across multiple domains**  
   Including coding, project planning, writing, learning, and illustrating.

6. **Enables local-only AI for highly sensitive work**  
   Raw data may only be used when inference is fully under user control, without reliance on cloud vendors or external telemetry.

---

## 3. Logical Structure of the Solution

### 3.1 Organizational Spine

Praxis is organized around two primary, cross-cutting dimensions that define *capability* rather than policy:

- **Domain** – the type of work being performed  
  `coding | illustrating | project-planning | learning | writing`

- **Stage** – the lifecycle position of the work  
  `collect | connect | ideate | refine | implement | maintain`

---

### 3.2 Project Control Planes

Two global control planes define *how* AI and data may be used.

#### Privacy (Mutable Project State)

Privacy represents the current security posture of a project and may change at any time:

- `public`
- `private`
- `secret` – AI interacts only with abstractions and redacted data
- `top-secret` – raw data permitted only with local or air-gapped models

Privacy reclassification applies across all domains and stages and retroactively tightens constraints on future work.

#### Execution Target

Defines where AI inference is allowed to run:

- `cloud`
- `local`
- `airgap`

**Invariant:**

```
privacy = top-secret ⇒ target = local | airgap
```

---

### 3.3 Environment as a Late-Bound Overlay

- **Environment (`env`)**: `home | work`

Environment does not affect data handling or AI permissions. Instead, it controls:

- tone and formality
- compliance posture
- formatting and presentation expectations

This allows work to originate creatively and later be rendered safely for professional contexts without rewriting core logic.

---

### 3.4 Deterministic Resolution Model

Praxis resolves AI interactions in a fixed, predictable order:

1. **Select capability**: `domain + stage`
2. **Apply constraints**: `privacy + target`
3. **Render presentation**: `env`

This model prevents unsafe defaults and ensures consistent behavior across contexts.

---

### 3.5 Policy Enforcement via CUE

Praxis uses **CUE** as its configuration and policy backbone to:

- define schemas
- enforce invariants
- unify layered policies
- validate privacy reclassification

This provides:
- validation-first behavior
- order-independent policy composition
- deterministic resolution of prompts and workflows

---

## 4. Role of the Solution Overview Document (SOD)

Within Praxis, the SOD is a **keystone artifact** that:

- translates ideation into structured intent
- survives privacy reclassification
- can be re-rendered for different environments
- feeds downstream artifacts such as spike tickets, Jira stories, and implementation plans

---

## 5. Summary

**Praxis** is a policy-driven AI workflow system that governs how ideas become maintained reality.

By combining lifecycle awareness, privacy-first governance, late-bound environment rendering, and local-only handling for highly sensitive work, Praxis enables safe, repeatable, and adaptable collaboration with AI across creative and regulated domains.
