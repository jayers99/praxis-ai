# Story: Tracer Bullet — Code × Capture End-to-End

**Project:** opinions-framework  
**Size:** Large  
**Priority:** High (proves the process)  
**Depends on:** 01, 02, 03, 04

---

## Summary

Run one complete Domain × Stage cell through the full opinion research pipeline, single-threaded, to discover the real shape of the work before parallelizing.

**Target cell:** Code domain × Capture stage

---

## Problem Statement

We have a proposed research pipeline:
```
Influencers → First Principles → Consensus → Prioritization → Contract Validation
```

But we haven't proven it works. Running one cell end-to-end will:
1. Validate the pipeline steps
2. Reveal missing steps or unnecessary ones
3. Produce a real artifact we can evaluate
4. Inform the template and contract

---

## Why Code × Capture?

- **Code** is the most developed domain (template-python-cli exists)
- **Capture** is the first stage (simplest, least dependencies)
- This combination has the most prior art to validate against

---

## Acceptance Criteria

- [ ] Key influencers identified (5-10 sources)
- [ ] First principles extracted from each influencer
- [ ] Consensus synthesis produced (common themes, debates)
- [ ] Principles prioritized (must-have, should-have, nice-to-have)
- [ ] Quality gates defined
- [ ] Anti-patterns documented
- [ ] Final opinion file follows template from Story 04
- [ ] Opinion validated against template-python-cli Capture phase
- [ ] Process learnings documented (what worked, what didn't)
- [ ] Time/effort tracked for estimation of remaining cells

---

## Research Pipeline

### Phase 1: Key Influencers (Research)

**Goal:** Identify 5-10 authoritative sources on best practices for the Capture stage of code projects.

**Sources to consider:**
- Software engineering thought leaders (Martin Fowler, Kent Beck, etc.)
- Product management literature (on requirements gathering)
- Academic research on software inception phases
- Agile/Lean methodology (early-stage practices)
- Developer experience research

**Output:** `key-influencers.md` with:
- Name/Title
- Why authoritative
- Key concepts they contribute
- Citation/URL

### Phase 2: First Principles Extraction

**Goal:** For each key influencer, extract their core principles relevant to Code × Capture.

**Output:** `research-notes.md` with:
- Influencer-by-influencer analysis
- Direct quotes or paraphrased principles
- How principle maps to Capture stage

### Phase 3: Consensus Synthesis

**Goal:** Identify common themes across influencers and note areas of disagreement.

**Output:** `synthesis.md` with:
- Common principles (high confidence)
- Emerging patterns
- Areas of debate or contradiction
- Gaps not covered by sources

### Phase 4: Prioritization

**Goal:** Categorize principles by importance.

**Criteria:**
- **must-have:** Violating this causes project failure or significant rework
- **should-have:** Improves quality; absence creates friction
- **nice-to-have:** Helpful but not critical

**Output:** Update `synthesis.md` with severity tags

### Phase 5: Contract Validation

**Goal:** Format the synthesized opinions according to the template and validate against contract.

**Output:** `docs/opinions/code/capture.md` following Story 04 template

---

## Validation Step

After producing the opinion file:

1. Review against `projects/code/template-python-cli/` Capture phase
2. Ask: Would these opinions have helped? Hurt? Were they followed implicitly?
3. Identify gaps: What did template-python-cli do that opinions don't cover?
4. Identify excess: What do opinions say that wasn't relevant?
5. Refine opinion file based on findings

---

## Tasks

1. [ ] Research key influencers for Code × Capture
2. [ ] Extract first principles from each source
3. [ ] Synthesize consensus and debates
4. [ ] Prioritize principles (must/should/nice-to-have)
5. [ ] Draft opinion file using template
6. [ ] Validate against template-python-cli
7. [ ] Refine based on validation
8. [ ] Document process learnings
9. [ ] Estimate time for remaining cells

---

## Tracking

| Phase | Estimated Time | Actual Time | Notes |
|-------|----------------|-------------|-------|
| Key Influencers | 2 hours | | |
| Extraction | 3 hours | | |
| Synthesis | 2 hours | | |
| Prioritization | 1 hour | | |
| Drafting | 1 hour | | |
| Validation | 1 hour | | |
| Refinement | 1 hour | | |
| **Total** | **11 hours** | | |

This estimate helps scope the full 45-cell effort.

---

## Non-Goals

- Not parallelizing (this is intentionally single-threaded)
- Not perfecting the output (learning > polish)
- Not creating opinions for other cells

---

## Dependencies

- 01-refine-lifecycle-story (Capture stage must be well-defined)
- 02-refine-domains-story (Code domain must be well-defined)
- 03-define-praxis-contract-story (contract must be settled)
- 04-define-opinion-structure-story (template must exist)

## Blocks

- 06-document-process (depends on learnings from this)
- Multi-agent parallelization (can't scale until process is proven)

---

## Notes

This is the "tracer bullet" — a single end-to-end pass that proves the system works before scaling.

Key questions to answer:
1. Is the research pipeline correct? Missing steps? Unnecessary steps?
2. Does the template structure work in practice?
3. How long does one cell take? (Informs parallelization planning)
4. What tools/methods work best for the research phase?
