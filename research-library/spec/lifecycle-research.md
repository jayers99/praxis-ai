# Lifecycle Stage Research Report

<!--
metadata:
  id: spec-lifecycle-research-2025-12-28
  title: Lifecycle Stage Research Report
  date: 2025-12-28
  author: research-librarian
  status: approved
  topic: spec
  also_relevant: [foundations]
  keywords: [lifecycle, stages, capture, sense, explore, shape, formalize, commit, execute, sustain, close]
  consensus: high
  epistemic_standard: thorough
  sources_count: 15
  supersedes: null
  related: [spec-domains-research-2025-12-28, spec-sustain-worked-example-2025-12-28]
  approved_by: human
  approved_date: 2025-12-30
-->

## Executive Summary

- All 9 Praxis lifecycle stages align with established methodologies
- Key synthesis: GTD (Capture), Weick (Sense), Double Diamond (diverge/converge), Shape Up (Shape), Stage-Gate (Commit), Agile (Execute), ITIL (Sustain), PMI (Close)
- Unique Praxis contributions: explicit "Formalize hinge", two iteration modes, regression model, Close → Capture loop
- Overall confidence: HIGH for all 9 stages

## Consensus Rating

**High**: Each stage maps to established frameworks with strong prior art. Unique contributions are clearly differentiated.

## Body

### Stage Research

#### 1. Capture

**Definition:** Collect raw inputs with minimal friction. No commitment required.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| GTD (Allen) | Capture / Inbox | "Mind like water" — externalize to trusted system |
| Zettelkasten (Luhmann) | Fleeting Notes | 90,000 notes over 40 years; assume refinement later |
| Design Thinking (IDEO) | Empathize / Observe | User-centric observation |
| Double Diamond | Discover | Research broadly |

**Entry/Exit Criteria:**
- Entry: Any input exists
- Exit: Input stored in retrievable location

**Influencers:** David Allen, Niklas Luhmann, Tim Brown/IDEO, Jane Fulton Suri

**Confidence:** HIGH. Praxis combines observation + ideation, which some frameworks separate.

---

#### 2. Sense

**Definition:** Convert raw inputs into understanding. Light organization, tagging, pattern recognition.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| Weick | Sensemaking | ESR: Enactment-Selection-Retention; "plausibility over accuracy" |
| Cynefin (Snowden) | Probe-Sense-Respond | Complex domain requires sensing before acting |
| Zettelkasten | Literature Notes | Interpretation layer |
| Design Thinking | Define | Synthesize into problem statement |

**Entry/Exit Criteria:**
- Entry: Captured inputs exist
- Exit: Inputs have meaning/context; problem can be articulated

**Influencers:** Karl Weick, Dave Snowden, Brenda Dervin

**Confidence:** HIGH. Weick's theory directly supports this. "Sense" is less common than "Define" but more accurate.

---

#### 3. Explore

**Definition:** Generate possibilities without obligation. Abandonment is safe.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| Double Diamond | Discover (divergent) | Breadth over commitment |
| Design Thinking | Ideate | Quantity over quality; wild ideas welcome |
| Guilford | Divergent Thinking | Generate multiple solutions |
| Cynefin | Probe | Test ideas in complex domain |

**Entry/Exit Criteria:**
- Entry: Sense complete; problem understood
- Exit: Multiple possibilities exist; could describe 2-3 directions

**Influencers:** J.P. Guilford, Alex Osborn, British Design Council

**Confidence:** HIGH. Explicit "abandonment is safe" distinguishes Praxis.

---

#### 4. Shape

**Definition:** Converge toward viable direction. Selection, refinement. Work remains reversible.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| Shape Up (Singer) | Shaping | "Fixed time, variable scope"; defines what fits appetite |
| Double Diamond | Define (convergent) | Narrow using constraints |
| Convergent Thinking | Option Selection | Score options against criteria |

**Entry/Exit Criteria:**
- Entry: Multiple options exist
- Exit: Single direction chosen; scope roughed out; major tradeoffs resolved

**Influencers:** Ryan Singer, J.P. Guilford, British Design Council

**Confidence:** HIGH. Shape Up methodology is near-identical.

---

#### 5. Formalize (Structural Hinge)

**Definition:** Convert shaped thinking into durable, policy-bearing artifacts. Establishes scope, constraints, success criteria. Output: SOD.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| Software Engineering | SRS | "Clear, complete, unambiguous, non-contradictory" |
| Shape Up | Pitch | Bounded solution for betting |
| Stage-Gate | Business Case | Formal justification |
| Agile | Definition of Done | Explicit completion criteria |

**Entry/Exit Criteria:**
- Entry: Shape complete; direction chosen
- Exit: SOD exists with scope, constraints, success criteria

**Influencers:** IEEE, Ryan Singer, Robert G. Cooper, PMI

**Confidence:** HIGH. The "structural hinge" concept is **unique** — most frameworks blur exploration/execution.

**Key Insight:** Praxis balances Waterfall (over-formalizes) and Agile (under-formalizes).

---

#### 6. Commit

**Definition:** Explicitly decide to proceed. Locks scope, allocates effort, enforces policy.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| Stage-Gate | Gate / Go-Kill | "Gates with teeth" — real resource commitment |
| Shape Up | Betting Table | Selective betting; most ideas don't get bet on |
| Agile | Sprint Commitment | Team commits to backlog |
| Psychology | Public Commitment | Increases follow-through (Cialdini) |

**Entry/Exit Criteria:**
- Entry: SOD complete
- Exit: Explicit commitment to proceed; resources allocated

