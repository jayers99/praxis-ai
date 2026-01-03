# Praxis Roles Subsystem Analysis Report

**Date:** 2026-01-02
**Status:** Analysis Complete (Revised)
**Scope:** `praxis-ai/core/roles/` directory and related research

---

## Executive Summary

The Praxis Roles subsystem is a **normative control surface** for solo + AI execution. It defines 12 roles across two tiers (Core and Supporting), with governance documents controlling lifecycle phase activation, invocation syntax, kickback standards, and agent prompts.

**Key Findings:**
- The architecture is sound and well-grounded in established frameworks (Scrum, Agile, psychological safety research)
- All 12 roles are now at v1.1 with full CCR review sections and collaboration notes
- The lifecycle matrix uses a 5-phase model that doesn't explicitly map to Praxis's 9-stage lifecycle
- Strong foundation for AI agent integration exists but isn't connected to Praxis CLI

---

## 1. System Architecture

### 1.1 Role Taxonomy

The system defines 12 roles in two tiers:

#### Core Roles (Always Active)

| # | Role | Purpose | Version |
|---|------|---------|---------|
| 00 | Research Librarian | Epistemic backbone; curates truth and provenance | v1.1 |
| 01 | Product Owner | Value decisions; backlog ordering | v1.1 |
| 02 | Red Team | Constructive adversarial validation | v1.1 |
| 03 | Synthesis | Resolves inputs into single direction; performs ASR | v1.1 |
| 04 | Scrum Master | Cadence, flow, impediment removal | v1.1 |
| 05 | Developer | Produces "Done" increments | v1.1 |

#### Supporting Roles (Invoked as Needed)

| # | Role | Purpose | Version |
|---|------|---------|---------|
| 06 | Stakeholder Proxy | User needs and acceptance language | v1.1 |
| 07 | Architect | Coherence and boundaries | v1.1 |
| 08 | Security | Threats, controls, mitigations | v1.1 |
| 09 | QA | Risk-based validation strategy | v1.1 |
| 10 | FinOps | Cost drivers and constraints | v1.1 |
| 11 | SRE | Operability, SLOs, monitoring | v1.1 |

### 1.2 Governance Documents

| Document | Purpose | Status |
|----------|---------|--------|
| `index.md` | Canonical entry point | Complete |
| `README.md` | Layer description and authority | Complete |
| `lifecycle-matrix.md` | Phase → role mapping (Primary/Consulted/Forbidden) | Needs alignment |
| `invocation-syntax.md` | Grammar for role activation | Complete |
| `kickback-rubrics.md` | Structured rejection standards | Complete |
| `system-prompt-bundle.md` | Agent prompts for each role | Complete |

### 1.3 Three-Layer Separation

The roles subsystem follows a deliberate architectural separation:

| Layer | Location | Purpose | Stability |
|-------|----------|---------|-----------|
| **Core** | `core/roles/` | Normative definitions | Stable, versioned |
| **Research** | `research-library/roles/` | Explanatory rationale | Expansive, non-binding |
| **Handoff** | `handoff/roles/` | Operational instructions | Evolves with work |

**Rationale:** This separation ensures the system remains governable. Core is the policy surface; Research explains decisions without destabilizing operations; Handoff provides execution context.

---

## 2. Lifecycle Matrix Analysis

### 2.1 Current Phase Model

The `lifecycle-matrix.md` defines 5 phases:

| Phase | Goal | Primary Roles | Forbidden Roles |
|-------|------|---------------|-----------------|
| **Explore** | Understand problem space | Research Librarian, Stakeholder | Architect, Developer, Scrum Master |
| **Shape** | Form testable options | Product Owner, Red Team | Developer, Scrum Master |
| **Decide** | Make explicit decision | Product Owner, Synthesis | Developer, Scrum Master |
| **Execute** | Build Done increment | Developer, Scrum Master | Red Team, Research Librarian |
| **Review** | Inspect and improve | Synthesis, Product Owner, Scrum Master | — |

### 2.2 Misalignment with Praxis Lifecycle

Praxis defines 9 lifecycle stages:

```
Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain → Close
```

The 5-phase matrix doesn't explicitly map to these stages. Proposed alignment:

| Praxis Stage(s) | Matrix Phase | Notes |
|-----------------|--------------|-------|
| Capture, Sense, Explore | Explore | Discovery and understanding |
| Shape | Shape | Option formation |
| Formalize | Decide | Commitment point (Formalize spine) |
| Commit, Execute | Execute | Building phase |
| Sustain, Close | Review | Operational and retrospective |

**Gap:** The Formalize stage is the critical "spine" in Praxis (no execution without formalization artifacts). This isn't reflected in the current matrix.

### 2.3 Artifact Constraints by Phase

The matrix defines allowed/forbidden artifacts:

