# Story: Validate Opinions Against render-run Project

**Project:** opinions-framework  
**Size:** Medium  
**Priority:** Medium (real-world validation)  
**Depends on:** 05-tracer-bullet-story, 06-document-process-story

---

## Summary

Apply the generated opinions to a real project (render-run) to validate that they improve work quality and integrate with actual Praxis usage.

---

## Problem Statement

Opinions generated in isolation may be academically sound but practically useless. Validation against a real project answers:
1. Do the opinions apply to real work?
2. Are they actionable (not just abstract)?
3. Do they integrate with the Praxis workflow?
4. Do they catch real issues or prevent real mistakes?

---

## Why render-run?

- It's an active Code domain project
- It has history we can retrospectively evaluate
- It's complex enough to stress-test opinions
- It's not template-python-cli (avoids overfitting to our validation source)

---

## Acceptance Criteria

- [ ] Opinions applied to render-run at current stage
- [ ] Gaps identified (opinions that should exist but don't)
- [ ] Excess identified (opinions that don't apply)
- [ ] Actionability tested (could we follow these?)
- [ ] AI integration tested (can agent use opinions effectively?)
- [ ] Retrospective analysis done (would opinions have helped earlier stages?)
- [ ] Refinements captured and fed back to opinion files
- [ ] Integration friction documented (Praxis workflow issues)

---

## Validation Approach

### Prospective Validation (Current Stage)

1. Read render-run's `praxis.yaml` to determine stage
2. Load applicable opinions for that Domain × Stage
3. Evaluate current work against opinion quality gates
4. Attempt to follow stage transition checklist
5. Note: What's missing? What doesn't apply? What's unclear?

### Retrospective Validation (Past Stages)

1. Review render-run's git history for each lifecycle stage
2. For each stage, ask: "Would the opinions have helped?"
3. Identify instances where opinions would have caught issues
4. Identify instances where opinions would have been ignored/irrelevant

### AI Integration Test

1. Start a Claude session with render-run context
2. Prompt: "Read the applicable opinions and evaluate this project"
3. Evaluate: Did the AI apply opinions correctly? Usefully?
4. Note friction: What instructions did the AI need?

---

## Tasks

1. [ ] Identify render-run's current stage
2. [ ] Apply current opinions to render-run
3. [ ] Document gaps and excess
4. [ ] Perform retrospective analysis on past stages
5. [ ] Test AI integration with opinions
6. [ ] Capture refinements for opinion files
7. [ ] Document Praxis integration friction
8. [ ] Review with stakeholder

---

## Expected Findings

| Category | What We Might Learn |
|----------|---------------------|
| Gaps | Opinions that should exist but don't |
| Excess | Opinions too abstract/not applicable |
| Actionability | Opinions that are hard to follow |
| Integration | Praxis workflow doesn't support opinions well |
| AI | Agent instructions need refinement |

---

## Non-Goals

- Not fixing render-run (observation only, unless quick wins)
- Not generating all 45 opinion files
- Not implementing Praxis CLI features

---

## Dependencies

- 05-tracer-bullet-story (opinions must exist to test)
- 06-document-process-story (process must be documented)

## Blocks

- Parallelized opinion research (need validation before scaling)
- Praxis CLI opinion features (need friction findings)

---

## Notes

This story addresses the concern: "Validate that against a dummy coding project, I suggest render-run."

The validation ensures opinions are grounded in reality, not just research. It also surfaces integration issues that inform the Praxis policy engine work.
