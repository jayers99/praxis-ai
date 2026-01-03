# Lifecycle Matrix
**Canonical Reference (v1.1)**

This matrix defines which roles are active, optional, or forbidden by project phase.
It merges the summary and detailed views into a single authoritative source.

## Authority
This document is **normative**. If other documents conflict with this matrix, this document wins.

---

## Praxis Stage-to-Phase Mapping

The Praxis lifecycle defines 9 stages. This matrix uses 5 phases that map to those stages:

| Praxis Stage | Matrix Phase | Stage Purpose |
|--------------|--------------|---------------|
| Capture | Explore | Raw idea capture |
| Sense | Explore | Initial understanding |
| Explore | Explore | Deep investigation |
| Shape | Shape | Option formation |
| **Formalize** | **Decide** | **SPINE: Commitment boundary** |
| Commit | Execute | Resource allocation |
| Execute | Execute | Building increment |
| Sustain | Review | Operational maintenance |
| Close | Review | Retrospective and archival |

### The Formalize Spine

**Formalize is the critical boundary.** No execution without formalization artifacts.

- Before Formalize: Discovery iteration ("what is this?")
- After Formalize: Refinement iteration ("how good can it be?")
- Detecting scope change during Execute → regression to Formalize

**Required artifacts by domain at Formalize:**
| Domain | Required Artifact |
|--------|-------------------|
| Code | `docs/sod.md` (Solution Overview Document) |
| Create | `docs/brief.md` |
| Write | `docs/brief.md` |
| Learn | `docs/plan.md` |
| Observe | (none required) |

---

## Legend
- **Primary**: Must be active; drives the phase
- **Consulted**: Available on request
- **Forbidden**: Must not be invoked in this phase

## Summary Table

| Phase | Praxis Stages | Primary Roles | Consulted Roles | Forbidden Roles |
|-------|---------------|---------------|-----------------|-----------------|
| Explore | Capture, Sense, Explore | Research Librarian, Stakeholder | Product Owner, Red Team | Architect, Developer, Scrum Master, FinOps, SRE |
| Shape | Shape | Product Owner, Red Team | Research Librarian, Architect, Stakeholder, Synthesis, Security | Developer, Scrum Master |
| Decide | Formalize | Product Owner, Synthesis | Red Team, Research Librarian, Architect, QA, Security, FinOps | Developer, Scrum Master |
| Execute | Commit, Execute | Developer, Scrum Master | Product Owner, Architect, QA, Security, SRE, FinOps | Red Team, Research Librarian |
| Review | Sustain, Close | Synthesis, Product Owner, Scrum Master | Research Librarian, Red Team, Developer, SRE, FinOps | — |

---

## Phase Details

### Phase 1: Explore

**Praxis Stages:** Capture, Sense, Explore

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
| Security | Forbidden |
| QA | Forbidden |
| FinOps | Forbidden |
| SRE | Forbidden |

**Constraints**:
- No solutions
- No architecture
- Output is knowledge, not plans

**Allowed artifacts**: Research notes, taxonomies, problem statements
**Forbidden artifacts**: Code, architecture diagrams, cost estimates

---

### Phase 2: Shape

**Praxis Stages:** Shape

**Goal**: Form testable options and narrow scope.

| Role | Status |
|------|--------|
| Product Owner | Primary |
| Red Team | Primary |
| Research Librarian | Consulted |
| Architect | Consulted |
| Stakeholder / Customer Proxy | Consulted |
| Synthesis | Consulted |
| Security | Consulted |
| Developer | Forbidden |
| Scrum Master | Forbidden |
| QA | Forbidden |
| FinOps | Consulted |
| SRE | Forbidden |

**Constraints**:
- Competing options encouraged
- No build commitment
- Risk assessment begins (Red Team + Security)

**Allowed artifacts**: Options, tradeoff tables, risk assessments, cost projections
**Forbidden artifacts**: Implementation code, detailed designs

---

### Phase 3: Decide

**Praxis Stages:** Formalize ← **THE SPINE**

**Goal**: Make an explicit, accountable decision. Produce formalization artifacts.

| Role | Status |
|------|--------|
| Product Owner | Primary (decision authority) |
| Synthesis / Editor-in-Chief | Primary (resolution authority) |
| Red Team | Consulted |
| Research Librarian | Consulted |
| Architect | Consulted |
| QA | Consulted |
| Security | Consulted |
| FinOps | Consulted |
| Developer | Forbidden |
| Scrum Master | Forbidden |
| SRE | Forbidden |

**Constraints**:
- One direction chosen
- Tradeoffs documented
- Formalization artifact produced (SOD, brief, or plan)
- CCR review completed before approval

**Allowed artifacts**: Decision logs, synthesis documents, SOD/brief/plan, ADRs
**Forbidden artifacts**: New research, implementation code

**Gate Requirements**:
- [ ] Formalization artifact exists and is complete
- [ ] CCR review passed (all required roles approved)
- [ ] ASR synthesis completed
- [ ] Human approval at Gate C

---

### Phase 4: Execute

**Praxis Stages:** Commit, Execute

**Goal**: Build a Done increment.

| Role | Status |
|------|--------|
| Developer | Primary |
| Scrum Master / Flow Facilitator | Primary |
| Product Owner | Consulted |
| Architect | Consulted |
| QA / Test Strategist | Consulted |
| Security | Consulted |
| SRE | Consulted |
| FinOps | Consulted |
| Red Team | Forbidden |
| Research Librarian | Forbidden |
| Stakeholder Proxy | Consulted |

**Constraints**:
- No scope debate
- No re-litigation of decisions
- Scope change detected → regression to Formalize (Decide phase)

**Allowed artifacts**: Code, tests, configurations, deployment scripts, runbooks
**Forbidden artifacts**: Scope documents, new options, new research

**Scope Change Detection**:
If during Execute the team discovers that:
- Requirements were misunderstood
- Scope needs expansion
- Technical approach is infeasible

Then: Stop work, document findings, regress to Decide phase for re-formalization.

---

### Phase 5: Review & Learn

**Praxis Stages:** Sustain, Close

**Goal**: Inspect outcomes, maintain operations, and improve the system.

| Role | Status |
|------|--------|
| Synthesis / Editor-in-Chief | Primary |
| Product Owner | Primary |
| Scrum Master | Primary |
| Research Librarian | Consulted |
| Red Team | Consulted |
| Developer | Consulted |
| SRE | Consulted |
| FinOps | Consulted |
| QA | Consulted |
| Security | Consulted |
| Architect | Consulted |
| Stakeholder Proxy | Consulted |

**Constraints**:
- Update canonical knowledge
- Feed learnings back into the library
- Capture operational insights (SRE, FinOps)
- Document security lessons learned

**Allowed artifacts**: Retrospectives, knowledge updates, post-mortems, operational runbooks
**Forbidden artifacts**: New scope, new features

**Sustain Activities**:
- Monitor SLOs and error budgets
- Track cost trends
- Maintain security posture
- Update documentation

**Close Activities**:
- Archive project artifacts
- Conduct final retrospective
- Update research library with learnings
- Close out any remaining issues

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
