# Spike: Research Lifecycle Stage Definitions

**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Large  
**Priority:** High (foundational for all opinions work)

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 30 min | ~20 queries |
| Medium | 60 min | ~50 queries |
| **Large** | **120 min** | **~100 queries** |

*This spike is Large.*

---

## Spike Intent

Research and document best practices, prior art, and academic foundations for each of the 9 Praxis lifecycle stages. This is exploratory work to inform concrete refinement stories.

**This is NOT an implementation story.** The output is research, not code or final documentation.

---

## Why a Spike?

We're in the Capture stage of the opinions-framework project. Per our own model, Capture involves:
- Initial brain dumps (done)
- Expansion and orthogonal thinking (this spike)
- Prior art research (this spike)
- Directed collection (this spike)

A spike is appropriate because:
1. We don't know what we don't know about lifecycle stages
2. Each stage may have significant academic/industry research we're missing
3. Better to research broadly now than discover gaps during execution
4. Spike outputs inform which follow-up stories are needed

---

## Research Questions per Stage

### Capture

- What prior art exists? (Ideation, divergent thinking, brainstorming, design thinking)
- Does Capture have internal phases/lifecycle?
- What prompts users to continue collecting vs. stopping too early?
- How to balance "minimal friction" with "thorough collection"?
- Key influencers/researchers in this space?

### Sense

- What prior art exists? (Sensemaking, affinity mapping, thematic analysis)
- How is "understanding" distinguished from "raw data" in research?
- What frameworks exist for organizing unstructured inputs?
- Key influencers/researchers?

### Explore

- What prior art exists? (Divergent thinking, option generation, design space exploration)
- How do methodologies like Design Thinking handle exploration?
- What signals "enough" exploration?
- Key influencers/researchers?

### Shape

- What prior art exists? (Convergent thinking, decision-making, option selection)
- How is "viable direction" defined in product/design literature?
- What frameworks exist for narrowing options?
- Key influencers/researchers?

### Formalize

- What prior art exists? (Requirements documentation, specifications, contracts)
- How do Agile, Waterfall, and other methodologies handle formalization?
- What makes a formalization artifact "good enough"?
- Key influencers/researchers?

### Commit

- What prior art exists? (Go/no-go decisions, commitment protocols)
- How do organizations handle commitment gates?
- What psychology research exists on commitment and follow-through?
- Key influencers/researchers?

### Execute

- What prior art exists? (Implementation, production, delivery)
- How do methodologies govern execution?
- What distinguishes execution from sustain?
- Key influencers/researchers?

### Sustain

- What prior art exists? (Maintenance, operations, continuous improvement)
- How is "scope creep" distinguished from "legitimate enhancement"?
- What triggers regression to earlier stages?
- Key influencers/researchers?

### Close

- What prior art exists? (Project closure, retrospectives, knowledge capture)
- What makes a good close?
- How do outcomes seed new cycles?
- Key influencers/researchers?

---

## Output Artifacts

### 1. Research Report

**File:** `projects/write/opinions-framework/docs/spike-01-lifecycle-research.md`

For each stage:
- Summary of prior art found
- Key influencers/sources identified
- Terminology mapping (what we call it vs. what others call it)
- Gaps or contradictions discovered
- Confidence level (high/medium/low) in our current definition

### 2. Follow-Up Spikes Needed

List of areas where more research is needed before we can write implementation stories. Each should specify:
- What question remains unanswered
- Where to look for answers
- Estimated time to research

### 3. Implementation Stories Ready

List of refinements that are well-understood enough to become concrete stories. For each:
- What change to make
- Why we're confident
- Proposed story size

### 4. Proposed Story Order

Based on dependencies and confidence, propose which stories to tackle first.

---

## Time Box Structure

| Phase | Time | Activity |
|-------|------|----------|
| Setup | 15 min | Read current lifecycle.md, note initial questions |
| Research: Capture-Sense-Explore | 90 min | Web search, synthesis |
| Research: Shape-Formalize-Commit | 60 min | Web search, synthesis |
| Research: Execute-Sustain-Close | 45 min | Web search, synthesis |
| Synthesis | 30 min | Compile research report, identify gaps |
| Handoff | 15 min | Write up findings, propose next steps |
| **Total** | **4 hours** | |

**If time runs out:** Stop and document what's known vs. unknown. Incomplete research is still valuable.

---

## Research Methods

1. **Web search** — Academic papers, industry blogs, methodology docs
2. **Cross-reference terminology** — What do others call these phases?
3. **Look for patterns** — Multiple sources agreeing = high confidence
4. **Note contradictions** — Disagreement indicates area for deeper investigation
5. **Identify influencers** — Who are the authorities in this space?

---

## Definition of Done

- [ ] Research report produced for all 9 stages
- [ ] Each stage has at least 2-3 sources identified
- [ ] Follow-up spikes listed with clear questions
- [ ] Implementation-ready stories identified
- [ ] Proposed story order documented
- [ ] Time box respected (stop at 4 hours even if incomplete)
- [ ] Handoff summary produced

---

## Non-Goals

- Not updating `docs/lifecycle.md` (that's implementation)
- Not resolving all ambiguities (some may need more research)
- Not producing opinion content (that's later)
- Not exceeding time box

---

## Dependencies

- None (this is foundational research)

## Enables

- Concrete lifecycle refinement stories
- Domain refinement spike (Story 02)
- All downstream opinion work

---

## Agent Instructions

**To execute this spike, copy the following to the agent:**

```
Read and execute this spike file completely.

This is a RESEARCH spike, not an implementation story. Your job is to explore, not to change docs/lifecycle.md.

Time box: 4 hours (stop when time is up, even if incomplete)

Your task:
1. For EACH of the 9 lifecycle stages:
   - Search for prior art (academic, industry, methodology docs)
   - Identify what others call this phase
   - Find key influencers/researchers
   - Note gaps or contradictions
   - Rate your confidence in our current definition (high/medium/low)

2. Produce the research report:
   - Save to: projects/write/opinions-framework/docs/spike-01-lifecycle-research.md

3. List follow-up spikes needed (questions that remain unanswered)

4. List implementation-ready stories (changes we're confident about)

5. Propose story order based on dependencies and confidence

6. Produce a handoff summary with:
   - What you researched
   - Key findings
   - What remains unknown
   - Recommended next steps
   - Time spent

If you hit the time box before finishing, STOP and document your partial findings. Incomplete research is valuable.
```
