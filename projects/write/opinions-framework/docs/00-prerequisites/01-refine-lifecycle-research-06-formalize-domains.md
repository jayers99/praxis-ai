# Spike: Refine Formalize Stage Across All Domains

**Date:** 2026-01-05  
**Status:** In Progress  
**Time Box:** 60 minutes  
**Credit Budget:** ~50 queries  
**Domain:** Write  
**Related Issue:** [Spike] Refine Formalize Stage Across All Domains

---

## Spike Intent

Research how the **Formalize** stage applies differently across all 5 domains. Formalize is the "structural hinge" — but what does formalization look like for Create, Write, Learn, and Observe (not just Code)?

---

## Research Questions

1. What does "formalization" mean for each domain?
2. What artifacts mark the transition from Shape → Formalize for each domain?
3. Are there domains where Formalize is optional or implicit?
4. What are the entry/exit criteria for Formalize per domain?
5. How does AI governance change at Formalize for non-Code domains?

---

## Background Context

From lifecycle research, Formalize is defined as:
> "Convert shaped thinking into durable, policy-bearing artifacts. Establishes scope, constraints, success criteria."

### Formalize Spine (Universal Elements)

Every Formalize artifact MUST explicitly define:

1. **Intent & Outcome** — Problem/thesis/creative intent, audience, success criteria, why now
2. **Scope & Boundaries** — In scope, out of scope (non-goals), assumptions, dependencies
3. **Constraints** — Domain constraints, environment overlay, privacy classification, tooling limits, time/effort caps
4. **Execution Framing** — First executable increment, risks & mitigations, open questions as explicit spikes
5. **Commit Criteria** — Success is unambiguous, scope is bounded, constraints are complete, unknowns are resolved or spiked

### Current Artifact Mappings (from domains.md)

| Domain | Artifact Name | Path | Current Status |
|--------|---------------|------|----------------|
| Code | Solution Overview Document (SOD) | `docs/sod.md` | ✓ Well-defined |
| Create | Creative Brief | `docs/brief.md` | ? Draft status |
| Write | Writing Brief | `docs/brief.md` | ? Draft status |
| Learn | Learning Plan | `docs/plan.md` | ? Draft (called "Competency Target" in some places) |
| Observe | _(none)_ | — | Observe is pre-Formalize by nature |

---

## Domain Analysis

### 1. Code Domain

**Status:** ✓ Well-established baseline

**Formalize Artifact:** Solution Overview Document (SOD) at `docs/sod.md`

**What Formalization Means:**
- Lock intent and boundaries while remaining implementation-light
- Answer "what" and "why" without prescribing "how"
- Create policy-bearing artifact that survives privacy reclassification

**Entry Criteria:**
- Shape complete; direction chosen
- Single direction chosen from multiple options
- Scope roughed out
- Major tradeoffs resolved

**Exit Criteria:**
- SOD exists with scope and constraints
- SOD includes success criteria
- Intent is explicit and documented
- Boundaries are clearly defined
- Technical architecture overview present
- Implementation technologies and constraints identified
- Testing strategy defined (unit, integration, acceptance)

**Key SOD Sections:**
1. Problem Statement
2. Business Context / Drivers
3. Goals & Non-Goals
4. Functional Overview
5. High-Level Architecture / Workflow
6. Assumptions & Constraints
7. Dependencies
8. Phases / Increments
9. Risks & Mitigations
10. Open Questions / Spikes
11. Glossary / Definitions
12. Gherkin Specification / Acceptance Criteria
13. Commit Readiness Checklist

**AI Governance at Formalize:**
- `suggest`: Allowed
- `complete`: Allowed
- `generate`: Ask (requires permission)
- `transform`: Ask (requires permission)
- `execute`: Ask (requires permission)

**Special Characteristics:**
- Most mature and detailed formalization pattern
- Strong emphasis on technical constraints and architecture
- Explicit testing strategy required
- Balances SRS (over-formalized) and Agile (under-formalized)

---

### 2. Create Domain

**Status:** ⚠️ Needs refinement

**Formalize Artifact:** Creative Brief at `docs/brief.md`

**What Formalization Means (Hypothesis):**
- Bound creative intent without constraining exploration prematurely
- Lock aesthetic direction, audience, and success criteria
- Define constraints (medium, format, tools, time) without prescribing exact execution
- Preserve ambiguity that invites imagination while setting clear boundaries

