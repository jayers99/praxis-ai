# Spike: AI Permission Matrices by Domain

**Project:** opinions-framework  
**Type:** Spike (research/exploration)  
**Size:** Medium  
**Priority:** Medium

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 30 min | ~20 queries |
| **Medium** | **60 min** | **~50 queries** |
| Large | 120 min | ~100 queries |

*This spike is Medium.*

---

## Spike Intent

Research what AI operations should be allowed in each domain. Different domains have different risk profiles for AI assistance.

---

## Research Questions

1. What AI operations are allowed in each domain?
2. How do creative domains (Create) differ from technical (Code)?
3. What AI governance patterns exist in industry?
4. How do ethical considerations differ by domain?
5. What's the relationship between privacy level and AI permissions?

---

## Where to Look

- AI governance literature
- Creative AI ethics (copyright, authorship)
- AI-assisted development best practices
- Enterprise AI policy frameworks

---

## Output Artifacts

1. Research report → `02-refine-domains-research-03-ai-permissions-report.md`
2. Permission matrix (Domain × AI Operation)
3. Risk assessment per domain
4. Follow-up stories if needed

---

## Definition of Done

- [ ] AI permissions defined for each of 5 domains
- [ ] Permission matrix created
- [ ] Risk considerations documented
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 60-minute time box
3. Commit changes to your branch with message: `docs: spike ai permissions research`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: AI Permission Matrices by Domain" --body-file <handoff.md> --base main
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
