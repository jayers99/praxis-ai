# Spike: Shape Up Deep Dive

**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Small  
**Priority:** Low

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| **Small** | **15 min** | **~10 queries** |
| Medium | 30 min | ~25 queries |
| Large | 60 min | ~50 queries |

*This spike is Small.*

---

## Spike Intent

Research how closely Basecamp's Shape Up methodology aligns with Praxis Shape and Formalize stages. Shape Up is the closest prior art to our shaping/betting model.

---

## Research Questions

1. How closely does Shape Up align with Shape/Formalize?
2. What can we borrow from Shape Up?
3. Where do we diverge and why?
4. What's the relationship between "appetite" and our SOD constraints?

---

## Where to Look

- Shape Up book (Basecamp)
- Shape Up community discussions
- Ryan Singer's talks and blog posts

---

## Output Artifacts

1. Research report → `01-refine-lifecycle-research-05-shape-up-report.md`
2. Alignment matrix (Shape Up concepts → Praxis stages)
3. Recommendations for borrowing/diverging
4. Follow-up stories if needed

---

## Definition of Done

- [ ] Shape Up concepts mapped to Praxis
- [ ] Alignment/divergence documented
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 15-minute time box
3. Commit changes to your branch with message: `docs: spike 05 shape up deep dive`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: Shape Up Deep Dive" --body-file <handoff.md> --base main
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