**Subtypes:**
- `create.visual` — Static images, illustrations, graphics
- `create.audio` — Music, sound design, podcasts
- `create.video` — Film, animation, motion graphics
- `create.interactive` — Games, installations, experiences
- `create.generative` — AI-generated or algorithmic art
- `create.design` — UI/UX, product design, crafts

**Entry Criteria (Proposed):**
- Creative direction chosen from exploration
- Aesthetic intent can be articulated
- Medium/format selected
- Audience identified
- Major creative tradeoffs resolved

**Exit Criteria (Proposed):**
- Creative Brief exists
- Creative intent and aesthetic direction documented
- Audience and context defined
- Success criteria defined (what makes it "done"?)
- Constraints documented (medium, tools, time, budget)
- Non-goals explicit (what this is NOT)
- First creative increment defined
- Style references or mood boards captured
- Dependencies identified (materials, collaborators, tools)

**Proposed Creative Brief Sections:**
1. **Creative Intent** — What emotional/aesthetic response are you seeking?
2. **Audience & Context** — Who experiences this? Where/how?
3. **Aesthetic Direction** — Visual/sonic/spatial qualities, style references
4. **Scope & Format** — Medium, dimensions, duration, deliverable format
5. **Non-Goals** — What this explicitly is NOT
6. **Constraints** — Tools, materials, time, budget, technical limits
7. **Success Criteria** — What makes this "done"? How will you know it succeeded?
8. **First Creative Increment** — What's the first concrete artifact to create?
9. **Dependencies** — Materials, collaborators, access, approvals
10. **Open Questions** — Unresolved creative decisions, spikes needed
11. **Commit Readiness** — Is creative direction locked? Are resources available?

**AI Governance at Formalize:**
- `suggest`: Allowed
- `complete`: Allowed
- `generate`: Allowed (Create domain is permissive for AI generation)
- `transform`: Allowed
- `execute`: Not applicable

**Special Characteristics:**
- Balance between constraint and creative freedom
- Aesthetic qualities are harder to formalize than functional requirements
- Success criteria may be subjective/emotional rather than measurable
- "Ambiguity invites imagination" — preserve intentional ambiguity
- Style references and mood boards are formalization tools

**Key Tension:**
> "Clarity invites action (Write) vs. ambiguity invites imagination (Create)"

The Creative Brief must formalize intent while preserving the generative ambiguity that makes creative work alive.

---

### 3. Write Domain

**Status:** ⚠️ Needs refinement

**Formalize Artifact:** Writing Brief at `docs/brief.md`

**What Formalization Means (Hypothesis):**
- Fix thesis, audience, and scope before drafting
- Lock argument structure and information architecture
- Define success criteria for clarity and impact
- Distinguish from Create: clarity invites action, not imagination

**Subtypes:**
- `write.technical` — Documentation, tutorials, specs
- `write.business` — Reports, proposals, memos
- `write.narrative` — Essays, personal stories (not fiction)
- `write.academic` — Research papers, theses
- `write.journalistic` — Articles, news, long-form journalism

**Note:** Fiction and poetry belong to Create domain, not Write.

**Entry Criteria (Proposed):**
- Thesis or central argument identified
- Audience and context understood
- Argument structure roughed out
- Sources/research gathered
- Purpose and tone chosen

**Exit Criteria (Proposed):**
- Writing Brief exists
- Thesis statement clear and defensible
- Audience and publication context defined
- Scope and boundaries explicit
- Success criteria defined (clarity, persuasiveness, completeness)
- Information architecture mapped
- Sources and citations identified
- First writing increment defined
- Dependencies identified (research, reviews, approvals)

**Proposed Writing Brief Sections:**
1. **Thesis/Central Argument** — What is the core claim or message?
2. **Audience & Context** — Who reads this? Where/how is it published?
3. **Purpose & Tone** — Inform? Persuade? Entertain? Formal/casual?
4. **Scope & Boundaries** — What's covered? What's explicitly excluded?
5. **Information Architecture** — How is the argument structured?
6. **Sources & Evidence** — What research supports this?
7. **Success Criteria** — Clear? Persuasive? Complete? How will you know?
8. **Constraints** — Word count, format, publication deadlines, style guides
9. **Non-Goals** — What this is NOT trying to accomplish
10. **First Writing Increment** — What section/chapter/draft comes first?
11. **Dependencies** — Research needed, expert review, approvals
12. **Open Questions** — Unresolved arguments, research gaps
13. **Commit Readiness** — Is thesis locked? Is structure sound?

