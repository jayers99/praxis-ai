# Spike: Regression Trigger Detection

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

Research whether stage regressions can be detected automatically. Praxis allows regression (unlike Stage-Gate's "kill or continue"), but detection relies on human judgment. Can this be automated?

---

## Research Questions

1. Can regressions be detected automatically?
2. What signals indicate premature stage advancement?
3. How do other frameworks handle "going back"?
4. What heuristics could trigger regression alerts?
5. Can `praxis validate` detect scope creep during Execute?

---

## Where to Look

- Stage-Gate failure analysis
- Agile/Scrum scope creep detection
- Project management warning signs literature
- AI code review tools (for scope drift detection)

---

## Output Artifacts

1. Research report → `01-refine-lifecycle-research-04-regression-detection-report.md`
2. List of regression trigger heuristics
3. Feasibility assessment for automation
4. Follow-up stories if needed

---

## Definition of Done

- [ ] At least 5 regression triggers identified
- [ ] Feasibility of automation assessed
- [ ] Detection heuristics documented
- [ ] Time box respected
- [ ] Handoff via PR

---

## Agent Instructions

1. Read this issue completely
2. Execute the spike respecting the 30-minute time box
3. Commit changes to your branch with message: `docs: spike 04 regression detection research`
4. Create a PR with handoff summary:
   ```
   gh pr create --title "Spike: Regression Trigger Detection" --body-file <handoff.md> --base main
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