| Phase | Allowed | Forbidden |
|-------|---------|-----------|
| Explore | Research notes, taxonomies | Code, architecture diagrams |
| Shape | Options, tradeoff tables | Implementation code |
| Decide | Decision logs, synthesis docs | New research |
| Execute | Code, tests, configs | Scope documents, new options |
| Review | Retrospectives, knowledge updates | New scope |

---

## 3. Role Definition Analysis

### 3.1 Version Distribution

| Version | Count | Roles |
|---------|-------|-------|
| v1.1 | 12 | All roles (Research Librarian, Product Owner, Red Team, Synthesis, Scrum Master, Developer, Stakeholder Proxy, Architect, Security, QA, FinOps, SRE) |

### 3.2 Structural Completeness

All 12 roles are now at v1.1 and include:
- Inputs section
- Outputs section
- Guardrails
- **CCR review section** (Issue Draft Review with checklist)
- **Collaboration notes**
- Kickback triggers (general + issue review)

### 3.3 CCR (Concurrent Code Review) Integration

All 12 roles now have full CCR integration:

| Role | Review Focus | Output Format |
|------|--------------|---------------|
| Research Librarian | Evidence quality, citation completeness, consensus clarity | APPROVE / KICKBACK / SUGGEST |
| Product Owner | Value clarity, scope discipline, strategic alignment | APPROVE / KICKBACK / SUGGEST |
| Red Team | Risk blindspots, untested assumptions, disconfirming evidence | APPROVE / KICKBACK / SUGGEST |
| Synthesis | Conflict resolution, tradeoff clarity, decision coherence | APPROVE / KICKBACK / SUGGEST |
| Scrum Master | Sizing, sequencing, workflow hygiene | APPROVE / KICKBACK / SUGGEST |
| Developer | Technical feasibility, scope clarity | APPROVE / KICKBACK / SUGGEST |
| Stakeholder Proxy | User language grounding, JTBD clarity | APPROVE / KICKBACK / SUGGEST |
| Architect | System coherence, boundaries, NFRs | APPROVE / KICKBACK / SUGGEST |
| Security | Threat implications, trust boundaries | APPROVE / KICKBACK / SUGGEST |
| QA | Acceptance criteria quality, BDD format | APPROVE / KICKBACK / SUGGEST |
| FinOps | Cost implications, scale analysis, ROI justification | APPROVE / KICKBACK / SUGGEST |
| SRE | Operability, SLO implications, monitoring gaps | APPROVE / KICKBACK / SUGGEST |

### 3.4 ASR (Adjudicated Synthesis & Resolution)

The Synthesis role performs ASR after CCR reviews:

1. **Collect** — Gather all CCR role outputs
2. **Identify conflicts** — Note where roles disagree
3. **Weigh tradeoffs** — Consider value, risk, feasibility
4. **Adjudicate** — Make binding decisions
5. **Synthesize** — Produce consolidated output
6. **Hand off** — Deliver to human for Gate C review

**Adjudication Principles:**
1. Safety first — Security KICKBACK generally wins
2. Value clarity — PO concerns take precedence
3. Feasibility matters — Developer KICKBACK requires scope adjustment
4. Architecture coherence — Architect concerns shouldn't be dismissed
5. Quality gates — QA KICKBACK on testability must be addressed
6. Explicit tradeoffs — Never hide what was sacrificed

---

## 4. Invocation System

### 4.1 Syntax

Formal syntax:
```
[ROLE: Research Librarian]
[PHASE: Explore]
[PRIMARY]
```

Optional modifiers:
- `[CONSULTED]`
- `[FORBIDDEN]`
- `[TIMEBOX: 30 minutes]`
- `[VERBOSITY: low|medium|high]`

Shorthand:
```
You are the Product Owner role. Phase: Decide.
```

### 4.2 Rules

- Multiple PRIMARY roles allowed per phase (with distinct authorities)
- Forbidden roles may not be invoked, even implicitly
- Phase must always be declared
- Role changes must be explicit

### 4.3 Decision Precedence

When PRIMARY roles disagree:
- **Shape/Decide:** Product Owner has final authority on "what"
- **Execute:** Developer has final authority on "how"
- **Review:** Synthesis has final authority on "what we learned"

---

## 5. Kickback System

### 5.1 Universal Template

All kickbacks must include:
1. **What failed** — Specific output that didn't meet standards
2. **What is missing** — Required elements not present
3. **Standard not met** — Reference to violated requirement
4. **Direction for revision** — Concrete next steps
5. **Effort cap** — Maximum time/tokens for revision

### 5.2 Role-Specific Triggers