**Influencers:** Robert G. Cooper, Ryan Singer, McKinsey

**Confidence:** HIGH. "Small subset should reach Commit" aligns with Stage-Gate selectivity.

---

#### 7. Execute

**Definition:** Produce the artifact. Coding, writing, implementation. AI behavior tightly governed.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| Agile/Scrum | Sprint Execution | Iterative delivery |
| Shape Up | Build Cycle | 6-week fixed cycle |
| Double Diamond | Deliver | Finalize and implement |
| SDLC | Implementation | Build the software |

**Entry/Exit Criteria:**
- Entry: Commit complete
- Exit: Artifact produced per SOD

**Influencers:** Kent Beck, Jeff Sutherland, Ken Schwaber

**Confidence:** HIGH. Most universally understood stage. Praxis adds SOD-bounded governance.

---

#### 8. Sustain

**Definition:** Maintain and govern delivered work. Updates, evaluation, optimization.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| ITIL | Service Operation + CSI | Day-to-day + continuous improvement |
| DevOps | Operate / Monitor | Maintain reliability |
| SDLC | Maintenance | Bug fixes, support |

**Entry/Exit Criteria:**
- Entry: Execute complete; work delivered
- Exit: Work retired or closed

**Influencers:** ITIL, Gene Kim (Phoenix Project)

**Confidence:** MEDIUM-HIGH. Strong for technical work; less prior art for creative/written sustain.

**Key Question:** What does sustain mean for Write, Create, Learn domains?

---

#### 9. Close

**Definition:** End work intentionally. Archive, capture learnings, seed future cycles.

| Framework | Equivalent | Key Insight |
|-----------|------------|-------------|
| PMI | Project Closure | Formal sign-off, lessons learned |
| Agile | Retrospective | Reflect on process |
| Military | After-Action Review | Structured reflection |
| Research | Post-mortem | 33% improvement in outcome prediction |

**Entry/Exit Criteria:**
- Entry: Sustain complete or decision to end
- Exit: Leverage captured; next cycle seeded

**Influencers:** PMI, Esther Derby & Diana Larsen (Agile Retrospectives)

**Confidence:** HIGH. "Seeding future cycles" (Close → Capture loop) is unique.

---

### Cross-Cutting Findings

#### Framework Alignments

| Framework | Praxis Mapping |
|-----------|---------------|
| **Double Diamond** | Discover=Capture, Define=Sense+Shape, Develop=Explore+Shape, Deliver=Execute |
| **Stage-Gate** | Scoping=Capture+Sense, Business Case=Formalize, Gate=Commit, Development=Execute, Post-Launch=Close |
| **ITIL** | Strategy=Shape+Formalize, Transition=Commit+Execute, Operation=Sustain, CSI=Sustain+Close |
| **Shape Up** | Shaping=Shape, Betting=Commit, Building=Execute |

#### Unique Praxis Contributions

1. **Explicit Formalize hinge** — Most frameworks blur exploration/execution
2. **Two iteration modes** — Discovery (pre-Formalize) vs. refinement (post-Formalize)
3. **Regression model** — Stage-Gate says "kill or continue"; Praxis says "regress and fix"
4. **Close → Capture loop** — Explicit knowledge transfer to future cycles
5. **AI governance by stage** — Novel; no prior art found

---

### Follow-Up Research

| Topic | Priority | Key Questions |
|-------|----------|---------------|
| SOD Template Research | High | What makes a good SOD? Minimum viable SOD? |
| Sustain for Non-Code Domains | Medium | What does "sustain" mean for Create, Write, Learn? |
| Regression Trigger Detection | Medium | Can regressions be detected automatically? |
| Shape Up Deep Dive | Low | How closely does Shape Up align with Shape/Formalize? |

## Reusable Artifacts

### Stage Quick Reference

| Stage | Definition | Key Framework |
|-------|------------|---------------|
| Capture | Collect raw inputs | GTD, Zettelkasten |
| Sense | Convert to understanding | Weick Sensemaking |
| Explore | Generate possibilities | Double Diamond, Ideate |
| Shape | Converge on direction | Shape Up |
| Formalize | Create SOD | IEEE SRS, Stage-Gate |
| Commit | Explicitly decide | Stage-Gate, Betting |
| Execute | Produce artifact | Agile/Scrum |
| Sustain | Maintain and govern | ITIL |
| Close | End intentionally | PMI, Retrospective |

### Implementation-Ready Stories

| Story | Size | Confidence |
|-------|------|------------|
| Add Weick reference to Sense | S | HIGH |
| Add "abandonment safe" to Explore | S | HIGH |
| Document Formalize hinge | S | HIGH |
| Create SOD template | M | HIGH |
| Add Commit go/no-go criteria | M | HIGH |
| Add regression detection to validate | M | MEDIUM |

## Sources

### Design/Creativity
1. Double Diamond (British Design Council)
2. Design Thinking (IDEO, Tim Brown)
3. Divergent/Convergent Thinking (Guilford)

### Sensemaking
4. Weick, K. (Organizations)
5. Cynefin (Snowden)

### Product
6. Shape Up (Singer/Basecamp)
7. Stage-Gate (Cooper)

### Engineering
8. SRS (IEEE)
9. Agile/Scrum

### Operations
10. ITIL
11. DevOps

### Closure
12. PMI
13. After-Action Review
14. Agile Retrospectives (Derby & Larsen)

### Psychology
15. Cialdini (Public Commitment)

---

_Migrated from research/spec/lifecycle-research.md_
_Approved: 2025-12-30_
