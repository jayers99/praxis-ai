# Spike 02: Domain Definitions Research Report (Consolidated)

**Date:** 2025-12-28  
**Status:** Complete  
**Spikes Merged:** Main research + Subtype Taxonomies + Domain Transitions + AI Permissions

---

## Executive Summary

This consolidated report covers all domain research for Praxis. Key findings:
- 5 domains validated with industry-standard taxonomies
- 28 subtypes defined across all domains
- 4 domain transition patterns identified
- AI permission matrix established with 6 operation categories
- Boundary criteria refined for adjacent domains

---

## Part 1: Domain Definitions

### 1. Code Domain

**Definition:** Functional systems and tools  
**Confidence:** HIGH

#### Prior Art

| Source | Key Insight |
|--------|-------------|
| OSS Taxonomy (Nesbitt) | Faceted approach: domain, role, technology, audience |
| Wikipedia | Application, System, Programming tools |
| SWEBOK | Construction (20%), Design (20%), Requirements (16%) |

#### Subtypes

| Subtype | Description |
|---------|-------------|
| `code.cli` | Command-line tools and utilities |
| `code.library` | Reusable packages and modules |
| `code.api` | HTTP/REST/GraphQL services |
| `code.webapp` | Web applications with UI |
| `code.infrastructure` | IaC, DevOps, platform tooling |
| `code.script` | One-off automation scripts |

#### Boundary

- **In scope:** Output is executable/runnable code
- **Out of scope:** AI-generated art (even if tooling is code), documentation-only

---

### 2. Create Domain

**Definition:** Aesthetic and expressive output (any medium)  
**Confidence:** HIGH

#### Prior Art

| Source | Key Insight |
|--------|-------------|
| Taxonomy of Creative Design | Progression from imitation to original creation |
| UX Magazine | Stylistic, Functional, Strategic, Innovative design |
| Springer Research | Aesthetics = sensory + cognitive response |

#### Subtypes

| Subtype | Description |
|---------|-------------|
| `create.visual` | Static images, illustrations, graphics |
| `create.audio` | Music, sound design, podcasts |
| `create.video` | Film, animation, motion graphics |
| `create.interactive` | Games, installations, experiences |
| `create.generative` | AI-generated or algorithmic art |
| `create.design` | UI/UX, product design, crafts |

#### Boundary

- **In scope:** Primary purpose is aesthetic/emotional response
- **Out of scope:** Functional documentation, executable code
- **Key test:** "Does ambiguity invite imagination, or does clarity invite action?"

---

### 3. Write Domain

**Definition:** Structured externalized thought  
**Confidence:** MEDIUM (boundary with Create needs attention)

#### Prior Art

| Source | Key Insight |
|--------|-------------|
| Four Rhetorical Modes | Expository, Descriptive, Persuasive, Narrative |
| IEEE Technical Writing | Translates specialized knowledge into accessible information |
| Business Writing | Reports, emails, proposals, white papers |

#### Subtypes

| Subtype | Description |
|---------|-------------|
| `write.technical` | Documentation, tutorials, specs |
| `write.business` | Reports, proposals, memos |
| `write.narrative` | Essays, personal stories (not fiction) |
| `write.academic` | Research papers, theses |
| `write.journalistic` | Articles, news, long-form journalism |

**Note:** Fiction and poetry belong to **Create**, not Write.

#### Boundary

- **In scope:** Primary purpose is information transfer or argumentation
- **Out of scope:** Primary purpose is aesthetic/emotional response
- **Key test:** "Clarity invites action (Write) vs. ambiguity invites imagination (Create)"

---

### 4. Observe Domain

**Definition:** Capture without judgment or refinement  
**Confidence:** HIGH

#### Prior Art

| Source | Key Insight |
|--------|-------------|
| Zettelkasten (Luhmann) | 90,000+ index cards, web of linked notes |
| BASB (Forte) | PARA system, capture now, organize later |
| PKM Research | Raw capture = initial collection without processing |

#### Subtypes