**AI Governance at Formalize:**
- `suggest`: Allowed
- `complete`: Allowed
- `generate`: Ask (requires permission — respects authorship)
- `transform`: Ask (requires permission)
- `execute`: Not applicable

**Special Characteristics:**
- Emphasis on thesis clarity and argumentative rigor
- Information architecture is structural formalization
- Sources and citations are constraints
- Success criteria emphasize clarity over subjective aesthetics
- Distinguishes informational (Write) from aesthetic (Create) intent

**Boundary with Create Domain:**
> "Clarity invites action (Write) vs. ambiguity invites imagination (Create)"

If the primary purpose is information transfer or argumentation → Write.  
If the primary purpose is aesthetic/emotional response → Create.

---

### 4. Learn Domain

**Status:** ⚠️ Needs refinement

**Formalize Artifact:** Learning Plan at `docs/plan.md` (also called "Competency Target" in lifecycle.md)

**What Formalization Means (Hypothesis):**
- Turn curiosity into directed learning with verifiable evidence
- Define competency target and success criteria
- Map learning path from current to target state
- Establish practice schedule and evidence collection

**Subtypes:**
- `learn.skill` — Procedural knowledge, how-to
- `learn.concept` — Theoretical understanding, mental models
- `learn.practice` — Exercises, drills, deliberate practice
- `learn.course` — Structured learning path
- `learn.exploration` — Self-directed discovery

**Entry Criteria (Proposed):**
- Learning goal identified
- Current competency level understood
- Target competency level defined
- Learning resources identified
- Time commitment estimated

**Exit Criteria (Proposed):**
- Learning Plan exists
- Current and target competency clearly defined
- Gap analysis complete
- Learning path mapped (sequence of topics/skills)
- Practice schedule defined
- Success criteria and evidence collection method identified
- Resources identified (courses, books, mentors, tools)
- First learning increment defined
- Dependencies identified (prerequisites, access, time)

**Proposed Learning Plan Sections:**
1. **Learning Goal** — What competency am I building?
2. **Current State** — Where am I now? (self-assessment)
3. **Target State** — Where do I want to be? (competency target)
4. **Gap Analysis** — What's missing between current and target?
5. **Learning Path** — Sequence of topics/skills to acquire
6. **Practice Schedule** — How much time? How often? What activities?
7. **Success Criteria** — How will I know I've achieved the goal?
8. **Evidence Collection** — What artifacts prove competency? (projects, tests, demonstrations)
9. **Resources** — Books, courses, mentors, tools, environments
10. **Constraints** — Time available, budget, access to materials/mentors
11. **Dependencies** — Prerequisites, permissions, setup required
12. **First Learning Increment** — What's the first thing to study/practice?
13. **Open Questions** — Unknowns about the learning path
14. **Commit Readiness** — Is the path clear? Are resources available?

**AI Governance at Formalize:**
- `suggest`: Allowed
- `complete`: Allowed
- `generate`: Allowed (Learn domain is permissive)
- `transform`: Allowed
- `execute`: Not applicable

**Special Characteristics:**
- Emphasis on competency measurement and evidence
- Self-directed by nature — "for me, not for others"
- Success criteria must be verifiable (not just "I feel like I learned")
- Practice schedule is a commitment mechanism
- Gap analysis formalizes the learning challenge
- Evidence collection makes learning tangible

**Boundary Test:**
> "Is this for me to get better, or for others to use?"

If for internal capability formation → Learn.  
If for external production → Code/Create/Write.

---

### 5. Observe Domain

**Status:** ✓ Special case — Formalize may not apply

**Formalize Artifact:** _(none required)_

**What Formalization Means (Hypothesis):**
- **Observe is pre-Formalize by nature** — raw capture without interpretation
- Formalize may be optional or implicit for Observe domain
- Formalization happens when Observe transitions to another domain (promotion to Write, Learn, etc.)

**Subtypes:**
- `observe.notes` — Text-based raw capture
- `observe.bookmarks` — Links, references, citations
- `observe.clips` — Screenshots, quotes, snippets
- `observe.logs` — Journals, daily notes, activity records
- `observe.captures` — Photos, recordings, sensory data

