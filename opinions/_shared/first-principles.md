---
version: "1.0"
status: active
---

# Praxis First Principles

> **Scope:** These principles apply across ALL domains and ALL lifecycle stages. They are the foundational axioms of Praxis governance.

## Core Principles

### 1. Formalize Before Execute

- **Statement:** No execution without formalization; thinking must become durable intent before action begins
- **Rationale:** AI amplifies throughput, not coherence. Without explicit formalization, speed leads to drift. The Formalize stage is the structural hinge that separates discovery from refinement.
- **Source:** Praxis lifecycle model, Aristotle (Phronesis — practical wisdom requires deliberation before action)
- **Severity:** must-have

### 2. Explicit State Over Implicit Assumption

- **Statement:** Project state (domain, stage, privacy, environment) must be explicitly declared, not inferred
- **Rationale:** Deterministic governance requires unambiguous inputs. Implicit state leads to inconsistent behavior and audit failures.
- **Source:** Praxis policy engine design
- **Severity:** must-have

### 3. Privacy as Constraint Overlay

- **Statement:** Privacy level constrains all other decisions — storage, collaboration, AI usage, artifact specificity
- **Rationale:** Privacy violations are irreversible. Conservative defaults protect against accidental exposure.
- **Source:** Praxis privacy model
- **Severity:** must-have

### 4. Small Reversible Steps Before Commitment

- **Statement:** Prefer exploration and shaping over premature commitment; keep work reversible until Formalize
- **Rationale:** Early stages should be cheap to abandon. The cost of changing direction should increase only after explicit commitment.
- **Source:** Shape Up (Basecamp), Double Diamond (British Design Council)
- **Severity:** should-have

### 5. Regression Over Failure

- **Statement:** When current stage cannot be completed, regress to an earlier stage rather than forcing forward
- **Rationale:** Gaps in earlier stages compound into larger problems. Controlled regression is cheaper than failed execution.
- **Source:** Praxis regression model, Stage-Gate (Cooper)
- **Severity:** should-have

### 6. Leverage Captured, Not Lost

- **Statement:** Close work intentionally; capture learnings and seed future cycles
- **Rationale:** Work that ends without reflection loses its compounding value. Close → Capture creates knowledge accumulation.
- **Source:** PMI Project Closure, Agile Retrospectives
- **Severity:** should-have

## AI Guidelines (All Domains)

| Operation | Permission | Notes |
|-----------|------------|-------|
| suggest | Allowed | AI may always propose; human decides |
| complete | Varies | Domain-specific; blocked in Observe |
| generate | Varies | Requires explicit approval in most domains |
| transform | Varies | Higher risk; domain-specific rules apply |
| execute | Ask | Never without explicit human approval |
| publish | Ask | Privacy level must permit; human confirms |

## Anti-Patterns (All Domains)

### Skipping Stages

- **What:** Jumping directly to Execute without Formalize
- **Why bad:** No scope lock means unbounded work; no success criteria means no completion
- **Instead:** Progress through stages; use lightweight artifacts if scope is small

### Privacy Afterthought

- **What:** Deciding privacy level after artifacts exist
- **Why bad:** Sensitive material may already be exposed; reclassification is expensive
- **Instead:** Declare privacy at project inception or Explore stage

### Infinite Sustain

- **What:** Staying in Sustain indefinitely without closing or iterating
- **Why bad:** Prevents reflection; accumulates maintenance burden; blocks new work
- **Instead:** Periodically evaluate: close, iterate (new Formalize), or continue Sustain with explicit decision

### Solo Context Syndrome

- **What:** All project knowledge exists only in one person's (or AI session's) head
- **Why bad:** No handoff possible; knowledge lost on context switch
- **Instead:** Externalize key decisions in stage artifacts; use formalization documents

## The Praxis Equation

Behavior is determined by the composition of four dimensions:

```
Domain + Stage + Privacy + Environment → Behavior
```

This resolution is:
- **Deterministic:** Same inputs produce same outputs
- **Auditable:** Each dimension is explicit and logged
- **Composable:** Dimensions combine without order dependency

## Philosophical Roots

These principles trace to classical philosophy:

| Concept | Origin | Praxis Implementation |
|---------|--------|----------------------|
| Praxis | Aristotle | Purposeful action (Execute, Sustain) |
| Phronesis | Aristotle | Practical wisdom (Policy Engine) |
| Akrasia | Aristotle | Weakness of will — what AI amplifies; Formalize defends |
| Divided Line | Plato | Knowledge stages (Capture → Execute progression) |
| Elenchus | Socrates | Testing assumptions (Red Team, validation) |

---

*Last updated: 2026-01-01*