| Subtype | Description |
|---------|-------------|
| `observe.notes` | Text-based raw capture |
| `observe.bookmarks` | Links, references, citations |
| `observe.clips` | Screenshots, quotes, snippets |
| `observe.logs` | Journals, daily notes, activity records |
| `observe.captures` | Photos, recordings, sensory data |

#### Boundary

- **In scope:** Raw capture, minimal processing, no synthesis
- **Out of scope:** Analysis, interpretation, structured output
- **Key test:** "Captured for later processing, or processed now?"

---

### 5. Learn Domain

**Definition:** Internal model and skill formation  
**Confidence:** HIGH

#### Prior Art

| Source | Key Insight |
|--------|-------------|
| Bloom's Taxonomy | Remember → Understand → Apply → Analyze → Evaluate → Create |
| Anderson & Krathwohl | Factual, Conceptual, Procedural, Metacognitive knowledge |
| Kolb's Cycle | Experience → Reflect → Conceptualize → Experiment |

#### Subtypes

| Subtype | Description |
|---------|-------------|
| `learn.skill` | Procedural knowledge, how-to |
| `learn.concept` | Theoretical understanding, mental models |
| `learn.practice` | Exercises, drills, deliberate practice |
| `learn.course` | Structured learning path |
| `learn.exploration` | Self-directed discovery |

#### Boundary

- **In scope:** Goal is internal capability formation
- **Out of scope:** Production-grade artifacts for external use
- **Key test:** "Is this for me to get better, or for others to use?"

---

## Part 2: Domain Transition Mechanics

### Transition Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Promotion** | Artifact matures into new domain | Observe → Write (notes become essay) |
| **Derivation** | New artifact references original | Code → Write (implementation spawns docs) |
| **Decomposition** | Artifact splits across domains | Write → Write + Code (blog + examples) |
| **Aggregation** | Multiple artifacts combine | Observe × 3 → Write (notes → synthesis) |

### Transition Triggers

| Trigger | Description |
|---------|-------------|
| Intent change | Purpose shifts from capture to create |
| Quality bar | Artifact exceeds domain's natural ceiling |
| Audience change | From self to others |
| Formalization | Artifact requires domain-specific SOD |
| Time investment | Significant effort signals transition |

### Progressive Summarization Model

| Layer | Action | Domain |
|-------|--------|--------|
| L1 | Raw capture | Observe |
| L2 | Bold key passages | Observe (enriched) |
| L3 | Highlight within bold | Observe → Write |
| L4 | Executive summary | Write |
| L5 | Remix into new form | Write → Create or Code |

### Transition Requirements

| From → To | Requirement |
|-----------|-------------|
| Observe → Write | Summary/thesis statement present |
| Observe → Learn | Learning goal identified |
| Write → Code | Technical specification present |
| Learn → Code | Working prototype exists |
| * → Create | Aesthetic intent declared |

---

## Part 3: AI Permission Matrix

### Operation Categories

| Operation | Description | Risk Level |
|-----------|-------------|------------|
| `suggest` | Propose content for human review | Low |
| `complete` | Auto-complete in-progress work | Medium |
| `generate` | Create new content from prompt | Medium |
| `transform` | Modify existing content | High |
| `execute` | Run generated code/commands | Critical |
| `publish` | Make content externally visible | Critical |

### Domain × Operation Matrix

| Operation | Code | Create | Write | Learn | Observe |
|-----------|:----:|:------:|:-----:|:-----:|:-------:|
| `suggest` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `complete` | ✓ | ✓ | ✓ | ✓ | ✗ |
| `generate` | ? | ✓ | ? | ✓ | ✗ |
| `transform` | ? | ✓ | ? | ✓ | ✗ |
| `execute` | ? | — | — | — | — |
| `publish` | ? | ? | ? | ? | ? |

**Legend:** ✓ = allowed, ? = ask user, ✗ = blocked, — = N/A

*Observe domain blocks AI generation to preserve raw capture authenticity.*

### Privacy Level Modifiers

