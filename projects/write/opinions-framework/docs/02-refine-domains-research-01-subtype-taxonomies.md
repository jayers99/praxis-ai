# Spike: Subtype Taxonomies per Domain

**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Medium  
**Priority:** Medium

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 15 min | ~10 queries |
| **Medium** | **30 min** | **~25 queries** |
| Large | 60 min | ~50 queries |

*This spike is Medium.*

---

## Spike Intent

Research what subtypes should each domain support. Subtypes enable hierarchical opinion inheritance (e.g., Code → CLI → CLI-Python).

---

## Research Questions

1. What subtypes should Code domain support? (CLI, Library, API, Web App, Infrastructure, etc.)
2. What subtypes should Create domain support? (Visual, Audio, Interactive, etc.)
3. What subtypes should Write domain support? (Technical, Business, Narrative, etc.)
4. What subtypes should Learn domain support? (Skill, Concept, Practice, etc.)
5. What subtypes should Observe domain support? (Notes, Bookmarks, Logs, etc.)
6. Are there industry-standard taxonomies for each domain?

---

## Where to Look

- Software engineering project taxonomies
- Creative industry categorizations
- Technical writing standards
- Educational/learning science frameworks
- Personal knowledge management (PKM) systems

---

## Output Artifacts

1. Research report → `02-refine-domains-research-01-subtype-taxonomies-report.md`
2. Proposed taxonomy tree per domain
3. Industry sources for each taxonomy
4. Follow-up stories if needed

---

## Definition of Done

- [ ] Subtype taxonomy proposed for each of 5 domains
- [ ] At least 2 sources per domain
- [ ] Taxonomies are hierarchical (support inheritance)
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 30-minute time box
3. Commit changes to your branch with message: `docs: spike subtype taxonomies research`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: Subtype Taxonomies per Domain" --body-file <handoff.md> --base main
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
