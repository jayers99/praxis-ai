---
domain: code
version: "1.0"
status: draft
---

# Code Domain Principles

> **Scope:** These principles apply across ALL lifecycle stages for Code projects.

## Core Principles

### 1. Design for Feedback

- **Statement:** Structure systems, code, and processes so that incorrect assumptions are revealed early, cheaply, and clearly
- **Rationale:** Fast feedback loops enable rapid iteration and reduce cost of mistakes
- **Source:** Deming (PDCA), Farley (Modern Software Engineering), Beck (TDD)
- **Severity:** must-have

### 2. Work in Small, Reversible Increments

- **Statement:** Prefer small batches and safe-to-fail experiments over large speculative commitments
- **Rationale:** Small changes are easier to understand, test, review, and roll back
- **Source:** Continuous Delivery (Farley), Shape Up (Basecamp)
- **Severity:** must-have

### 3. Optimize for Change

- **Statement:** Design systems that are easy to change over systems that merely appear complete
- **Rationale:** Requirements evolve; rigid code becomes legacy
- **Source:** Clean Architecture (Martin), Refactoring (Fowler)
- **Severity:** must-have

### 4. Make Behavior Explicit

- **Statement:** Prefer explicit behavior over implicit intent; use tests to express and verify intent
- **Rationale:** Implicit code is harder to understand and maintain
- **Source:** TDD (Beck), Clean Code (Martin)
- **Severity:** should-have

### 5. Continuously Refactor

- **Statement:** Improve design quality through ongoing behavior-preserving refactoring
- **Rationale:** Without refactoring, code quality degrades over time
- **Source:** Refactoring (Fowler), TDD (Beck)
- **Severity:** should-have

## AI Guidelines (All Stages)

| Operation | Permission | Notes |
|-----------|------------|-------|
| suggest | Allowed | Always permitted for code suggestions |
| complete | Allowed | In-context completion permitted |
| generate | Ask | User approval for new files/modules |
| transform | Ask | Refactoring needs approval |
| execute | Ask | Never run without explicit approval |

## Anti-Patterns (All Stages)

### Premature Optimization

- **What:** Optimizing before measuring
- **Why bad:** Wastes effort on non-bottlenecks, adds complexity
- **Instead:** Profile first, optimize where it matters

### Cargo Cult Programming

- **What:** Copying patterns without understanding
- **Why bad:** Creates fragile, unmaintainable code
- **Instead:** Understand before applying

### Big Bang Delivery

- **What:** Building large features before getting feedback
- **Why bad:** High risk of building wrong thing; expensive to change
- **Instead:** Tracer bullets, MVPs, continuous delivery

### Clever Over Clear

- **What:** Optimizing for brevity or cleverness over readability
- **Why bad:** Future maintainers (including yourself) struggle to understand
- **Instead:** Prefer clear, boring code that's easy to change

## Influential Lineage

These principles draw from:

| Author | Key Contribution |
|--------|------------------|
| W. Edwards Deming | Systems thinking, PDCA, continuous improvement |
| Dave Farley | Fast feedback, continuous delivery, small batches |
| Kent Beck | TDD, red-green-refactor, tests as design |
| Martin Fowler | Refactoring, patterns, design quality |
| Eric Evans | Domain-driven design, ubiquitous language |
| Robert C. Martin | Clean code, SOLID principles, boundaries |

## Productive Tensions

These tensions are intentional and resolved contextually:

- Feedback vs. commitment
- Cleanliness vs. speed
- Deep modeling vs. incremental delivery
- Theory vs. pragmatism
- Reuse vs. simplicity

---

*Last updated: 2025-12-28*
