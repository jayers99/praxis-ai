# Spike 02: Domain Definitions Research Report

**Spike:** Research Domain Definitions
**Time Budget:** 30 minutes
**Date:** 2025-12-28

---

## Executive Summary

This spike researched prior art, industry taxonomies, and academic foundations for the 5 Praxis domains (Code, Create, Write, Observe, Learn). Key finding: our domain definitions align well with established frameworks, but boundary criteria need refinement—particularly Write vs. Create and Observe vs. Learn transitions.

---

## Domain Research

### 1. Code Domain

**Current Praxis Definition:** Functional systems and tools
**Confidence in Definition:** HIGH

#### Prior Art & Taxonomies

**OSS Taxonomy (2025)** - Andrew Nesbitt's multi-faceted classification:
- Uses CodeMeta standard extending schema.org
- Faceted approach: `domain:web-development`, `role:framework`, `technology:python`, `audience:developer`, `layer:backend`
- A project like Django spans 6+ facets simultaneously
- Source: [OSS Taxonomy](https://nesbitt.io/2025/11/29/oss-taxonomy.html)

**Wikipedia Software Categories:**
- Three broad classifications: Application software, System software, Programming tools
- Alternative 7-element taxonomy: platform/management, education/reference, home/entertainment, content/communication, operations/professional, manufacturing/delivery, line of business
- Source: [Software categories - Wikipedia](https://en.wikipedia.org/wiki/Software_categories)

**Academic SE Taxonomies:**
- Hierarchy (53%) and faceted analysis (39%) most common structures
- SWEBOK knowledge areas: construction (19.55%), design (19.55%), requirements (15.5%), maintenance (11.8%)
- Source: [ScienceDirect - Taxonomies in SE](https://www.sciencedirect.com/science/article/pii/S0950584917300472)

#### Subtype Taxonomy (Industry Standard)

| Category | Examples |
|----------|----------|
| CLI/Tools | Command-line utilities, build tools |
| Libraries | Shared code packages, SDKs |
| Frameworks | Web frameworks, testing frameworks |
| APIs/Services | REST APIs, microservices |
| Applications | Web apps, mobile apps, desktop apps |
| Infrastructure | IaC, deployment, monitoring |

#### Boundary Criteria

**In scope:** Output is executable/runnable code
**Out of scope:** AI-generated art (even if tooling is code), documentation-only

---

### 2. Create Domain

**Current Praxis Definition:** Aesthetic and expressive output (any medium)
**Confidence in Definition:** HIGH

#### Prior Art & Taxonomies

**Taxonomy of Creative Design** (senseandsensation.com):
- Progression from imitation to original creation
- Measures both form and content dimensions
- Analytical lens + skill development methodology
- Source: [Taxonomy of Creative Design](http://www.senseandsensation.com/2012/03/taxonomy-of-creative-design.html)

**UX Magazine Common Design Taxonomy:**
- **Stylistic design** - aesthetic appeal, visual style
- **Functional design** - feature set, UX, product design
- **Strategic design** - market positioning, demographics
- **Innovative design** - new product categories
- Source: [UX Magazine](https://uxmag.com/articles/a-common-design-taxonomy)

**Research on Creativity/Aesthetics/Functionality:**
- Functionality = opportunities for action, product performance
- Aesthetics = sensory response + cognitive reaction to product
- Aesthetic perception is "first response" to any product
- Source: [Springer Research](https://link.springer.com/article/10.1007/s00163-021-00366-9)

#### Subtype Taxonomy

| Medium | Examples |
|--------|----------|
| Visual | Illustration, photography, graphic design, UI design |
| Audio | Music composition, sound design, podcasts |
| Spatial | Architecture, interior design, 3D environments |
| Interactive | Games, installations, generative art |
| Motion | Animation, video, motion graphics |
| Written (aesthetic) | Poetry, fiction, creative nonfiction |

#### Boundary Criteria

**In scope:** Primary purpose is aesthetic/emotional response
**Out of scope:** Functional documentation, executable code
**Key distinction:** "In fiction, ambiguity invites imagination; in technical writing, clarity invites action"

---

### 3. Write Domain

**Current Praxis Definition:** Structured externalized thought
**Confidence in Definition:** MEDIUM (needs boundary clarification with Create)

#### Prior Art & Taxonomies

**Four Rhetorical Modes** (academic standard):
- Expository, Descriptive, Persuasive, Narrative
- Each requires different skills, serves different purposes
- Source: [Grammarly](https://www.grammarly.com/blog/writing-techniques/types-of-writing/)

**Technical Writing Definition (IEEE):**
- "Translates specialized knowledge into clear, accessible information"
- No figurative language, straightforward tone
- Discipline-specific jargon acceptable for expert audience
- Source: [IEEE Xplore](https://ieeexplore.ieee.org/iel2/766/908/00024018.pdf)

**Business Writing:**
- Reports, emails, proposals, white papers, minutes
- Expository: clear, concise communication
- Overlap with technical writing for specs/data
- Source: [Management.org](https://management.org/businesswriting/types-style-writing.htm)

#### Subtype Taxonomy

| Type | Primary Purpose | Praxis Domain |
|------|-----------------|---------------|
| Technical | Inform/instruct | Write |
| Business | Communicate/propose | Write |
| Academic | Argue/analyze | Write |
| Journalistic | Report/inform | Write |
| Essays | Explore/argue | Write |
| Fiction | Entertain/evoke | **Create** |
| Poetry | Express/evoke | **Create** |
| Creative nonfiction | Narrative + inform | **Boundary case** |

#### Boundary Criteria

**In scope:** Primary purpose is information transfer or argumentation
**Out of scope:** Primary purpose is aesthetic/emotional response
**Key test:** "Does clarity invite action, or does ambiguity invite imagination?"

---

### 4. Observe Domain

**Current Praxis Definition:** Capture without judgment or refinement
**Confidence in Definition:** HIGH

#### Prior Art & Taxonomies

**Personal Knowledge Management (PKM):**
- Zettelkasten (Niklas Luhmann): 90,000+ index cards, web of linked notes
- Building a Second Brain (Tiago Forte): PARA system (Projects, Areas, Resources, Archive)
- Source: [Nick Ang PKM](https://nickang.com/2020-07-05-personal-knowledge-management-system/), [Zettelkasten Forum](https://forum.zettelkasten.de/)

**Capture vs. Processing:**
- Raw capture = initial collection without processing
- Progressive summarization = later compression to key facts
- BASB principle: "Capture now, organize later"
- Source: [Elizabeth Butler MD](https://elizabethbutlermd.com/personal-knowledge-management/)

**Passive Learning Research:**
- Behaviorist view: learner as passive recipient of stimuli
- Cognitive view: even observation involves active mental processing
- Bandura: observational learning can be "very powerful"
- Source: [Teachers Institute](https://teachers.institute/), [Wikipedia Passive Learning](https://en.wikipedia.org/wiki/Passive_learning)

#### Subtype Taxonomy

| Type | Examples |
|------|----------|
| Visual capture | Photos, screenshots, sketches |
| Audio capture | Voice memos, recordings |
| Text capture | Notes, bookmarks, highlights |
| Sensory notes | Described textures, tastes, smells |
| Metadata | Tags, timestamps, locations |

#### Boundary Criteria

**In scope:** Raw capture, minimal processing, no synthesis
**Out of scope:** Analysis, interpretation, structured output
**Key test:** "Is this captured for later processing, or processed now?"

---

### 5. Learn Domain

**Current Praxis Definition:** Internal model and skill formation
**Confidence in Definition:** HIGH

#### Prior Art & Taxonomies

**Bloom's Taxonomy (1956, revised 2001):**
- Original: Knowledge → Comprehension → Application → Analysis → Synthesis → Evaluation
- Revised: Remember → Understand → Apply → Analyze → Evaluate → Create
- LOCS (lower-order): Remember, Understand, Apply
- HOCS (higher-order): Analyze, Evaluate, Create
- Source: [Wikipedia Bloom's](https://en.wikipedia.org/wiki/Bloom's_taxonomy), [Simply Psychology](https://www.simplypsychology.org/blooms-taxonomy.html)

**Knowledge Dimension (Anderson & Krathwohl 2001):**
- Factual knowledge (basic elements)
- Conceptual knowledge (interrelationships)
- Procedural knowledge (how to do something)
- Metacognitive knowledge (awareness of own cognition)
- Source: [NIU CITL](https://www.niu.edu/citl/resources/guides/instructional-guide/blooms-taxonomy.shtml)

**Psychomotor Domain (Simpson 1972):**
- Seven levels of physical skill acquisition
- Includes "guided response" (imitation, trial and error)
- Source: [Structural Learning](https://www.structural-learning.com/post/kolbs-learning-cycle)

**Kolb's Experiential Learning Cycle:**
- Concrete Experience → Reflective Observation → Abstract Conceptualization → Active Experimentation
- "Learners don't just absorb information—they make sense of it by doing, reflecting, thinking, and applying"
- Source: [Cogn-IQ](https://www.cogn-iq.org/learn/theory/experiential-learning/)

#### Subtype Taxonomy

| Type | Focus | Output |
|------|-------|--------|
| Skill acquisition | Procedural knowledge | Internal capability |
| Concept learning | Factual/conceptual | Mental models |
| Practice | Application/refinement | Improved performance |
| Meta-learning | Learning how to learn | Strategies |

#### Boundary Criteria

**In scope:** Goal is internal capability formation
**Out of scope:** Production-grade artifacts for external use
**Key test:** "Is this for me to get better, or for others to use?"

---

## Boundary Questions Resolution

### Write vs. Create

**Research-backed proposal:**

| Content Type | Domain | Rationale |
|--------------|--------|-----------|
| Technical docs | Write | Clarity → action |
| Business writing | Write | Information transfer |
| Blog posts (informational) | Write | Primary purpose: inform |
| Blog posts (personal/narrative) | **Boundary** | Could be either |
| Essays | Write | Argumentation |
| Fiction | Create | Ambiguity → imagination |
| Poetry | Create | Aesthetic/emotional |
| Creative nonfiction | Create | Narrative purpose dominates |

**Proposed test:** "Does the piece succeed through clarity (Write) or through evocation (Create)?"

### Observe vs. Learn

**Research-backed proposal:**

The boundary is **intent and processing**:

| Activity | Domain | Rationale |
|----------|--------|-----------|
| Taking a photo | Observe | Raw capture |
| Highlighting a book | Observe | Capture for later |
| Summarizing in own words | Learn | Active processing |
| Practice exercises | Learn | Skill formation |
| Making connections | Learn | Conceptualization (Kolb stage 3) |

**Key insight from Kolb:** Observation becomes learning when you move from "Concrete Experience" (pure observation) to "Reflective Observation" (beginning to process). The boundary is crossed when active mental processing begins with intent to form internal capability.

**Proposed test:** "Am I capturing for later, or processing to internalize now?"

### Code vs. Create

**Research-backed proposal:**

| Project | Domain | Rationale |
|---------|--------|-----------|
| AI art tool (the code) | Code | Functional output |
| AI art outputs (the images) | Create | Aesthetic output |
| Generative art installation | **Both** | Hybrid project |

**Key insight:** The same project may have components in multiple domains. The code itself is Code domain; the outputs are Create domain.

**Proposed handling:** Allow projects to span domains, with each artifact assigned to exactly one domain at creation.

### Hybrid Work Handling

**Research finding:** Both OSS Taxonomy (faceted approach) and PKM systems (PARA) handle hybrid work through:
1. **Multiple categorization facets** (not single-category)
2. **Artifact-level assignment** (not project-level)

**Proposed approach for Praxis:**
- Projects can span domains
- Each artifact belongs to exactly one domain
- Domain determines: storage, AI permissions, quality bar
- Promotion across domains requires explicit stage transition

---

## Follow-Up Spikes Needed

### Spike: Subtype Taxonomies per Domain
- **Question:** What subtypes should each domain support?
- **Where to look:** Industry standards for each domain
- **Size:** Medium (30 min)

### Spike: Domain Transition Mechanics
- **Question:** How exactly does an artifact move from Observe → Write?
- **Where to look:** PKM literature on progressive summarization
- **Size:** Small (15 min)

### Spike: AI Permission Matrices by Domain
- **Question:** What AI operations are allowed in each domain?
- **Where to look:** AI governance literature, creative AI ethics
- **Size:** Medium (30 min)

---

## Implementation-Ready Stories

### Story: Refine Write/Create Boundary
- Add "evocation test" to docs/domains.md
- Clarify creative nonfiction as Create domain
- **Confidence:** High (research supports clear distinction)

### Story: Add Observe→Learn Transition Criteria
- Document "processing intent" as transition trigger
- Map to Kolb's learning cycle stages
- **Confidence:** High (well-established framework)

### Story: Add Hybrid Project Guidance
- Document artifact-level domain assignment
- Add examples of multi-domain projects
- **Confidence:** Medium (need to validate with real projects)

---

## Sources Summary

### Code Domain
- [OSS Taxonomy - Andrew Nesbitt](https://nesbitt.io/2025/11/29/oss-taxonomy.html)
- [Software categories - Wikipedia](https://en.wikipedia.org/wiki/Software_categories)
- [Taxonomies in SE - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0950584917300472)

### Create Domain
- [Taxonomy of Creative Design](http://www.senseandsensation.com/2012/03/taxonomy-of-creative-design.html)
- [Common Design Taxonomy - UX Magazine](https://uxmag.com/articles/a-common-design-taxonomy)
- [Creativity/Aesthetics/Functionality - Springer](https://link.springer.com/article/10.1007/s00163-021-00366-9)

### Write Domain
- [Types of Writing - Grammarly](https://www.grammarly.com/blog/writing-techniques/types-of-writing/)
- [Technical Writing - IEEE](https://ieeexplore.ieee.org/iel2/766/908/00024018.pdf)
- [Technical vs Creative - ClickHelp](https://clickhelp.com/clickhelp-technical-writing-blog/technical-vs-academic-creative-business-and-literary-writing-what-is-the-difference/)

### Observe Domain
- [PKM Guide - Nick Ang](https://nickang.com/2020-07-05-personal-knowledge-management-system/)
- [PKM Guide - Elizabeth Butler](https://elizabethbutlermd.com/personal-knowledge-management/)
- [Passive Learning - Wikipedia](https://en.wikipedia.org/wiki/Passive_learning)

### Learn Domain
- [Bloom's Taxonomy - Wikipedia](https://en.wikipedia.org/wiki/Bloom's_taxonomy)
- [Bloom's Taxonomy - Simply Psychology](https://www.simplypsychology.org/blooms-taxonomy.html)
- [Experiential Learning - Cogn-IQ](https://www.cogn-iq.org/learn/theory/experiential-learning/)
- [Kolb's Learning Cycle - Structural Learning](https://www.structural-learning.com/post/kolbs-learning-cycle)

### Boundary Questions
- [Technical vs Creative Writing - Richard Rabil](https://richardrabil.com/2017/12/02/are-technical-writing-and-creative-writing-antithetical/)
- [Observational Learning - Wikipedia](https://en.wikipedia.org/wiki/Observational_learning)
- [Active vs Passive Learning - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6765278/)

---

## Time Spent

| Phase | Budgeted | Actual |
|-------|----------|--------|
| Setup (read definitions) | 3 min | 2 min |
| Research: Code + Create | 10 min | 8 min |
| Research: Write + Learn + Observe | 10 min | 10 min |
| Boundary resolution | 5 min | 5 min |
| Synthesis (this report) | 5 min | 5 min |
| **Total** | **30 min** | **~30 min** |

---

## Handoff Summary

### What Was Researched
- Prior art and industry taxonomies for all 5 Praxis domains
- Academic foundations (Bloom's taxonomy, Kolb's cycle, PKM literature)
- Boundary criteria between adjacent domains

### Key Findings
1. **Code domain:** OSS Taxonomy (2025) provides excellent faceted approach; our definition is solid
2. **Create domain:** UX Magazine taxonomy separates stylistic/functional/strategic/innovative design
3. **Write domain:** "Clarity vs. evocation" test distinguishes Write from Create
4. **Observe domain:** PKM literature (Zettelkasten, BASB) validates "raw capture" concept
5. **Learn domain:** Bloom's + Kolb provide strong framework for skill/knowledge formation

### What Remains Unknown
- Exact subtype lists for each domain (needs dedicated spike)
- AI permission matrices per domain
- Real-world validation of hybrid project handling

### Recommendations
1. Implement the "evocation test" for Write/Create boundary
2. Add Kolb's cycle reference for Observe/Learn transition
3. Document artifact-level domain assignment for hybrid projects
4. Create follow-up spikes for subtypes and AI permissions