**Entry Criteria (If Formalize applies):**
- Collection of observations exists
- Pattern or theme emerging
- Decision to organize/structure observations
- Intent to preserve for future use

**Exit Criteria (If Formalize applies):**
- Observation scope defined (what are we capturing?)
- Collection boundaries set (time range, topics, sources)
- Tagging/organization scheme defined
- Storage/retrieval method established
- Intended use articulated (even if vague)

**Proposed Observation Plan Sections (If needed):**
1. **Observation Intent** — Why are we capturing this?
2. **Scope & Focus** — What are we observing? What are we ignoring?
3. **Collection Method** — How are we capturing? (tools, frequency, format)
4. **Organization Scheme** — Tags, folders, metadata, links
5. **Boundaries** — Time range, topics, sources
6. **Intended Use** — What might we do with these observations later?
7. **Success Criteria** — When is the observation collection "complete"?

**AI Governance at Formalize:**
- `suggest`: Allowed
- `complete`: Blocked (preserve authenticity)
- `generate`: Blocked (preserve authenticity)
- `transform`: Blocked (preserve authenticity)
- `execute`: Not applicable

**Special Characteristics:**
- **Key insight:** Observe may not need Formalize at all
- Formalize happens during domain transition (Observe → Write, Observe → Learn)
- Raw capture authenticity is paramount
- AI generation is blocked to preserve observational integrity
- Lightweight or implicit formalization may be more appropriate

**Critical Question:**
> Does Observe domain ever reach Formalize, or does formalization happen when it transitions to another domain?

**Hypothesis:** Observe typically stays in Capture/Sense/Explore stages. When ready to formalize, it **promotes to another domain**:
- Observations → Essay = Observe → Write (Writing Brief required)
- Observations → Learning = Observe → Learn (Learning Plan required)
- Observations → Synthesis = Observe → Write/Create

Formalize may be the **transition trigger**, not a stage within Observe.

---

## Cross-Domain Findings

### 1. Formalize Spine is Universal

All domains share the 5 core elements:
1. Intent & Outcome
2. Scope & Boundaries
3. Constraints
4. Execution Framing
5. Commit Criteria

But each domain interprets these differently based on domain characteristics.

### 2. Domain-Specific Success Criteria

| Domain | Success Criteria Character |
|--------|---------------------------|
| Code | Measurable, testable, functional |
| Create | Aesthetic, emotional, experiential (may be subjective) |
| Write | Clear, persuasive, complete (informational) |
| Learn | Verifiable competency, demonstrable evidence |
| Observe | Authentic capture, retrievable storage |

### 3. AI Permissions Evolve at Formalize

| Domain | Generate at Formalize | Rationale |
|--------|----------------------|-----------|
| Code | Ask | Respect ownership, avoid over-generation |
| Create | Allowed | Generative by nature |
| Write | Ask | Respect authorship, avoid plagiarism |
| Learn | Allowed | Learning is accelerated by AI |
| Observe | Blocked | Preserve authenticity of raw capture |

### 4. Formalize Triggers Domain Transitions

**Key Pattern:** Formalize often marks domain promotion:
- Observe → Write (observations become essay)
- Observe → Learn (observations become learning goal)
- Learn → Code (learning becomes production skill)
- Explore (any domain) → Formalize (lock intent)

### 5. Observe is the Exception

**Hypothesis:** Observe domain may not reach Formalize within itself. Instead:
- Observe stays in Capture/Sense/Explore
- Formalize triggers promotion to Write/Learn/Create
- Formalize is the domain transition moment

This explains why `domains.md` says Observe has no formalize artifact.

---

## Entry/Exit Criteria Summary

### Universal Entry Criteria (All Domains)

- [ ] Shape complete; direction chosen
- [ ] Single direction selected from exploration
- [ ] Scope roughed out
- [ ] Major tradeoffs resolved
- [ ] Intent can be articulated clearly

### Universal Exit Criteria (All Domains)

- [ ] Formalize artifact exists (domain-specific)
- [ ] Intent and outcome explicitly documented
- [ ] Scope and boundaries defined (in-scope, out-of-scope)
- [ ] Constraints documented
- [ ] Success criteria defined
- [ ] First executable increment identified
- [ ] Dependencies and risks identified
- [ ] Commit readiness criteria met

