# Story: Refine Domain Definitions

**Project:** opinions-framework  
**Size:** Medium  
**Priority:** High (blocks opinion research)  
**Depends on:** 01-refine-lifecycle-story

---

## Summary

Review and refine the five domain definitions to ensure they are:
1. **Distinct** — No overlap or ambiguity between domains
2. **Complete** — Cover all reasonable work types
3. **Subtype-ready** — Support hierarchical inheritance for opinions

---

## Problem Statement

The opinions framework will generate guidance for each Domain × Stage cell. If domain definitions are fuzzy or overlap, the resulting opinions will conflict or leave gaps.

**Current domains:** Code, Create, Write, Observe, Learn

**Current state:** Domain definitions exist in `docs/domains.md` but may lack:
- Clear boundary criteria (when is something Code vs. Create?)
- Subtype taxonomy (what are the recognized subtypes per domain?)
- Formalization artifact requirements per domain

---

## Acceptance Criteria

- [ ] Each domain has explicit **boundary criteria** (what qualifies, what doesn't)
- [ ] Each domain has a **primary intent** (what are you trying to produce?)
- [ ] Each domain has a **formalize artifact** requirement (SOD, brief, plan, etc.)
- [ ] Each domain has initial **subtype taxonomy** (at least top-level categories)
- [ ] Domains are mutually exclusive (no work fits two domains)
- [ ] Domains are collectively exhaustive (all reasonable work fits somewhere)
- [ ] Edge cases are documented (hybrid work, sequenced domains)

---

## Current Domain Definitions (Audit)

| Domain | Intent | Formalize Artifact | Subtypes? | Issues |
|--------|--------|-------------------|-----------|--------|
| **Code** | Functional systems | SOD | CLI, Library, API, etc. (partial) | Needs subtype formalization |
| **Create** | Aesthetic output | Creative Brief | Unknown | Unclear subtypes |
| **Write** | Structured thought | Writing Brief | Unknown | Overlaps with Create? |
| **Observe** | Raw capture | None | N/A | When does Observe become Learn? |
| **Learn** | Skill formation | Learning Plan | Unknown | Boundary with Write unclear |

### Boundary Questions to Resolve

1. **Write vs. Create** — Is a blog post Write or Create? Is fiction Write or Create?
2. **Observe vs. Learn** — When does observation become learning?
3. **Code vs. Create** — Is generative AI art tooling Code or Create?
4. **Hybrid work** — A project that writes documentation for code — is it Code or Write?

---

## Proposed Refinements

### Clearer Boundary Criteria

| Domain | Core Question | Boundary Test |
|--------|---------------|---------------|
| **Code** | "Does it execute?" | If the output runs/compiles, it's Code |
| **Create** | "Is the output primarily aesthetic?" | If quality is judged by taste/beauty, it's Create |
| **Write** | "Is the output primarily informational?" | If quality is judged by clarity/accuracy, it's Write |
| **Observe** | "Am I just capturing, not processing?" | If no synthesis or judgment, it's Observe |
| **Learn** | "Am I developing a capability?" | If the goal is personal skill, it's Learn |

### Subtype Taxonomy (First Pass)

**Code:**
```
Code
├── CLI
│   ├── CLI-Python
│   └── CLI-Node
├── Library
├── API
│   ├── REST
│   └── GraphQL
├── Web App
└── Infrastructure
```

**Create:**
```
Create
├── Visual
│   ├── Illustration
│   ├── Photography
│   └── Video
├── Audio
│   ├── Music
│   └── Podcast
└── Interactive
    └── Game
```

**Write:**
```
Write
├── Technical
│   ├── README
│   ├── API Docs
│   ├── Specification
│   └── ADR
├── Business
│   ├── RFP
│   ├── User Story
│   └── Report
└── Narrative
    ├── Blog Post
    └── Essay
```

**Learn:**
```
Learn
├── Skill
│   ├── Programming Language
│   └── Tool Proficiency
├── Concept
│   └── Domain Knowledge
└── Practice
    └── Deliberate Practice
```

**Observe:**
```
Observe
├── Notes
├── Bookmarks
├── Screenshots
└── Logs
```

---

## Tasks

1. [ ] Review current domain definitions in `docs/domains.md`
2. [ ] Resolve boundary ambiguities (Write vs. Create, etc.)
3. [ ] Draft initial subtype taxonomy per domain
4. [ ] Document hybrid work handling (sequenced domains)
5. [ ] Update `docs/domains.md` with refinements
6. [ ] Validate against existing projects (template-python-cli, render-run)
7. [ ] Review with stakeholder

---

## Non-Goals

- Not adding new domains (five are fixed for now)
- Not defining full opinion content (that's later stories)
- Not implementing subtype resolution in code (that's policy engine work)

---

## Dependencies

- 01-refine-lifecycle-story (stages should be clear before domains)

## Blocks

- 03-define-praxis-contract
- 04-define-opinion-structure
- All opinion research work

---

## Notes

This story addresses the concern: "We should look and see if there's a gap in our current domain definitions that could result in inferior results from this exercise."

The refinements should make domains clear enough that:
1. Any work can be unambiguously assigned to exactly one domain
2. Subtypes can inherit opinions from parent domain
3. AI can determine applicable opinions from `praxis.yaml` domain + subtype
