# Spike Report: SOD Template Research

**Project:** opinions-framework
**Spike:** #76 - SOD Template Research
**Date:** 2025-12-28
**Status:** Complete

---

## Executive Summary

Researched Solution Overview Documents (SOD) and compared them to PRDs, BRDs, RFCs, and Design Docs. Found that SOD is not a standardized industry term—Praxis can define it as a lightweight formalization artifact that combines the best elements of existing document types while staying minimal.

---

## Comparison Matrix

| Document Type | Audience | Focus | Typical Length | When Used |
|---------------|----------|-------|----------------|-----------|
| **BRD** (Business Requirements) | Executives, stakeholders | Business case, goals, constraints | 5-15 pages | Before funding approval |
| **PRD** (Product Requirements) | Product, Engineering, Design | What to build, user stories, success metrics | 3-10 pages | Before development |
| **RFC** (Request for Comments) | Engineering peers | Technical approach, tradeoffs, alternatives | 2-8 pages | Before implementation |
| **Design Doc** | Engineering team | How to build, architecture, APIs | 5-15 pages | During implementation planning |
| **SOD** (Praxis) | Self + collaborators | Solution boundaries, constraints, done criteria | 1-3 pages | At Formalize stage |

### Key Insight

PRDs describe "a problem that needs to be solved" while RFCs describe "a solution you'd like feedback on." The SOD should bridge both: it documents the *bounded solution* that was shaped, not the full problem space or implementation details.

---

## What Makes a Good SOD?

Based on research into what makes effective documentation:

### 1. Background/Context (Required)
From HashiCorp's RFC template: "As a newcomer to this project, can I read the background section and get full context on why this change is necessary?"

### 2. Bounded Scope (Required)
Shape Up's pitch format includes "Appetite"—how much time/effort is worth spending. The SOD should define what's *in* and *out* explicitly.

### 3. Solution Sketch (Required)
Concrete enough to act on, abstract enough to allow flexibility. Not pixel-perfect designs, but key elements.

### 4. Rabbit Holes & No-Gos (Required)
From Shape Up: explicitly call out traps to avoid and things that are specifically excluded.

### 5. Done Criteria (Required)
How do we know when this is finished? What does success look like?

---

## Minimum Viable SOD

Based on the research, here's the proposed minimum viable SOD structure:

```markdown
# Solution Overview: [Name]

## Background
Why are we doing this? What problem does it solve?

## Appetite
How much effort is appropriate? (Small/Medium/Large or time-boxed)

## Solution
What are we building? Key elements only—not implementation details.

## Boundaries
### In Scope
- What's included

### Out of Scope
- What's explicitly excluded

### Rabbit Holes
- Known traps to avoid

## Done Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Design Decisions

1. **One page preferred, two max.** If it's longer, the scope is probably too big.
2. **No implementation details.** That's what Design Docs and code are for.
3. **Explicit exclusions.** "Out of Scope" and "Rabbit Holes" prevent scope creep.
4. **Checkable done criteria.** Binary yes/no, not fuzzy goals.

---

## Comparison to Shape Up Pitch

The SOD is very similar to a Shape Up pitch:

| Shape Up Pitch | Praxis SOD |
|----------------|------------|
| Problem | Background |
| Appetite | Appetite |
| Solution | Solution |
| Rabbit Holes | Boundaries: Rabbit Holes |
| No-gos | Boundaries: Out of Scope |
| (implicit) | Done Criteria |

The main addition is explicit **Done Criteria**, which Shape Up handles through fixed time boxes rather than explicit acceptance criteria.

---

## Required vs Optional Sections

| Section | Status | Rationale |
|---------|--------|-----------|
| Background | Required | Establishes "why" |
| Appetite | Required | Prevents gold-plating |
| Solution | Required | Describes "what" |
| In Scope | Required | Clarifies boundaries |
| Out of Scope | Required | Prevents scope creep |
| Rabbit Holes | Optional | Not all projects have known traps |
| Done Criteria | Required | Enables objective completion |
| Alternatives Considered | Optional | Useful for controversial decisions |

---

## Sources

- [Companies Using RFCs or Design Docs - The Pragmatic Engineer](https://blog.pragmaticengineer.com/rfcs-and-design-docs/)
- [HashiCorp RFC Template](https://works.hashicorp.com/articles/rfc-template)
- [What is a Product Requirements Document - Atlassian](https://www.atlassian.com/agile/product-management/requirements)
- [Write the Pitch - Shape Up](https://basecamp.com/shapeup/1.5-chapter-06)
- [6 Requirements Specification Formats - Aqua Cloud](https://aqua-cloud.io/requirements-specification-formats-brd-frd-urs/)

---

## Follow-Up Recommendations

1. **Create SOD template file** in `docs/templates/sod.md`
2. **Update lifecycle.md** to reference SOD template
3. **Add SOD validation** to `praxis validate` (check required sections exist)
