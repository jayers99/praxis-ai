# Spike Report: Regression Trigger Detection

**Project:** opinions-framework
**Spike:** #78 - Regression Trigger Detection
**Date:** 2025-12-28
**Status:** Complete

---

## Executive Summary

Researched whether stage regressions can be detected automatically. Found that partial automation is feasible, particularly for Code domain scope creep detection. Other domains require more human judgment, but heuristics can raise alerts for manual review.

---

## Regression Triggers Identified

### 1. Scope Expansion During Execute

**Signal:** New work items added without removing equivalent work.

**Detection Method:**
- Track issue/story count at Formalize → Execute transition
- Alert if net new items added during Execute
- Burndown charts showing scope increase

**Automation Feasibility:** High (can be automated via issue tracker APIs)

---

### 2. Requirements Drift

**Signal:** Acceptance criteria modified after Formalize.

**Detection Method:**
- Snapshot SOD/acceptance criteria at stage transition
- Diff on any modifications
- Alert on changes to "In Scope" or "Done Criteria"

**Automation Feasibility:** High (git diff on SOD file)

---

### 3. Timeline Slippage Patterns

**Signal:** Repeated deadline extensions or "just one more sprint."

**Detection Method:**
- Track original deadline vs. current deadline
- Count extension requests
- Alert after N extensions (configurable threshold)

**Automation Feasibility:** Medium (requires deadline tracking)

---

### 4. Solution Architecture Changes

**Signal:** Fundamental approach changes during Execute.

**Detection Method:**
- Monitor for new ADRs (Architecture Decision Records)
- Large-scale refactoring PRs during Execute
- New dependencies added outside initial scope

**Automation Feasibility:** Medium (can detect new ADRs, large PRs)

---

### 5. Stakeholder Churn

**Signal:** New stakeholders joining with new requirements.

**Detection Method:**
- Track contributor list at Formalize
- Alert when new stakeholders introduce scope items
- Meeting frequency increase

**Automation Feasibility:** Low (requires meeting/communication analysis)

---

### 6. "One More Feature" Pattern

**Signal:** Informal requests accumulating without formal scope change.

**Detection Method:**
- Slack/email analysis for phrases like "can we also," "while you're at it"
- Tracking informal asks vs. formal backlog items

**Automation Feasibility:** Low (requires NLP on communications)

---

### 7. Budget/Resource Overruns

**Signal:** Spending more than allocated without scope reduction.

**Detection Method:**
- Track hours/cost vs. budget
- Alert at 80% threshold
- Compare to original estimate

**Automation Feasibility:** High (if time tracking exists)

---

### 8. Rabbit Hole Entry

**Signal:** Work diverging into explicitly excluded areas.

**Detection Method:**
- Match PR descriptions/commit messages against "Out of Scope" items
- Keyword matching on rabbit holes list
- Code changes in excluded areas

**Automation Feasibility:** Medium (keyword matching feasible)

---

## Automation Feasibility Assessment

| Trigger | Automation Level | Implementation Complexity |
|---------|------------------|---------------------------|
| Scope expansion | High | Low - count issues |
| Requirements drift | High | Low - git diff |
| Timeline slippage | Medium | Medium - track dates |
| Architecture changes | Medium | Medium - detect ADRs |
| Budget overruns | High | Low - compare numbers |
| Rabbit hole entry | Medium | Medium - keyword match |
| Stakeholder churn | Low | High - requires integrations |
| Informal requests | Low | High - requires NLP |

### Recommended Priority

1. **Start with:** Requirements drift detection (diff SOD on each commit)
2. **Then add:** Scope expansion counting (issue tracker integration)
3. **Later:** Architecture change detection (ADR monitoring)

---

## Detection Heuristics for `praxis validate`

```yaml
regression_heuristics:
  # High confidence - can automate
  sod_modified_during_execute:
    trigger: "SOD file changed while stage >= execute"
    action: "warn"
    message: "SOD modified during Execute - possible regression to Formalize"

  scope_items_increased:
    trigger: "Issue count > count at formalize transition"
    action: "warn"
    message: "Scope expanded during Execute - review for regression"

  # Medium confidence - alert for human review
  new_adr_during_execute:
    trigger: "New ADR created while stage >= execute"
    action: "info"
    message: "Architecture decision made during Execute - may indicate scope issue"

  # Configurable thresholds
  deadline_extensions:
    trigger: "deadline_extension_count > threshold"
    threshold: 2
    action: "warn"
    message: "Multiple deadline extensions - consider regression to Formalize"
```

---

## How Other Frameworks Handle Regression

### Stage-Gate (Cooper)
- No regression allowed—gates are "go/kill" decisions
- Failed gates = project killed
- Praxis is more flexible by design

### Agile/Scrum
- Scope changes handled via backlog refinement
- Sprint scope is locked, but backlog can change
- Retrospectives catch process issues

### Shape Up
- Fixed time boxes act as "circuit breakers"
- If not done in 6 weeks, project is killed or re-pitched
- No scope extension by design

### Key Insight
Praxis is unique in explicitly *allowing* regression while still detecting it. Other frameworks either forbid regression (Stage-Gate) or handle it implicitly (Agile backlog churn).

---

## Proposed Implementation

### Phase 1: Manual Alerts
- Add regression warning messages to `praxis status`
- Detect SOD modifications during Execute
- Show time-since-last-stage-change

### Phase 2: Automated Detection
- Add `praxis validate --check-regression` flag
- Integrate with git history for SOD diffs
- Track issue counts if integration available

### Phase 3: Predictive Alerts
- Burndown trend analysis
- Deadline slip pattern matching
- Integration with project management tools

---

## Sources

- [Scope Creep in Project Management - Monday.com](https://monday.com/blog/project-management/keep-scope-creep-undermining-project/)
- [Project Management Scope Creep - TrueProject](https://www.trueprojectinsight.com/blog/project-office/project-management-scope-creep)
- [How to Handle Scope Creep in Agile - DE Project Manager](https://deeprojectmanager.com/handle-scope-creep-in-agile-projects/)
- [4 Ways to Deal with Scope Creep - Atlassian](https://www.atlassian.com/blog/inside-atlassian/4-how-tos-dealing-with-scope-creep)
- [Reduce Scope Creep in Agile - Tempo](https://www.tempo.io/blog/scope-creep-in-agile)

---

## Follow-Up Recommendations

1. **Add regression detection** to `praxis validate` (SOD diff check)
2. **Create issue tracker integration spec** for scope counting
3. **Add time-since-stage-change** to `praxis status` output
4. **Define regression severity levels** (info vs. warn vs. error)