| Privacy Level | Effect |
|---------------|--------|
| Public | `generate`/`transform` → Ask, `publish` → ✓ |
| Public-Trusted | Default permissions |
| Personal | Default permissions |
| Confidential | All operations → Ask |
| Restricted | `generate`/`transform` → ✗, `execute` → ✗ |

### Environment Modifiers

| Environment | Effect |
|-------------|--------|
| Home | Default permissions |
| Work | `execute` → Ask, `publish` → Ask |

### Risk by Domain

| Domain | Risk Level | Key Concerns |
|--------|------------|--------------|
| Code | High | Security vulnerabilities, secrets, license contamination |
| Create | Medium | Copyright, style plagiarism, deepfakes |
| Write | Medium | Plagiarism, misinformation, voice loss |
| Learn | Low | Over-reliance, incorrect information |
| Observe | Minimal | Contaminated capture, lost authenticity |

---

## Part 4: Boundary Resolution

### Write vs. Create

| Content Type | Domain | Rationale |
|--------------|--------|-----------|
| Technical docs | Write | Clarity → action |
| Business writing | Write | Information transfer |
| Essays | Write | Argumentation |
| Fiction | Create | Ambiguity → imagination |
| Poetry | Create | Aesthetic/emotional |
| Creative nonfiction | Create | Narrative purpose dominates |

### Observe vs. Learn

| Activity | Domain | Rationale |
|----------|--------|-----------|
| Taking a photo | Observe | Raw capture |
| Highlighting a book | Observe | Capture for later |
| Summarizing in own words | Learn | Active processing |
| Practice exercises | Learn | Skill formation |
| Making connections | Learn | Conceptualization |

**Key insight (Kolb):** Observation becomes learning when you move from "Concrete Experience" to "Reflective Observation" with intent to internalize.

### Hybrid Projects

- Projects can span domains
- Each artifact belongs to exactly one domain
- Domain determines: storage, AI permissions, quality bar
- Promotion across domains requires explicit stage transition

---

## Sources

### Code Domain
- [OSS Taxonomy - Nesbitt](https://nesbitt.io/2025/11/29/oss-taxonomy.html)
- [Software categories - Wikipedia](https://en.wikipedia.org/wiki/Software_categories)
- [Taxonomies in SE - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0950584917300472)

### Create Domain
- [Taxonomy of Creative Design](http://www.senseandsensation.com/2012/03/taxonomy-of-creative-design.html)
- [Creative Technology Taxonomy - Blair Neal](https://ablairneal.com/a-creative-technology-taxonomy)
- UNESCO Cultural Industries Classification

### Write Domain
- [Types of Writing - Grammarly](https://www.grammarly.com/blog/writing-techniques/types-of-writing/)
- [Technical Writing - IEEE](https://ieeexplore.ieee.org/iel2/766/908/00024018.pdf)

### Observe Domain
- [Progressive Summarization - Forte Labs](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)
- [PKM Guide - Nick Ang](https://nickang.com/2020-07-05-personal-knowledge-management-system/)

### Learn Domain
- [Bloom's Taxonomy - Wikipedia](https://en.wikipedia.org/wiki/Bloom's_taxonomy)
- [Experiential Learning - Cogn-IQ](https://www.cogn-iq.org/learn/theory/experiential-learning/)

### AI Permissions
- [VS Code Copilot Security](https://code.visualstudio.com/docs/copilot/security)
- [EU AI Code of Practice](https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai)

### Transitions
- [Artifact-centric BPM - Wikipedia](https://en.wikipedia.org/wiki/Artifact-centric_business_process_model)
- [FHIR Artifact Lifecycle](https://build.fhir.org/ig/HL7/crmi-ig/artifact-lifecycle.html)

---

## Time Spent

| Spike | Budget | Actual |
|-------|--------|--------|
| Main domain research | 30 min | ~30 min |
| Subtype taxonomies | 30 min | ~30 min |
| Domain transitions | 15 min | ~15 min |
| AI permissions | 30 min | ~30 min |
| **Consolidation** | — | ~10 min |
| **Total** | ~105 min | ~115 min |