| Role | Key Kickback Triggers |
|------|----------------------|
| Research Librarian | Missing sources, unclear consensus, excess verbosity |
| Product Owner | No decision stated, tradeoffs hidden, scope creep |
| Red Team | Vague risks, no evidence, blocking without alternative |
| Synthesis | Ambiguity remains, reopened closed debate, hidden tradeoffs |
| Developer | Acceptance criteria unmet, validation missing, scope expanded |
| Scrum Master | Blockers not identified, impediments untracked |
| Stakeholder Proxy | User needs ungrounded, JTBD vague |
| Architect | ADR missing, boundaries unclear, over-design |
| QA | No risk prioritization, high-risk scenarios not enumerated |
| Security | Threat model incomplete, mitigations unmapped |
| FinOps | Cost drivers unquantified, optimization levers missing |
| SRE | SLOs undefined, monitoring plan missing |

---

## 6. System Prompt Bundle

Each role has a ready-to-use agent prompt in `system-prompt-bundle.md`:

### 6.1 Prompt Structure

```
You are the [Role] role. Your purpose is to [purpose statement].

You must produce:
- [Required output 1]
- [Required output 2]

You may NOT:
- [Prohibited action 1]
- [Prohibited action 2]
```

### 6.2 Example: QA Role Prompt

```
You are the QA role. Your purpose is to prevent regressions through
risk-based validation and ensure acceptance criteria quality before
formalization.

Reference: research-library/patterns/tdd-bdd-ai-verification.md

You must produce:
- Test strategy (what to test, how, why)
- High-risk scenarios enumerated
- For ticket review: APPROVE / KICKBACK / SUGGEST verdict

For pre-formalization ticket review, check:
1. Acceptance criteria in Given-When-Then format
2. Declarative scenarios (behavior, not UI steps)
3. One behavior per scenario
4. Edge cases and error paths covered

You may NOT:
- Demand 100% coverage without justification
- Skip risk prioritization
- Approve tickets missing acceptance criteria for high-risk features
```

---

## 7. Research Foundation

### 7.1 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| "Roles" not "Hats" | Conveys accountability and authority; aligns with Scrum; scales beyond metaphor |
| Core/Research/Handoff split | Stable policy surface + expansive explanation + operational execution |
| Phase-gated activation | Prevents premature optimization and scope creep |
| Structured dissent | Red Team + Synthesis institutionalize disagreement constructively |

### 7.2 Theoretical Grounding

Sources cited in rationale:
1. The 2020 Scrum Guide (Schwaber & Sutherland)
2. Scrum.org: Accountability vs Roles
3. Agile Manifesto and 12 Principles
4. Amy Edmondson: Psychological Safety
5. Daniel Kahneman: Adversarial Collaboration
6. UPenn Adversarial Collaboration Project

### 7.3 Team Health Principles

1. **Clear decision rights** — Roles isolate authority, avoid consensus traps
2. **Short learning loops** — Agile principles reward frequent delivery
3. **Psychological safety with structured dissent** — Disagreement is institutionalized
4. **Adversarial collaboration** — Challenge becomes co-designed tests, not ego conflicts

---

## 8. Gap Analysis

### 8.1 Structural Gaps

| Gap | Severity | Impact |
|-----|----------|--------|
| ~~6 roles at v1.0 (no CCR)~~ | ~~Medium~~ | **RESOLVED** - All 12 roles now at v1.1 |
| Lifecycle matrix misalignment | Medium | Confusion about stage mapping |
| No CLI integration | Low | Manual invocation only |
| No subagent mapping | Low | Roles exist but aren't automated |

### 8.2 Content Gaps

**RESOLVED** - All roles now have CCR sections and collaboration notes.

| Role | Status |
|------|--------|
| All 12 roles | Complete at v1.1 |

### 8.3 Integration Gaps

| Integration Point | Current State | Desired State |
|-------------------|---------------|---------------|
| Praxis CLI | None | `praxis role invoke <role> <phase>` |
| Subagents | Conceptual link | Explicit role → subagent mapping |
| Domain variants | Code-centric | Domain-adapted roles (Create, Write, Learn) |

---

## 9. Recommendations

### 9.1 High Priority

#### 9.1.1 Align Lifecycle Matrix with Praxis Stages

Create explicit mapping between 5-phase matrix and 9-stage lifecycle:

```markdown
## Stage-to-Phase Mapping

| Praxis Stage | Matrix Phase | Formalize Boundary |
|--------------|--------------|-------------------|
| Capture | Explore | — |
| Sense | Explore | — |
| Explore | Explore | — |
| Shape | Shape | — |
| Formalize | Decide | ← SPINE (no execution without artifacts) |
| Commit | Execute | — |
| Execute | Execute | — |
| Sustain | Review | — |
| Close | Review | — |
```

#### 9.1.2 ~~Upgrade v1.0 Roles to v1.1~~ (COMPLETED)

**Status:** All 12 roles have been upgraded to v1.1 with full CCR review sections and collaboration notes. Each role now includes:

