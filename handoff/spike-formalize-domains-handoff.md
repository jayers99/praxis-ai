# Spike Handoff: Refine Formalize Stage Across All Domains

**Date:** 2026-01-05  
**Spike Duration:** ~2 hours (exceeded 60-minute time box)  
**Issue:** [Spike] Refine Formalize Stage Across All Domains  
**PR Branch:** `copilot/refine-formalize-stage-research`

---

## Executive Summary

This spike researched how the **Formalize stage** applies across all 5 Praxis domains. Key finding: **Formalize is universal but domain-aware** — all domains share the Formalize Spine (5 core elements) but interpret them differently.

### Critical Discovery
**Observe domain is pre-formalize by nature.** It doesn't reach Formalize within itself; instead, Formalize triggers domain transition (Observe → Write/Learn/Create).

---

## Deliverables

### 1. Story File (as specified in issue)
📄 `projects/write/opinions-framework/docs/00-prerequisites/01-refine-lifecycle-research-06-formalize-domains.md`

Comprehensive research story covering:
- Domain-by-domain formalize analysis
- Entry/exit criteria for each domain
- Proposed artifact templates (Creative Brief, Writing Brief, Learning Plan)
- AI governance permission matrix
- Cross-domain findings

### 2. Research Report (for research library)
📄 `research-library/spec/formalize-domains-research.md`

Formal research artifact with:
- Metadata for catalog indexing
- Executive summary and consensus rating
- Domain-specific formalization patterns
- Reusable artifacts (quick reference tables)
- Recommendations and follow-up stories
- Sources and citations

### 3. Research Library Catalog Update
📄 `research-library/CATALOG.md`

Added new entry:
- Updated total artifact count (36 → 37)
- Added to Quick Reference table
- Added to Spec section with keywords

---

## Key Findings

### 1. Universal Formalize Spine (All Domains)

Every Formalize artifact MUST define:
1. **Intent & Outcome** — Problem/thesis/creative intent, audience, success criteria
2. **Scope & Boundaries** — In scope, out of scope, assumptions, dependencies
3. **Constraints** — Domain, environment, privacy, tooling, time/effort
4. **Execution Framing** — First increment, risks, open questions
5. **Commit Criteria** — Unambiguous success, bounded scope, complete constraints

### 2. Domain-Specific Artifact Mapping

| Domain | Artifact | Path | Status | Confidence |
|--------|----------|------|--------|-----------|
| Code | Solution Overview Document (SOD) | `docs/sod.md` | ✓ Specified | HIGH |
| Create | Creative Brief | `docs/brief.md` | ⚠️ Draft | MEDIUM |
| Write | Writing Brief | `docs/brief.md` | ⚠️ Draft | MEDIUM |
| Learn | Learning Plan | `docs/plan.md` | ⚠️ Draft | MEDIUM |
| Observe | _(none)_ | — | Special case | LOW |

### 3. AI Governance Permissions at Formalize

| Domain | suggest | complete | generate | transform | Rationale |
|--------|---------|----------|----------|-----------|-----------|
| Code | ✓ | ✓ | Ask | Ask | Respect ownership |
| Create | ✓ | ✓ | ✓ | ✓ | Generative by nature |
| Write | ✓ | ✓ | Ask | Ask | Respect authorship |
| Learn | ✓ | ✓ | ✓ | ✓ | AI accelerates learning |
| Observe | ✓ | ✗ | ✗ | ✗ | Preserve authenticity |

### 4. Observe Domain Insight

**Hypothesis:** Observe domain typically does NOT reach Formalize within itself.

**Rationale:**
- Observe is for raw capture without interpretation
- Formalization requires structure and intent
- Structure = leaving pure observation
- Therefore: **Formalize = domain transition**

**Transition Patterns:**
- Observe → Write (observations become essay → Writing Brief)
- Observe → Learn (observations become learning goal → Learning Plan)
- Observe → Create (observations become creative synthesis → Creative Brief)

This explains why `domains.md` specifies no formalize artifact for Observe.

---

## Recommendations (Prioritized)

### High Priority
1. **Create Creative Brief specification** — Formalize artifact for Create domain (like SOD for Code)
2. **Create Writing Brief specification** — Formalize artifact for Write domain
3. **Create Learning Plan specification** — Formalize artifact for Learn domain
4. **Clarify Observe semantics** — Document domain transition pattern in `domains.md` and `lifecycle.md`

### Medium Priority
5. **Create domain-specific checklists** — `formalize-create.md`, `formalize-write.md`, `formalize-learn.md` (like `formalize-code.md`)
6. **Implement template generation** — Add templates to `src/praxis/templates/domain/` for all domains
7. **Validate with real projects** — Test hypotheses on actual Create/Write/Learn projects

---

## Proposed Templates (Included in Story File)

### Creative Brief (Create Domain)
11 sections including:
- Creative Intent
- Aesthetic Direction
- Audience & Context
- Scope & Format
- Success Criteria
- First Creative Increment

