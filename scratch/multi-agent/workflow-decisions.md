# Multi-Agent Workflow Decisions

**Date:** 2025-12-28  
**Status:** Working decisions (subject to refinement)

---

## Workflow Pattern

### Issue-Driven Agent Work

```
1. Create Story → Refine → Convert to GitHub Issue
2. Create Worktree + Branch for the issue
3. Launch Agent with minimal prompt
4. Agent reads issue → follows instructions → creates PR
5. Human reviews PR → merges or requests changes
```

### Command to Launch Agent

**Step 1:** Open terminal in worktree directory
```bash
cd /path/to/worktree
```

**Step 2:** Start Claude in interactive mode (not -p mode)
```bash
claude --dangerously-skip-permissions
```

**Step 3:** Paste the prompt
```
Work GitHub Issue #NN. Read the issue with 'gh issue view NN' and follow all instructions.
```

**Why interactive mode (not `-p`):**
- `-p` (print mode) exits after response — no visibility
- Interactive mode shows agent thinking, tool calls, progress
- Better for monitoring and debugging
- Can intervene if something goes wrong

The issue is the **source of truth** — contains everything agent needs.

---

## Sizing and Time Boxes

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 15 min | ~10 queries |
| Medium | 30 min | ~25 queries |
| Large | 60 min | ~50 queries |

**Key principle:** AI time ≠ human time. These are AI-appropriate durations.

---

## GitHub Labels Created

| Label | Description | Color |
|-------|-------------|-------|
| `spike` | Research/exploration story | Purple (#7057ff) |
| `size:small` | 15 min time box, ~10 queries | Light blue |
| `size:medium` | 30 min time box, ~25 queries | Blue |
| `size:large` | 60 min time box, ~50 queries | Green |

---

## Issue Structure

Every issue should contain:

```markdown
## Time Box
**Size:** [Small/Medium/Large]
**Duration:** [15/30/60] minutes
**Credit Budget:** ~[10/25/50] queries

## Story Details
📄 **Full story file:** `path/to/story.md`

## Task Summary
Quick reference of what to do

## Agent Instructions
1. Read this issue
2. Read the story file
3. Execute respecting time box
4. Commit changes
5. Create PR with handoff

## Handoff Template
[Format for PR body]

## Definition of Done
- [ ] Checkboxes
```

---

## Handoff via PR

**Decision:** Agent handoff is a Pull Request, not an issue comment.

**Rationale:**
- PR shows diff (what changed)
- PR has approval gate (human authority)
- PR links to issue (Closes #NN)
- One-click merge after approval

**PR body format:**
```markdown
## Summary
What was done and key findings

## Files Changed
- list

## Decisions Made
- key choices

## Open Questions
- unknowns

## Time Spent
- actual vs budget

## Follow-Up Needed
- next spikes/stories

Closes #NN
```

---

## Worktree Conventions

| Component | Convention | Example |
|-----------|------------|---------|
| Worktree directory | `praxis-ai-<name>` | `praxis-ai-claude-left` |
| Branch | `story/NN-short-name` | `story/01-refine-lifecycle` |

**Create worktree with branch:**
```bash
git worktree add ../praxis-ai-story-01 -b story/01-refine-lifecycle main
```

---

## Spike vs Implementation Stories

**Spike (research/exploration):**
- Output is research report, not code/doc changes
- Time-boxed (stop when time's up)
- Produces: findings, follow-up spikes, implementation-ready stories
- Used in early stages (Capture, Sense, Explore)

**Implementation story:**
- Output is actual changes (code, docs)
- Has acceptance criteria
- Used in later stages (Shape, Formalize, Execute)

---

## Parallel Agents

Agents can run in parallel when:
- They work on independent issues
- They have separate worktrees (isolation)
- They don't touch overlapping files

Current setup allows 2+ agents:
- One per worktree
- One per branch
- Merge conflicts resolved at PR time

---

## What We Haven't Decided Yet

- [ ] How to handle agent failures / incomplete work
- [ ] Credit tracking / monitoring
- [ ] Automated status dashboard
- [ ] When to split spikes vs. combine them
- [ ] Story template standardization

---

## Example: Spike 01

**Issue:** #70 - Research Lifecycle Stage Definitions  
**Labels:** `spike`, `size:large`  
**Time Box:** 60 min  
**Worktree:** `praxis-ai-claude-left`  
**Branch:** `story/01-refine-lifecycle`  
**Story file:** `projects/write/opinions-framework/docs/01-refine-lifecycle-story.md`  
**Output:** Research report + follow-up spikes + PR

---

## References

- `scratch/multi-agent/forman.md` — Foreman mental model
- `scratch/multi-agent/MULTI_AGENT_PLAYBOOK.md` — Isolation principles
- `scratch/multi-agent/AGENT_HANDOFF_TEMPLATE.md` — Handoff format