- CCR review section with role-specific focus areas
- Collaboration notes defining inter-role coordination
- Complete kickback triggers (general + issue review)

### 9.2 Medium Priority

#### 9.2.1 Role Composition Patterns

Document common role combinations:

| Pattern | Roles | Use Case |
|---------|-------|----------|
| Security Review | Security + Architect | Trust boundary changes |
| Feasibility Check | Developer + Architect | Technical approach validation |
| User Validation | Stakeholder Proxy + QA | Acceptance criteria quality |
| Cost-Value Analysis | FinOps + Product Owner | Investment decisions |

#### 9.2.2 CLI Integration

Add role invocation to Praxis CLI:

```bash
praxis role list                    # List all roles
praxis role invoke developer execute  # Invoke role in phase
praxis role matrix                  # Show lifecycle matrix
praxis role prompt <role>           # Output system prompt
```

#### 9.2.3 Subagent Integration

Map roles to subagent definitions:

| Role | Subagent | Invocation |
|------|----------|------------|
| Research Librarian | researcher | `[SUBAGENT: researcher]` |
| Red Team | red-team | `[SUBAGENT: red-team]` |
| QA | qa-reviewer | `[SUBAGENT: qa-reviewer]` |

### 9.3 Lower Priority

#### 9.3.1 Domain-Specific Role Variants

| Domain | Role Adaptation |
|--------|-----------------|
| Create | Developer → Maker; Architect → Creative Director |
| Write | Developer → Author; QA → Editor |
| Learn | Developer → Practitioner; QA → Assessor |

#### 9.3.2 Metrics and Feedback

Track role effectiveness:
- Kickback frequency by role
- Time-to-resolution after kickback
- Role invocation patterns by phase

---

## 10. Implementation Roadmap

### Phase 1: Alignment (1-2 sessions)

- [ ] Update `lifecycle-matrix.md` with stage mapping
- [ ] Add Formalize spine notation
- [ ] Document stage → phase translation rules

### Phase 2: Role Upgrades ~~(3-5 sessions)~~ (COMPLETED)

- [x] Upgrade Research Librarian to v1.1
- [x] Upgrade Red Team to v1.1
- [x] Upgrade Stakeholder Proxy to v1.1
- [x] Upgrade FinOps to v1.1
- [x] Upgrade SRE to v1.1
- [x] Add collaboration notes to QA

### Phase 3: Integration (2-3 sessions)

- [ ] Design CLI role commands
- [ ] Implement `praxis role` command group
- [ ] Create subagent mapping document

### Phase 4: Extension (ongoing)

- [ ] Document role composition patterns
- [ ] Create domain variants for Create/Write/Learn
- [ ] Add metrics collection hooks

---

## 11. Related Work in research-library/roles

Supporting research has been cataloged to `praxis-ai/research-library/roles/`:

| File | Topic |
|------|-------|
| `scrum-master-role.md` | Scrum Master deep dive |
| `lead-software-developer-scrum-role.md` | Developer role research |
| `security-engineer-scrum-role.md` | Security role research |
| `software-architect-role-scrum-dora-analysis.md` | Architect DORA analysis |
| `software-architect-scrum-role.md` | Architect Scrum research |
| `qa-engineer-role-scrum-dora-analysis.md` | QA DORA analysis |
| `synthesis-role.md` | Synthesis role research |
| `sre-role.md` | SRE role research |
| `dora-team-roles-critical-success.md` | DORA metrics and roles |
| `dora-refinement-peer-review-roles.md` | Refinement workflow |
| `scrum-team-roles-comprehensive.md` | Comprehensive Scrum team analysis |
| `agile-shared-responsibility-ai-context-memory.md` | AI context considerations |
| `multi-agent-role-specialization-context-mitigation.md` | Multi-agent patterns |

---

## 12. Conclusion

The Praxis Roles subsystem provides a solid foundation for structured human-AI collaboration. The Core/Research/Handoff separation, phase-gated activation, and kickback rubrics create a governable system.

**Status Update (2026-01-02):** All 12 roles have been upgraded to v1.1, resolving the previously identified version inconsistency gap.

**Remaining priorities:**
1. Align the lifecycle matrix with Praxis's 9-stage model
2. ~~Upgrade the 6 v1.0 roles to v1.1 with CCR sections~~ (COMPLETED)
3. Document the Formalize spine as the critical decision boundary
4. Implement CLI integration for role invocation
5. Create subagent mapping for automated role execution

**The system's greatest strength** is its structured approach to dissent (Red Team + Synthesis), which prevents both groupthink and analysis paralysis.

**The system's current state** shows consistent role maturity across all 12 definitions at v1.1, with full CCR integration and collaboration notes.

---

*Report generated: 2025-01-02*
*Revised: 2026-01-02 (version verification and updates)*
*Source: `praxis-ai/core/roles/` analysis*
