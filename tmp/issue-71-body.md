## Spike Intent

Research and document best practices, prior art, and academic foundations for the 5 Praxis domains (Code, Create, Write, Observe, Learn).

---

## Time Box

**Size:** Medium  
**Duration:** 60 minutes  
**Credit Budget:** ~50 queries  

⚠️ Stop when time is up, even if incomplete. Partial findings are valuable.

---

## Story Details

📄 **Full story file:** `projects/write/opinions-framework/docs/02-refine-domains-story.md`

Read the story file for:
- Research questions per domain
- Boundary questions (Write vs Create, etc.)
- Output artifact specifications

---

## Task Summary

**Research all 5 domains:** Code, Create, Write, Observe, Learn

**For each domain find:**
- How others categorize this work
- Subtype taxonomies
- Boundary criteria (what's in, what's out)
- Key influencers

**Boundary questions to resolve:**
- Write vs. Create (blog post? fiction?)
- Observe vs. Learn (when does observation become learning?)
- Hybrid work handling

**Output:**
1. Research report → `projects/write/opinions-framework/docs/spike-02-domains-research.md`
2. Follow-up spikes needed
3. Implementation-ready stories

---

## Agent Instructions

1. Read this issue completely
2. Read the full story file linked above
3. Execute the spike respecting the 30-minute time box
4. Commit changes to your branch with message: `docs: spike 02 domains research`
5. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike 02: Domain Definitions Research" --body-file <handoff.md> --base main
   ```
6. Include "Closes #71" in your PR body

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

Closes #71
```

---

## Definition of Done

- [ ] Research report for all 5 domains
- [ ] Each domain has 2-3 sources
- [ ] Boundary questions addressed
- [ ] Follow-up spikes listed
- [ ] Changes committed
- [ ] PR created with handoff

---

## Notes

Can run in parallel with Spike 01 (Lifecycle).