### Domain-Specific Exit Criteria

**Code:**
- [ ] Technical architecture overview present
- [ ] Testing strategy defined
- [ ] Implementation constraints documented

**Create:**
- [ ] Aesthetic direction and style references captured
- [ ] Medium and format specified
- [ ] Creative constraints balanced with freedom

**Write:**
- [ ] Thesis statement clear and defensible
- [ ] Information architecture mapped
- [ ] Sources and evidence identified

**Learn:**
- [ ] Current and target competency defined
- [ ] Gap analysis complete
- [ ] Evidence collection method established

**Observe:**
- [ ] N/A — Formalize likely triggers domain transition

---

## Artifact Templates (Proposed)

### Creative Brief Template (Create Domain)

```markdown
# Creative Brief: [Project Name]

## Creative Intent
[What emotional/aesthetic response are you seeking?]

## Audience & Context
[Who experiences this? Where/how?]

## Aesthetic Direction
[Visual/sonic/spatial qualities, style references]

## Scope & Format
[Medium, dimensions, duration, deliverable format]

## Non-Goals
[What this explicitly is NOT]

## Constraints
[Tools, materials, time, budget, technical limits]

## Success Criteria
[What makes this "done"? How will you know it succeeded?]

## First Creative Increment
[What's the first concrete artifact to create?]

## Dependencies
[Materials, collaborators, access, approvals]

## Open Questions
[Unresolved creative decisions, spikes needed]

## Commit Readiness
- [ ] Creative direction is locked
- [ ] Resources are available
- [ ] Constraints are understood
- [ ] Success criteria are clear
```

### Writing Brief Template (Write Domain)

```markdown
# Writing Brief: [Project Name]

## Thesis/Central Argument
[What is the core claim or message?]

## Audience & Context
[Who reads this? Where/how is it published?]

## Purpose & Tone
[Inform? Persuade? Entertain? Formal/casual?]

## Scope & Boundaries
[What's covered? What's explicitly excluded?]

## Information Architecture
[How is the argument structured?]

## Sources & Evidence
[What research supports this?]

## Success Criteria
[Clear? Persuasive? Complete? How will you know?]

## Constraints
[Word count, format, publication deadlines, style guides]

## Non-Goals
[What this is NOT trying to accomplish]

## First Writing Increment
[What section/chapter/draft comes first?]

## Dependencies
[Research needed, expert review, approvals]

## Open Questions
[Unresolved arguments, research gaps]

## Commit Readiness
- [ ] Thesis is locked
- [ ] Structure is sound
- [ ] Sources are identified
- [ ] Audience is clear
```

### Learning Plan Template (Learn Domain)

```markdown
# Learning Plan: [Competency Name]

## Learning Goal
[What competency am I building?]

## Current State
[Where am I now? (self-assessment)]

## Target State
[Where do I want to be? (competency target)]

## Gap Analysis
[What's missing between current and target?]

## Learning Path
[Sequence of topics/skills to acquire]

## Practice Schedule
[How much time? How often? What activities?]

## Success Criteria
[How will I know I've achieved the goal?]

## Evidence Collection
[What artifacts prove competency?]

## Resources
[Books, courses, mentors, tools, environments]

## Constraints
[Time available, budget, access to materials/mentors]

## Dependencies
[Prerequisites, permissions, setup required]

## First Learning Increment
[What's the first thing to study/practice?]

## Open Questions
[Unknowns about the learning path]

## Commit Readiness
- [ ] Path is clear
- [ ] Resources are available
- [ ] Time is allocated
- [ ] Success is measurable
```

---

## AI Governance at Formalize

### Permission Matrix

| Domain | suggest | complete | generate | transform | execute |
|--------|---------|----------|----------|-----------|---------|
| Code | ✓ | ✓ | Ask | Ask | Ask |
| Create | ✓ | ✓ | ✓ | ✓ | — |
| Write | ✓ | ✓ | Ask | Ask | — |
| Learn | ✓ | ✓ | ✓ | ✓ | — |
| Observe | ✓ | ✗ | ✗ | ✗ | — |

### Rationale by Domain

**Code:**
- `generate/transform/execute` require permission to respect ownership and avoid over-automation
- Formalize locks intent; AI helps but doesn't dictate implementation

**Create:**
- Fully permissive — generative AI is a creative tool
- AI can suggest, complete, generate, and transform creative work

