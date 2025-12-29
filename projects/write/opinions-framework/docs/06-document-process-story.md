# Story: Document Opinion Generation Process

**Project:** opinions-framework  
**Size:** Small  
**Priority:** Medium (enables scaling)  
**Depends on:** 05-tracer-bullet-story

---

## Summary

After completing the tracer bullet, document what we learned about the opinion generation process. This becomes the playbook for parallelizing the remaining cells.

---

## Problem Statement

The tracer bullet (Story 05) will reveal the actual process for generating opinions. We need to capture that knowledge before it's lost, so:
1. Future cells follow a proven process
2. Multi-agent work has clear instructions
3. The process is repeatable and improvable

---

## Acceptance Criteria

- [ ] Each step in the actual process is named and described
- [ ] Each step has estimated duration
- [ ] Each step has clear inputs and outputs
- [ ] Friction points are documented (what was hard?)
- [ ] Tools and methods that worked well are captured
- [ ] Process is formatted as agent-ready instructions
- [ ] Variations by domain/stage are noted (if discovered)

---

## Proposed Outline

**File:** `docs/opinion-generation-process.md`

```markdown
# Opinion Generation Process

## Overview

Step-by-step process for generating a complete opinion file for any Domain × Stage cell.

## Process Steps

### Step 1: {{Step Name}}

- **Duration:** X hours
- **Input:** What you need before starting
- **Output:** What you produce
- **Method:** How to do it
- **Tools:** What helps
- **Pitfalls:** What to avoid

### Step 2: {{Step Name}}

...

## Templates and Checklists

- [ ] Checklist for step completion
- Reference templates for each artifact

## Variations

- Domain-specific differences
- Stage-specific differences

## Lessons Learned

What we discovered during the tracer bullet that should inform future work.
```

---

## Tasks

1. [ ] Complete tracer bullet (Story 05)
2. [ ] Immediately document process while fresh
3. [ ] Name each step in the pipeline
4. [ ] Record actual time spent per step
5. [ ] Note what worked and what didn't
6. [ ] Format as agent-ready instructions
7. [ ] Review with stakeholder

---

## Non-Goals

- Not refining the process (that's future iteration)
- Not creating automation (just documentation)
- Not generating more opinion files

---

## Dependencies

- 05-tracer-bullet-story (must complete first)

## Blocks

- Multi-agent parallelization (agents need this playbook)

---

## Notes

This is a "capture the learning" story. It should be done immediately after the tracer bullet while the experience is fresh.

The output becomes the instruction set for Story 07 (validate against render-run) and any future multi-agent research.
