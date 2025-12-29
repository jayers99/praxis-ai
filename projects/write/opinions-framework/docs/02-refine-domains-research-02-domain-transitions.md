# Spike: Domain Transition Mechanics

**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Small  
**Priority:** Medium

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| **Small** | **30 min** | **~20 queries** |
| Medium | 60 min | ~50 queries |
| Large | 120 min | ~100 queries |

*This spike is Small.*

---

## Spike Intent

Research how an artifact transitions between domains. For example, how does an observation (Observe) become a document (Write)?

---

## Research Questions

1. How exactly does an artifact move from Observe → Write?
2. What triggers a domain transition?
3. Is this a new project or a continuation?
4. How do PKM systems handle progressive summarization?
5. What artifacts carry over between domains?

---

## Where to Look

- PKM literature on progressive summarization (Tiago Forte)
- Zettelkasten literature notes → permanent notes
- Knowledge pipeline patterns

---

## Output Artifacts

1. Research report → `02-refine-domains-research-02-domain-transitions-report.md`
2. Transition patterns documented
3. Proposed mechanics for domain handoff
4. Follow-up stories if needed

---

## Definition of Done

- [ ] At least 3 transition patterns documented
- [ ] Trigger conditions identified
- [ ] Artifact handoff rules proposed
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 30-minute time box
3. Commit changes to your branch with message: `docs: spike domain transitions research`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: Domain Transition Mechanics" --body-file <handoff.md> --base main
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
