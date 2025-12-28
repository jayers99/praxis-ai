# Story: Refine Lifecycle Stage Definitions

**Project:** opinions-framework  
**Size:** Medium  
**Priority:** High (blocks opinion research)

---

## Summary

Review and refine the nine lifecycle stage definitions in `docs/lifecycle.md` to ensure they are:
1. **Unambiguous** — Clear enough that AI can interpret them consistently
2. **Actionable** — Convertible to concrete instructions per stage
3. **Opinion-ready** — Provide sufficient structure for stage-specific opinions

---

## Problem Statement

The opinions framework will generate guidance for each Domain × Stage cell. If stage definitions are fuzzy, the resulting opinions will be inconsistent or overlapping.

**Current state:** `docs/lifecycle.md` v0.2 provides good high-level descriptions, but some stages may lack:
- Concrete entry/exit criteria
- Clear distinction from adjacent stages
- Sufficient specificity for AI-consumable instructions

---

## Acceptance Criteria

- [ ] Each stage has explicit **entry criteria** (what must be true to enter)
- [ ] Each stage has explicit **exit criteria** (what must be true to leave)
- [ ] Each stage has a **primary question** it answers
- [ ] Each stage has a **primary output** (artifact or state change)
- [ ] Boundaries between adjacent stages are unambiguous
- [ ] Stage definitions are AI-parseable (could generate instructions from them)
- [ ] No circular dependencies or unclear regression paths

---

## Current Stage Definitions (Audit)

| Stage | Current Definition | Clarity | Issues to Address |
|-------|-------------------|---------|-------------------|
| **Capture** | Collect raw inputs with minimal friction | ✓ Clear | Entry criteria implicit (none needed?) |
| **Sense** | Convert raw inputs into understanding | ◐ Moderate | What distinguishes "understanding" from raw? |
| **Explore** | Generate possibilities without obligation | ◐ Moderate | When is exploration "enough"? |
| **Shape** | Converge toward a viable direction | ◐ Moderate | What's the threshold for "viable"? |
| **Formalize** | Convert shaped thinking into durable artifacts | ✓ Clear | Well-defined (SOD requirement) |
| **Commit** | Explicitly decide to proceed | ✓ Clear | Clear gate |
| **Execute** | Produce the artifact | ✓ Clear | Bounded by formalized scope |
| **Sustain** | Maintain and govern delivered work | ◐ Moderate | When does maintenance become new work? |
| **Close** | End work intentionally | ✓ Clear | Terminal state, seeds new cycle |

### Stages Requiring Attention

1. **Sense** — Boundary with Capture is soft ("organized notes" vs "raw notes")
2. **Explore** — No clear signal for when exploration is complete
3. **Shape** — "Viable direction" is subjective; needs criteria
4. **Sustain** — Distinction between "maintenance" and "new feature" unclear

---

## Proposed Refinements

### Sense

**Current:** Convert raw inputs into understanding.

**Proposed additions:**
- **Entry criteria:** Raw inputs exist in Capture
- **Exit criteria:** Inputs are organized, tagged, and you can articulate the problem/opportunity
- **Primary question:** "What do I have here?"
- **Primary output:** Organized summary, tagged references, pattern observations
- **Distinguisher from Capture:** Capture = collect; Sense = organize and name

### Explore

**Current:** Generate possibilities without obligation.

**Proposed additions:**
- **Entry criteria:** Problem/opportunity is understood (Sense complete)
- **Exit criteria:** Multiple viable options exist; you could describe at least 2-3 directions
- **Primary question:** "What could I do?"
- **Primary output:** Options list, rough sketches, divergent possibilities
- **Distinguisher from Shape:** Explore = diverge; Shape = converge

### Shape

**Current:** Converge toward a viable direction.

**Proposed additions:**
- **Entry criteria:** Multiple options exist (Explore complete)
- **Exit criteria:** Single direction chosen; scope is roughed out; major tradeoffs resolved
- **Primary question:** "What will I do?"
- **Primary output:** Selected direction, rough scope, key constraints identified
- **Distinguisher from Formalize:** Shape = decision; Formalize = documentation

### Sustain

**Current:** Maintain and govern delivered work.

**Proposed additions:**
- **Entry criteria:** Work is delivered and in use (Execute complete)
- **Exit criteria:** Work is no longer active or is being closed
- **Primary question:** "Is this still fit for purpose?"
- **Primary output:** Maintenance updates, evaluations, governed changes
- **Distinguisher from Execute:** Sustain = incremental improvement within scope; Execute = initial delivery
- **Regression trigger:** If change expands scope → Commit (new decision); if change alters design → Formalize

---

## Tasks

1. [ ] Review each stage definition in `docs/lifecycle.md`
2. [ ] Draft entry/exit criteria for each stage
3. [ ] Add "Primary Question" and "Primary Output" to each stage
4. [ ] Clarify boundaries between Capture↔Sense, Explore↔Shape, Sustain↔Execute
5. [ ] Validate against template-python-cli project (did it follow these stages cleanly?)
6. [ ] Update `docs/lifecycle.md` with refinements
7. [ ] Review with stakeholder (you)

---

## Non-Goals

- Not redefining the stage model (9 stages are fixed)
- Not changing regression rules (those are settled)
- Not creating domain-specific stage variations (that's a separate concern)

---

## Dependencies

- None (this is foundational work)

## Blocks

- Story: Define opinions ↔ Praxis contract
- Story: Tracer bullet (Code × Capture)
- All opinion research work

---

## Notes

This story addresses the concern: "I think it would be smart to review our lifecycle stages and see if they lack in any clarity or can be augmented to provide unambiguous clear instructions that can be converted by AI into instructions."

The refinements should make stages concrete enough that an AI reading `docs/lifecycle.md` could generate stage-appropriate guidance without human interpretation.
