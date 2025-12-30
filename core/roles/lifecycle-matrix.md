# Lifecycle Matrix
**Canonical Reference (v1.0)**

This matrix defines which roles are active, optional, or forbidden by project phase.
It merges the summary and detailed views into a single authoritative source.

## Authority
This document is **normative**. If other documents conflict with this matrix, this document wins.

## Legend
- **Primary**: Must be active; drives the phase
- **Consulted**: Available on request
- **Forbidden**: Must not be invoked in this phase

## Summary Table

| Phase | Primary Roles | Consulted Roles | Forbidden Roles |
|-------|---------------|-----------------|-----------------|
| Explore | Research Librarian, Stakeholder | Product Owner, Red Team | Architect, Developer, Scrum Master |
| Shape | Product Owner, Red Team | Research Librarian, Architect, Stakeholder, Synthesis | Developer, Scrum Master |
| Decide | Product Owner, Synthesis | Red Team, Research Librarian, Architect | Developer, Scrum Master |
| Execute | Developer, Scrum Master | Product Owner, Architect, QA, Security | Red Team, Research Librarian |
| Review | Synthesis, Product Owner, Scrum Master | Research Librarian, Red Team, Developer | — |

---

## Phase Details

### Phase 1: Explore

**Goal**: Understand the problem space without committing.

| Role | Status |
|------|--------|
| Research Librarian | Primary |
| Stakeholder / Customer Proxy | Primary |
| Product Owner | Consulted |
| Red Team | Consulted |
| Architect | Forbidden |
| Developer | Forbidden |
| Scrum Master | Forbidden |

**Constraints**:
- No solutions
- No architecture
- Output is knowledge, not plans

**Allowed artifacts**: Research notes, taxonomies
**Forbidden artifacts**: Code, architecture diagrams

---

### Phase 2: Shape

**Goal**: Form testable options and narrow scope.

| Role | Status |
|------|--------|
| Product Owner | Primary |
| Red Team | Primary |
| Research Librarian | Consulted |
| Architect | Consulted |
| Stakeholder / Customer Proxy | Consulted |
| Synthesis | Consulted |
| Developer | Forbidden |
| Scrum Master | Forbidden |

**Constraints**:
- Competing options encouraged
- No build commitment

**Allowed artifacts**: Options, tradeoff tables
**Forbidden artifacts**: Implementation code

---

### Phase 3: Decide

**Goal**: Make an explicit, accountable decision.

| Role | Status |
|------|--------|
| Product Owner | Primary (decision authority) |
| Synthesis / Editor-in-Chief | Primary (resolution authority) |
| Red Team | Consulted |
| Research Librarian | Consulted |
| Architect | Consulted |
| Developer | Forbidden |
| Scrum Master | Forbidden |

**Constraints**:
- One direction chosen
- Tradeoffs documented

**Allowed artifacts**: Decision logs, synthesis documents
**Forbidden artifacts**: New research

---

### Phase 4: Execute

**Goal**: Build a Done increment.

| Role | Status |
|------|--------|
| Developer | Primary |
| Scrum Master / Flow Facilitator | Primary |
| Product Owner | Consulted |
| Architect | Consulted |
| QA / Test Strategist | Consulted |
| Security | Consulted |
| Red Team | Forbidden |
| Research Librarian | Forbidden |

**Constraints**:
- No scope debate
- No re-litigation of decisions

**Allowed artifacts**: Code, tests, configurations
**Forbidden artifacts**: Scope documents, new options

---

### Phase 5: Review & Learn

**Goal**: Inspect outcomes and improve the system.

| Role | Status |
|------|--------|
| Synthesis / Editor-in-Chief | Primary |
| Product Owner | Primary |
| Scrum Master | Primary |
| Research Librarian | Consulted |
| Red Team | Consulted |
| Developer | Consulted |

**Constraints**:
- Update canonical knowledge
- Feed learnings back into the library

**Allowed artifacts**: Retrospectives, knowledge updates
**Forbidden artifacts**: New scope

---

## Global Rules

1. **Multiple Primary roles are allowed** per phase, but each has a distinct authority:
   - Product Owner: value and priority decisions
   - Synthesis: conflict resolution and direction-setting
   - Developer: implementation decisions
   - Scrum Master: process and flow decisions

2. **Forbidden roles may not be invoked**, even implicitly.

3. **Role changes must be explicit** — declare the new role before switching.

4. **When confused, revert to phase rules** — the matrix is the tiebreaker.

5. **Decision precedence** (when Primary roles disagree):
   - In Shape/Decide: Product Owner has final authority on "what"
   - In Execute: Developer has final authority on "how"
   - In Review: Synthesis has final authority on "what we learned"
