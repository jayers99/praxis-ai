# Formalize Stage Domain Refinement Research

<!--
metadata:
  id: spec-formalize-domains-research-2026-01-05
  title: Formalize Stage Domain Refinement Research
  date: 2026-01-05
  author: copilot-spike
  status: draft
  topic: spec
  also_relevant: [domains, lifecycle]
  keywords: [formalize, domains, creative-brief, writing-brief, learning-plan, observe, code, create, write, learn, SOD]
  consensus: medium
  epistemic_standard: thorough
  sources_count: 8
  supersedes: null
  related: [spec-lifecycle-research-2025-12-28, spec-domains-research-2025-12-28]
  approved_by: pending
  approved_date: null
-->

## Executive Summary

- Formalize stage is universal but domain-aware across all 5 Praxis domains
- All domains share the **Formalize Spine** (5 universal elements) but interpret them differently
- **Key finding:** Observe domain is pre-formalize by nature — formalization triggers domain transition
- Artifact templates needed for Create (Creative Brief), Write (Writing Brief), and Learn (Learning Plan)
- AI governance permissions vary significantly by domain at Formalize stage
- Code domain formalization (SOD) is well-established; other domains need specification

## Consensus Rating

**Medium**: Hypotheses are well-reasoned but need validation with real projects. Code domain patterns are proven; other domains are extrapolated.

## Body

### Research Questions Addressed

1. ✓ What does "formalization" mean for each domain?
2. ✓ What artifacts mark the transition from Shape → Formalize for each domain?
3. ✓ Are there domains where Formalize is optional or implicit?
4. ✓ What are the entry/exit criteria for Formalize per domain?
5. ✓ How does AI governance change at Formalize for non-Code domains?

---

### Universal Formalize Spine

Every Formalize artifact MUST explicitly define:

1. **Intent & Outcome** — Problem/thesis/creative intent, audience, success criteria, why now
2. **Scope & Boundaries** — In scope, out of scope (non-goals), assumptions, dependencies
3. **Constraints** — Domain constraints, environment overlay, privacy classification, tooling limits, time/effort caps
4. **Execution Framing** — First executable increment, risks & mitigations, open questions as explicit spikes
5. **Commit Criteria** — Success is unambiguous, scope is bounded, constraints are complete, unknowns are resolved or spiked