**Write:**
- `generate/transform` require permission to respect authorship
- AI assists but doesn't replace the writer's voice

**Learn:**
- Fully permissive — AI accelerates learning
- Generated exercises, explanations, and practice materials are valuable

**Observe:**
- AI generation blocked to preserve raw capture authenticity
- Only suggestions allowed (e.g., tagging, organization)

---

## Recommendations

### 1. Refine Create/Write/Learn Artifacts

**Action:** Create explicit templates for Creative Brief, Writing Brief, and Learning Plan based on this research.

**Rationale:** These domains have formalize artifacts named in `domains.md` but lack detailed specifications like Code's SOD.

**Priority:** HIGH

### 2. Clarify Observe Formalize Semantics

**Action:** Document that Observe domain typically does NOT reach Formalize within itself. Formalize triggers domain transition.

**Rationale:** Observe is pre-formalize by nature. Formalizing observations means promoting to Write/Learn/Create.

**Priority:** HIGH

### 3. Create Domain-Specific Formalize Checklists

**Action:** Create `formalize-create.md`, `formalize-write.md`, `formalize-learn.md` addenda (like `formalize-code.md`).

**Rationale:** Each domain needs specific guidance beyond the universal Formalize checklist.

**Priority:** MEDIUM

### 4. Update Templates

**Action:** Add Creative Brief, Writing Brief, and Learning Plan templates to `src/praxis/templates/domain/`.

**Rationale:** `praxis templates render --stage formalize` should generate appropriate artifacts for all domains.

**Priority:** MEDIUM

### 5. Validate with Real Projects

**Action:** Test these formalize patterns on real Create, Write, and Learn projects.

**Rationale:** Hypotheses need validation against actual work.

**Priority:** MEDIUM (post-initial implementation)

---

## Open Questions

1. **Observe Formalize:** Should Observe have any formalize artifact, or is domain transition always the formalize moment?

2. **Creative Brief Ambiguity:** How much ambiguity should remain in a Creative Brief? Too much constraint kills creativity; too little prevents commitment.

3. **Learning Evidence:** What constitutes sufficient evidence of competency? Domain-specific or universal standards?

4. **Formalize → Commit:** Do all domains require the same Commit gate criteria, or should criteria vary by domain?

5. **Multi-Domain Projects:** How do projects spanning domains (e.g., Code + Write for docs) handle Formalize?

---

## Next Steps

### Immediate (This Spike)
- [x] Research formalization patterns for all 5 domains
- [x] Define entry/exit criteria per domain
- [x] Identify domain-specific artifacts
- [x] Analyze AI governance implications
- [ ] Create handoff summary

### Follow-Up Work (Future Stories)
- [ ] Create Creative Brief template and specification
- [ ] Create Writing Brief template and specification
- [ ] Create Learning Plan template and specification
- [ ] Create `formalize-create.md` checklist addendum
- [ ] Create `formalize-write.md` checklist addendum
- [ ] Create `formalize-learn.md` checklist addendum
- [ ] Update `domains.md` with Observe formalize clarification
- [ ] Validate templates with real projects
- [ ] Update `praxis templates render` to generate all domain artifacts

---

## Research Time Log

- **00:00-00:15** — Repository exploration, reading lifecycle.md, domains.md, SOD spec
- **00:15-00:30** — Review existing checklists and domain opinions
- **00:30-01:00** — Deep analysis and hypothesis formation for each domain
- **01:00-01:30** — Template creation and artifact specification
- **01:30-02:00** — Synthesis, recommendations, documentation

**Total Time:** ~2 hours (exceeded 60-minute time box — spike went deep)

---

## Conclusion

**Formalize is universal but domain-aware.** All domains share the Formalize Spine (Intent, Scope, Constraints, Execution, Commit), but each domain interprets formalization differently:

- **Code:** Lock technical intent with SOD
- **Create:** Bound aesthetic intent with Creative Brief
- **Write:** Fix argumentative intent with Writing Brief
- **Learn:** Target competency with Learning Plan
- **Observe:** Formalize by transitioning to another domain

**Key insight:** Observe domain is the exception — it's pre-formalize by nature. Formalization for Observe means promotion to Write, Learn, or Create.

**Next action:** Implement Creative Brief, Writing Brief, and Learning Plan templates with domain-specific checklists.

---

_End of spike research._
