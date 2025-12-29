## Spike Intent

Research and document best practices, prior art, and academic foundations for each of the 9 Praxis lifecycle stages.

---

## Time Box

**Size:** Large  
**Duration:** 60 minutes  
**Credit Budget:** ~50 queries  

⚠️ Stop when time is up, even if incomplete. Partial findings are valuable.

---

## Story Details

📄 **Full story file:** `projects/write/opinions-framework/docs/01-refine-lifecycle-story.md`

Read the story file for:
- Research questions per stage
- Special focus on Capture stage
- Output artifact specifications

---

## Task Summary

**Research all 9 stages:** Capture, Sense, Explore, Shape, Formalize, Commit, Execute, Sustain, Close

**For each stage find:**
- Prior art / what others call it
- Key influencers
- Entry/exit criteria patterns
- Confidence in current definition

**Output:**
1. Research report → `projects/write/opinions-framework/docs/spike-01-lifecycle-research.md`
2. Follow-up spikes needed
3. Implementation-ready stories
4. Proposed order

---

## Agent Instructions

1. Read this issue completely
2. Read the full story file linked above
3. Execute the spike respecting the 60-minute time box
4. Commit changes to your branch with message: `docs: spike 01 lifecycle research`
5. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike 01: Lifecycle Stage Research" --body-file <handoff.md> --base main
   ```
6. Include "Closes #70" in your PR body

---

## Handoff Template

Your PR body should include:

```markdown
## Summary
What you researched and key findings

## Files Changed
- List of files created/modified

## Decisions Made
- Key choices and rationale

## Open Questions
- What remains unknown

## Time Spent
- Actual time vs budget

## Follow-Up Needed
- Recommended next spikes/stories

Closes #70
```

---

## Definition of Done

- [ ] Research report for all 9 stages
- [ ] Each stage has 2-3 sources
- [ ] Follow-up spikes listed
- [ ] Changes committed
- [ ] PR created with handoff