**Source:** [lifecycle.md](../../core/spec/lifecycle.md#5-formalize-structural-hinge)

This spine is domain-agnostic — all domains must address these elements, but each interprets them through domain-specific lenses.

---

### Domain-Specific Formalization Patterns

#### 1. Code Domain (Baseline)

**Status:** ✓ Well-established

**Formalize Artifact:** Solution Overview Document (SOD) at `docs/sod.md`

**What Formalization Means:**
- Lock intent and boundaries while remaining implementation-light
- Answer "what" and "why" without prescribing "how"
- Create policy-bearing artifact that survives privacy reclassification

**Key Characteristics:**
- Most mature and detailed formalization pattern
- Strong emphasis on technical constraints and architecture
- Explicit testing strategy required
- Balances SRS (IEEE over-formalization) and Agile (under-formalization)

**Required Sections:** 13 sections including Problem Statement, Goals/Non-Goals, Architecture, Dependencies, Risks, Acceptance Criteria, Commit Readiness

**AI Permissions:** suggest ✓, complete ✓, generate Ask, transform Ask, execute Ask

**Confidence:** HIGH — Battle-tested pattern with clear specification

**Sources:** 
- [sod.md](../../core/spec/sod.md)
- [formalize-code.md](../../core/checklists/formalize-code.md)
- IEEE SRS standards
- Shape Up (Basecamp/Ryan Singer)

---

#### 2. Create Domain

**Status:** ⚠️ Needs specification

**Formalize Artifact:** Creative Brief at `docs/brief.md`

**What Formalization Means:**
- Bound creative intent without constraining exploration prematurely
- Lock aesthetic direction, audience, and success criteria
- Define constraints (medium, format, tools, time) without prescribing exact execution
- Preserve ambiguity that invites imagination while setting clear boundaries

**Key Tension:**
> "Clarity invites action (Write) vs. ambiguity invites imagination (Create)"

The Creative Brief must formalize intent while preserving the generative ambiguity that makes creative work alive.

**Proposed Sections:**
1. Creative Intent (emotional/aesthetic response sought)
2. Audience & Context
3. Aesthetic Direction (style references, mood boards)
4. Scope & Format (medium, dimensions, deliverable format)
5. Non-Goals
6. Constraints (tools, materials, time, budget)
7. Success Criteria (what makes it "done"?)
8. First Creative Increment
9. Dependencies (materials, collaborators, approvals)
10. Open Questions
11. Commit Readiness Checklist

**Success Criteria Character:** Aesthetic, emotional, experiential (may be subjective)

**AI Permissions:** suggest ✓, complete ✓, generate ✓, transform ✓ (Create domain is permissive)

**Confidence:** MEDIUM — Extrapolated from design brief practices, needs validation

**Sources:**
- Design brief templates (AIGA, IDEO)
- Creative project management practices
- Domain boundary analysis in [domains.md](../../core/spec/domains.md)

**Open Question:** How much ambiguity should remain? Too much constraint kills creativity; too little prevents commitment.

---

#### 3. Write Domain

**Status:** ⚠️ Needs specification

**Formalize Artifact:** Writing Brief at `docs/brief.md`

**What Formalization Means:**
- Fix thesis, audience, and scope before drafting
- Lock argument structure and information architecture
- Define success criteria for clarity and impact
- Distinguish from Create: clarity invites action, not imagination

**Key Boundary:**
> "Clarity invites action (Write) vs. ambiguity invites imagination (Create)"

If primary purpose is information transfer or argumentation → Write  
If primary purpose is aesthetic/emotional response → Create  
(Note: Fiction and poetry belong to Create, not Write)

**Proposed Sections:**
1. Thesis/Central Argument
2. Audience & Context
3. Purpose & Tone (inform, persuade, entertain)
4. Scope & Boundaries
5. Information Architecture (argument structure)
6. Sources & Evidence
7. Success Criteria (clear, persuasive, complete)
8. Constraints (word count, format, deadlines, style guides)
9. Non-Goals
10. First Writing Increment
11. Dependencies (research, reviews, approvals)
12. Open Questions
13. Commit Readiness Checklist

**Success Criteria Character:** Clear, persuasive, complete (informational)

**AI Permissions:** suggest ✓, complete ✓, generate Ask, transform Ask (respect authorship)

**Confidence:** MEDIUM — Extrapolated from academic/technical writing practices, needs validation

**Sources:**
- Academic thesis/dissertation planning
- Technical writing methodologies
- Information architecture (Rosenfeld & Morville)

---

#### 4. Learn Domain

**Status:** ⚠️ Needs specification

**Formalize Artifact:** Learning Plan at `docs/plan.md` (also called "Competency Target")

**What Formalization Means:**
- Turn curiosity into directed learning with verifiable evidence
- Define competency target and success criteria
- Map learning path from current to target state
- Establish practice schedule and evidence collection

**Key Boundary:**
> "Is this for me to get better, or for others to use?"

If for internal capability formation → Learn  
If for external production → Code/Create/Write

**Proposed Sections:**
1. Learning Goal (competency being built)
2. Current State (self-assessment)
3. Target State (competency target)
4. Gap Analysis (what's missing)
5. Learning Path (sequence of topics/skills)
6. Practice Schedule (time, frequency, activities)
7. Success Criteria (how to know goal achieved)
8. Evidence Collection (artifacts proving competency)
9. Resources (books, courses, mentors, tools)
10. Constraints (time, budget, access)
11. Dependencies (prerequisites, setup)
12. First Learning Increment
13. Open Questions
14. Commit Readiness Checklist

**Success Criteria Character:** Verifiable competency, demonstrable evidence

**AI Permissions:** suggest ✓, complete ✓, generate ✓, transform ✓ (AI accelerates learning)

**Confidence:** MEDIUM — Based on instructional design and deliberate practice research

**Sources:**
- Bloom's Taxonomy (competency levels)
- Deliberate Practice (Ericsson)
- Learning objectives design (Mager)
- Competency-based education frameworks

**Open Question:** What constitutes sufficient evidence of competency? Domain-specific or universal standards?

---

#### 5. Observe Domain

**Status:** ⚠️ Special case — Needs clarification

**Formalize Artifact:** _(none required)_

**Critical Finding:** Observe is pre-formalize by nature

**Hypothesis:** Observe domain typically does NOT reach Formalize within itself. Instead:
- Observe stays in Capture/Sense/Explore stages
- Formalize triggers domain transition (promotion)
- Formalize is the domain transition moment

**Domain Transition Patterns:**
- Observe → Write: Observations become essay (Writing Brief required)
- Observe → Learn: Observations become learning goal (Learning Plan required)
- Observe → Create: Observations become creative synthesis (Creative Brief required)

**Rationale:**
- Observe is for raw capture without interpretation
- Formalization requires structure and intent
- Structure and intent mean leaving pure observation
- Therefore: Formalize = domain transition

**If Formalize Within Observe (Edge Case):**

Minimal formalization might include:
1. Observation Intent (why capturing)
2. Scope & Focus (what observing, what ignoring)
3. Collection Method (tools, frequency, format)
4. Organization Scheme (tags, metadata)
5. Boundaries (time range, topics)
6. Intended Use (future processing)
7. Success Criteria (when collection "complete")

**AI Permissions:** suggest ✓, complete ✗, generate ✗, transform ✗ (preserve authenticity)

**Confidence:** LOW — Needs further investigation and real-world testing

**Sources:**
- Zettelkasten fleeting notes (Luhmann)
- Ethnographic field notes practices
- Research capture methodologies

**Open Question:** Should Observe have any formalize artifact, or is domain transition always the formalize moment?

---

### Cross-Domain Findings

#### 1. Success Criteria Vary by Domain Nature

| Domain | Success Criteria Character |
|--------|---------------------------|
| Code | Measurable, testable, functional |
| Create | Aesthetic, emotional, experiential (may be subjective) |
| Write | Clear, persuasive, complete (informational) |
| Learn | Verifiable competency, demonstrable evidence |
| Observe | Authentic capture, retrievable storage |

#### 2. AI Governance Permissions Matrix

| Domain | suggest | complete | generate | transform | execute |
|--------|---------|----------|----------|-----------|---------|
| Code | ✓ | ✓ | Ask | Ask | Ask |
| Create | ✓ | ✓ | ✓ | ✓ | — |
| Write | ✓ | ✓ | Ask | Ask | — |
| Learn | ✓ | ✓ | ✓ | ✓ | — |
| Observe | ✓ | ✗ | ✗ | ✗ | — |

**Pattern:** Permissions align with domain purpose:
- **Code:** Cautious (ownership, avoid over-automation)
- **Create:** Permissive (generative by nature)
- **Write:** Cautious (authorship, voice preservation)
- **Learn:** Permissive (AI accelerates learning)
- **Observe:** Restrictive (preserve raw capture authenticity)

#### 3. Formalize Often Triggers Domain Transitions

**Key Pattern:** Formalize marks domain promotion:
- Observe → Write (observations → essay)
- Observe → Learn (observations → learning goal)
- Learn → Code (learning → production skill)
- Explore → Formalize (any domain locks intent)

#### 4. Universal vs Domain-Specific Elements

**Universal (All Domains):**
- Intent & Outcome
- Scope & Boundaries
- Constraints
- Execution Framing
- Commit Criteria

**Domain-Specific Interpretation Examples:**
- **Code:** "Execution Framing" = first buildable increment
- **Create:** "Execution Framing" = first creative artifact
- **Write:** "Execution Framing" = first section/chapter
- **Learn:** "Execution Framing" = first study session
- **Observe:** N/A (triggers domain transition)

---

### Entry/Exit Criteria Summary

#### Universal Entry Criteria (All Domains)

- Shape complete; direction chosen
- Single direction selected from exploration
- Scope roughed out
- Major tradeoffs resolved
- Intent can be articulated clearly

#### Universal Exit Criteria (All Domains)

- Formalize artifact exists (domain-specific)
- Intent and outcome explicitly documented
- Scope and boundaries defined (in-scope, out-of-scope)
- Constraints documented
- Success criteria defined
- First executable increment identified
- Dependencies and risks identified
- Commit readiness criteria met

#### Domain-Specific Exit Criteria Additions

**Code:**
- Technical architecture overview present
- Testing strategy defined
- Implementation constraints documented

**Create:**
- Aesthetic direction and style references captured
- Medium and format specified
- Creative constraints balanced with freedom

**Write:**
- Thesis statement clear and defensible
- Information architecture mapped
- Sources and evidence identified

**Learn:**
- Current and target competency defined
- Gap analysis complete
- Evidence collection method established

**Observe:**
- N/A — Formalize likely triggers domain transition

---

### Recommendations

#### 1. Create Formal Specifications (Priority: HIGH)

**Action:** Develop detailed specifications for:
- Creative Brief (Create domain)
- Writing Brief (Write domain)
- Learning Plan (Learn domain)

**Rationale:** These artifacts are named in `domains.md` but lack specifications like Code's SOD.

**Deliverable:** Markdown specs similar to `sod.md` in `core/spec/`

#### 2. Create Domain-Specific Checklists (Priority: MEDIUM)

**Action:** Create formalize checklist addenda:
- `formalize-create.md`
- `formalize-write.md`
- `formalize-learn.md`

**Rationale:** Each domain needs specific guidance beyond universal checklist (like `formalize-code.md` provides).

**Deliverable:** Markdown checklists in `core/checklists/`

#### 3. Clarify Observe Formalize Semantics (Priority: HIGH)

**Action:** Document in `domains.md` and `lifecycle.md`:
- Observe domain typically does NOT reach Formalize within itself
- Formalize for Observe means domain transition
- Domain transition patterns (Observe → Write/Learn/Create)

**Rationale:** Resolves ambiguity about why Observe has no formalize artifact.

**Deliverable:** Updates to `core/spec/domains.md` and `core/spec/lifecycle.md`

#### 4. Implement Template Generation (Priority: MEDIUM)

**Action:** Add templates to `src/praxis/templates/domain/`:
- `create/artifact/brief.md`
- `write/artifact/brief.md`
- `learn/artifact/plan.md`

**Rationale:** `praxis templates render --stage formalize` should generate appropriate artifacts for all domains.

**Deliverable:** Template files following existing pattern

#### 5. Validate with Real Projects (Priority: MEDIUM)

**Action:** Test formalize patterns on real Create, Write, and Learn projects.

**Rationale:** Hypotheses need validation against actual work. Current confidence is MEDIUM because patterns are extrapolated, not tested.

**Deliverable:** Worked examples and refinements based on real usage

---

### Open Questions for Further Research

1. **Observe Formalize Boundary:** Should Observe have any formalize artifact, or is domain transition always the formalize moment? Need real-world examples.

2. **Creative Brief Ambiguity Balance:** How much ambiguity should remain in a Creative Brief? Need case studies of over-constrained vs under-constrained creative projects.

3. **Learning Evidence Standards:** What constitutes sufficient evidence of competency? Should standards be domain-specific (e.g., code tests vs musical performance) or universal?

4. **Multi-Domain Projects:** How do projects spanning domains (e.g., Code + Write for documentation) handle Formalize? Single artifact or multiple?

5. **Formalize → Commit Gate Variation:** Should Commit gate criteria vary by domain, or remain universal? Code has clear go/no-go; does Create need different criteria?

---

### Follow-Up Research Stories

| Story | Priority | Size | Confidence |
|-------|----------|------|------------|
| Create Creative Brief specification | HIGH | M | MEDIUM |
| Create Writing Brief specification | HIGH | M | MEDIUM |
| Create Learning Plan specification | HIGH | M | MEDIUM |
| Document Observe domain transition pattern | HIGH | S | LOW |
| Create formalize-create.md checklist | MEDIUM | S | MEDIUM |
| Create formalize-write.md checklist | MEDIUM | S | MEDIUM |
| Create formalize-learn.md checklist | MEDIUM | S | MEDIUM |
| Implement template generation for all domains | MEDIUM | M | HIGH |
| Validate Creative Brief with real project | MEDIUM | L | N/A |
| Validate Writing Brief with real project | MEDIUM | L | N/A |
| Validate Learning Plan with real project | MEDIUM | L | N/A |

---

## Reusable Artifacts

### Formalize Artifact Quick Reference

| Domain | Artifact Name | Path | Status | Sections |
|--------|---------------|------|--------|----------|
| Code | Solution Overview Document (SOD) | `docs/sod.md` | ✓ Specified | 13 |
| Create | Creative Brief | `docs/brief.md` | ⚠️ Draft | 11 proposed |
| Write | Writing Brief | `docs/brief.md` | ⚠️ Draft | 13 proposed |
| Learn | Learning Plan | `docs/plan.md` | ⚠️ Draft | 14 proposed |
| Observe | _(none)_ | — | ⚠️ Special case | Triggers domain transition |

### AI Governance Quick Reference

Use this table when determining AI permissions at Formalize stage:

| Domain | Suggest | Complete | Generate | Transform | Rationale |
|--------|---------|----------|----------|-----------|-----------|
| Code | ✓ | ✓ | Ask | Ask | Respect ownership |
| Create | ✓ | ✓ | ✓ | ✓ | Generative by nature |
| Write | ✓ | ✓ | Ask | Ask | Respect authorship |
| Learn | ✓ | ✓ | ✓ | ✓ | AI accelerates learning |
| Observe | ✓ | ✗ | ✗ | ✗ | Preserve authenticity |

---

## Sources

### Primary (Praxis Internal)

1. [lifecycle.md](../../core/spec/lifecycle.md) — Formalize stage definition and Formalize Spine
2. [domains.md](../../core/spec/domains.md) — Domain definitions and artifact paths
3. [sod.md](../../core/spec/sod.md) — Code domain formalize artifact specification
4. [formalize.md](../../core/checklists/formalize.md) — Universal formalize checklist
5. [formalize-code.md](../../core/checklists/formalize-code.md) — Code-specific formalize checklist

### Secondary (External Frameworks)

6. IEEE Software Requirements Specification (SRS) standard — Technical formalization
7. Design brief best practices (AIGA, IDEO) — Creative formalization
8. Academic thesis/dissertation planning — Argumentative formalization
9. Bloom's Taxonomy — Learning objectives and competency levels
10. Deliberate Practice (K. Anders Ericsson) — Skill acquisition and evidence
11. Zettelkasten method (Niklas Luhmann) — Observation and capture practices
12. Shape Up (Ryan Singer/Basecamp) — Formalize as "shaping" before commitment

---

## Metadata

**Research Scope:** 5 Praxis domains × Formalize stage interaction  
**Time Investment:** ~2 hours (exceeded 60-minute time box due to depth)  
**Artifacts Created:**
- Story file: `projects/write/opinions-framework/docs/00-prerequisites/01-refine-lifecycle-research-06-formalize-domains.md`
- This research report: `research-library/spec/formalize-domains-research.md`

**Next Phase:** Specification and template creation for Create, Write, and Learn domain formalize artifacts

---

_Research conducted: 2026-01-05_  
_Status: Draft — awaiting validation with real projects_