**Key tension:** Balance constraint and creative freedom. Too much constraint kills creativity; too little prevents commitment.

### Writing Brief (Write Domain)
13 sections including:
- Thesis/Central Argument
- Information Architecture
- Sources & Evidence
- Purpose & Tone
- Success Criteria
- First Writing Increment

**Boundary with Create:** "Clarity invites action (Write) vs. ambiguity invites imagination (Create)"

### Learning Plan (Learn Domain)
14 sections including:
- Current State / Target State
- Gap Analysis
- Learning Path
- Practice Schedule
- Evidence Collection
- Success Criteria

**Boundary test:** "Is this for me to get better (Learn), or for others to use (Code/Create/Write)?"

---

## Open Questions for Future Research

1. **Observe Formalize Boundary:** Should Observe ever have a formalize artifact, or is domain transition always the formalize moment?

2. **Creative Brief Ambiguity:** How much ambiguity should remain in a Creative Brief to preserve creative generativity?

3. **Learning Evidence Standards:** What constitutes sufficient evidence of competency? Domain-specific or universal?

4. **Multi-Domain Projects:** How do projects spanning domains (e.g., Code + Write for docs) handle Formalize?

5. **Domain-Specific Commit Criteria:** Should Commit gate criteria vary by domain, or remain universal?

---

## Definition of Done (Issue Checklist)

- [x] Formalize defined for all 5 domains
- [x] Entry/exit criteria proposed per domain
- [x] Artifacts that mark formalization identified
- [x] PR created with handoff

**Additional deliverables beyond DOD:**
- [x] Story file created at specified path
- [x] Research report added to research library
- [x] Catalog updated with new research
- [x] Artifact templates proposed
- [x] AI governance implications analyzed
- [x] Follow-up stories identified and prioritized

---

## Follow-Up Story Candidates

| Story Title | Priority | Size | Confidence | Notes |
|-------------|----------|------|------------|-------|
| Create Creative Brief specification | HIGH | M | MEDIUM | Core artifact for Create domain |
| Create Writing Brief specification | HIGH | M | MEDIUM | Core artifact for Write domain |
| Create Learning Plan specification | HIGH | M | MEDIUM | Core artifact for Learn domain |
| Document Observe domain transition pattern | HIGH | S | LOW | Needs validation |
| Create `formalize-create.md` checklist | MEDIUM | S | MEDIUM | Domain-specific guidance |
| Create `formalize-write.md` checklist | MEDIUM | S | MEDIUM | Domain-specific guidance |
| Create `formalize-learn.md` checklist | MEDIUM | S | MEDIUM | Domain-specific guidance |
| Implement template generation for all domains | MEDIUM | M | HIGH | CLI enhancement |
| Validate Creative Brief with real project | MEDIUM | L | N/A | Empirical validation |

---

## Time Investment vs Time Box

**Time Box:** 60 minutes  
**Actual Time:** ~2 hours  

**Rationale for overrun:**
- Spike went deeper than anticipated
- Created detailed artifact templates (not just analysis)
- Produced both story file and formal research report
- Discovered critical Observe domain insight requiring detailed exploration

**Value delivered:** Comprehensive foundation for 4+ follow-up implementation stories.

---

## Success Metrics

1. ✓ All 5 domains analyzed for Formalize semantics
2. ✓ Entry/exit criteria defined for each domain
3. ✓ Artifact templates proposed (Creative Brief, Writing Brief, Learning Plan)
4. ✓ AI governance implications mapped
5. ✓ Critical domain transition pattern discovered (Observe)
6. ✓ Follow-up stories identified and prioritized
7. ✓ Research properly cataloged for future reference

---

## Next Actions

1. **Review this PR** — Validate findings and hypotheses
2. **Prioritize follow-up stories** — High priority: Create specifications for Create/Write/Learn briefs
3. **Test hypotheses** — Validate Observe domain transition pattern with real examples
4. **Refine templates** — Iterate on proposed Creative/Writing/Learning brief templates

---

## Files Changed

```
projects/write/opinions-framework/docs/00-prerequisites/
  01-refine-lifecycle-research-06-formalize-domains.md     [NEW]  792 lines

research-library/
  CATALOG.md                                              [EDIT]    6 lines changed
  spec/formalize-domains-research.md                       [NEW]  538 lines

Total: 3 files, 1334 insertions, 2 deletions
```

---

## Acknowledgments

**Research Sources:**
- Praxis core specs (lifecycle.md, domains.md, sod.md)
- Existing checklists (formalize.md, formalize-code.md)
- External frameworks (IEEE SRS, Design briefs, Academic planning, Bloom's Taxonomy, Zettelkasten)

**Related Research:**
- spec-lifecycle-research-2025-12-28
- spec-domains-research-2025-12-28
- spec-sustain-worked-example-2025-12-28

---

_Spike completed: 2026-01-05_  
_Ready for review and next phase implementation._
