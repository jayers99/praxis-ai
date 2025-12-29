# Spike: SOD Template Research

**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Medium  
**Priority:** High

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 30 min | ~20 queries |
| **Medium** | **60 min** | **~50 queries** |
| Large | 120 min | ~100 queries |

*This spike is Medium.*

---

## Spike Intent

Research what makes a good Solution Overview Document (SOD). Compare with PRDs, BRDs, RFCs, and Design Docs to understand minimum viable formalization.

---

## Research Questions

1. What makes a good SOD?
2. How does SOD compare to PRD, BRD, RFC, Design Doc?
3. What's the minimum viable SOD?
4. What sections are required vs. optional?
5. How do lightweight vs. heavyweight formalizations differ?

---

## Where to Look

- Product management literature (PRDs, user stories)
- Engineering documentation practices (RFCs, Design Docs)
- Agile/Lean documentation approaches
- Shape Up pitch format

---

## Output Artifacts

1. Research report → `01-refine-lifecycle-research-02-sod-template-report.md`
2. Comparison matrix (SOD vs PRD vs BRD vs RFC)
3. Proposed SOD template structure
4. Follow-up stories if needed

---

## Definition of Done

- [ ] SOD compared to at least 3 similar artifacts
- [ ] Minimum viable SOD identified
- [ ] Template structure proposed
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 60-minute time box
3. Commit changes to your branch with message: `docs: spike 02 sod template research`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: SOD Template Research" --body-file <handoff.md> --base main
   ```
5. Include "Closes #XX" in your PR body

---

## Handoff Template

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

Closes #XX
```
