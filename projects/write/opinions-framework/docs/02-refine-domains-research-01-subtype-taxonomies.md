# Spike: Subtype Taxonomies per Domain

**Issue:** #80
**Type:** Research Spike
**Time Box:** 30 minutes
**Status:** Complete

---

## Spike Intent

Research what subtypes should each domain support for hierarchical opinion inheritance.

---

## Research Findings

### 1. Code Domain Subtypes

#### Industry Taxonomy (from "A Taxonomy of Software Types")

The software industry generally categorizes software into three primary classes:

| Class | Description | Examples |
|-------|-------------|----------|
| **Apps** | Built to help users do valuable activities; immediately useful without development | Banking apps, image editors, mobile apps |
| **Tools** | General-purpose software for "fashioning" applications | Excel, WordPress, Figma, IDEs |
| **Infrastructure** | No end-user experience; foundation for other software | Databases, APIs, middleware, CLIs |

#### Proposed Code Subtypes for Praxis

| Subtype | Description | Inheritance Path |
|---------|-------------|------------------|
| `code.cli` | Command-line tools and utilities | Code → CLI |
| `code.library` | Reusable packages and modules | Code → Library |
| `code.api` | HTTP/REST/GraphQL services | Code → API |
| `code.webapp` | Web applications with UI | Code → WebApp |
| `code.infrastructure` | IaC, DevOps, platform tooling | Code → Infrastructure |
| `code.script` | One-off automation scripts | Code → Script |

**Sources:**
- [A Taxonomy of Software Types](http://insearchof.regenerateweb.net/a-taxonomy-of-software-types/)
- [Software Architecture Patterns 2025](https://www.index.dev/blog/software-architecture-patterns-guide)

---

### 2. Create Domain Subtypes

#### UNESCO Cultural Industries Classification

UNESCO identifies 7 categories of cultural/creative activities:
1. Cultural and natural heritage
2. Entertainment and events
3. Visual arts
4. Crafts and design
5. Publishing
6. Audio-visual and interactive media
7. Architecture and advertising

#### Creative Technology Taxonomy (Blair Neal)

Blair Neal's taxonomy organizes creative technology tools by medium:
- Cameras, projectors, alternative displays
- Interactive installations
- Generative art tools
- Real-time graphics engines

#### Proposed Create Subtypes for Praxis

| Subtype | Description | Inheritance Path |
|---------|-------------|------------------|
| `create.visual` | Static images, illustrations, graphics | Create → Visual |
| `create.audio` | Music, sound design, podcasts | Create → Audio |
| `create.video` | Film, animation, motion graphics | Create → Video |
| `create.interactive` | Games, installations, experiences | Create → Interactive |
| `create.generative` | AI-generated or algorithmic art | Create → Generative |
| `create.design` | UI/UX, product design, crafts | Create → Design |

**Sources:**
- [Creative Technology Taxonomy – Blair Neal](https://ablairneal.com/a-creative-technology-taxonomy)
- [Taxonomy of Creative Design](http://www.senseandsensation.com/2012/03/taxonomy-of-creative-design.html)
- UNESCO Cultural Industries Classification

---

### 3. Write Domain Subtypes

#### IEEE Technical Writing Taxonomy

IEEE research differentiates writing into:
- **Technical writing:** Procedural, instructional, system-focused
- **Business writing:** Reports, proposals, communications
- **Scientific writing:** Research papers, academic output

#### Documentation Categories

Common taxonomy for technical documentation:
- Setup / Installation
- User Guides / How-To
- Reference / API docs
- Troubleshooting
- Conceptual / Architecture

#### Proposed Write Subtypes for Praxis

| Subtype | Description | Inheritance Path |
|---------|-------------|------------------|
| `write.technical` | Documentation, tutorials, specs | Write → Technical |
| `write.business` | Reports, proposals, memos | Write → Business |
| `write.narrative` | Fiction, essays, personal stories | Write → Narrative |
| `write.academic` | Research papers, theses | Write → Academic |
| `write.journalistic` | Articles, news, long-form journalism | Write → Journalistic |

**Sources:**
- [IEEE Technical Writing Taxonomy](https://ieeexplore.ieee.org/document/24018/)
- [Taxonomy for Technical Documentation – Hedden](https://www.hedden-information.com/taxonomies-for-technical-documentation/)
- [Technical Writing Taxonomy – Medium](https://lucavettor.medium.com/the-backbone-of-technical-writing-is-taxonomy-8caccc190d7c)

---

### 4. Learn Domain Subtypes

#### Bloom's Taxonomy (Revised 2001)

The cognitive domain hierarchy:
1. **Remember** – Recall facts and basic concepts
2. **Understand** – Explain ideas or concepts
3. **Apply** – Use information in new situations
4. **Analyze** – Draw connections among ideas
5. **Evaluate** – Justify a decision or course of action
6. **Create** – Produce new or original work

#### Knowledge Dimensions (Anderson & Krathwohl)

| Dimension | Description |
|-----------|-------------|
| Factual | Basic facts, terminology |
| Conceptual | Classifications, categories, principles |
| Procedural | How to do something, methods, techniques |
| Metacognitive | Self-awareness, learning strategies |

#### Proposed Learn Subtypes for Praxis

| Subtype | Description | Inheritance Path |
|---------|-------------|------------------|
| `learn.skill` | Procedural knowledge, how-to | Learn → Skill |
| `learn.concept` | Theoretical understanding, mental models | Learn → Concept |
| `learn.practice` | Exercises, drills, deliberate practice | Learn → Practice |
| `learn.course` | Structured learning path | Learn → Course |
| `learn.exploration` | Self-directed discovery | Learn → Exploration |

**Sources:**
- [Bloom's Taxonomy – Wikipedia](https://en.wikipedia.org/wiki/Bloom's_taxonomy)
- [Taxonomies of Learning – Harvard](https://bokcenter.harvard.edu/taxonomies-learning)
- [Using Bloom's Taxonomy – Arkansas](https://tips.uark.edu/using-blooms-taxonomy/)

---

### 5. Observe Domain Subtypes

#### PKM Capture Categories (Tiago Forte)

Tiago Forte's PARA method categorizes captured information:
- **Projects** – Active work with deadlines
- **Areas** – Ongoing responsibilities
- **Resources** – Potentially useful reference material
- **Archives** – Inactive storage

#### Progressive Summarization Layers

Forte's Progressive Summarization describes capture maturity:
1. **Layer 1:** Raw capture (notes, highlights)
2. **Layer 2:** Bold key passages
3. **Layer 3:** Highlight within bold
4. **Layer 4:** Executive summary
5. **Layer 5:** Remix into new form

#### Proposed Observe Subtypes for Praxis

| Subtype | Description | Inheritance Path |
|---------|-------------|------------------|
| `observe.notes` | Text-based raw capture | Observe → Notes |
| `observe.bookmarks` | Links, references, citations | Observe → Bookmarks |
| `observe.clips` | Screenshots, quotes, snippets | Observe → Clips |
| `observe.logs` | Journals, daily notes, activity records | Observe → Logs |
| `observe.captures` | Photos, recordings, sensory data | Observe → Captures |

**Sources:**
- [Progressive Summarization – Forte Labs](https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/)
- [Building a Second Brain – Mindfulbytes](https://mindfulbytes.blog/how-to-build-a-second-brain-a-complete-guide-to-tiago-fortes-personal-knowledge-management-method)

---

## Inheritance Model

```
domain
└── subtype
    └── (future: variant)

Example:
code
├── code.cli
├── code.library
├── code.api
├── code.webapp
├── code.infrastructure
└── code.script
```

**Inheritance rules:**
1. Subtype inherits all parent domain opinions
2. Subtype can override specific opinions
3. Subtype can add new opinions
4. Conflict resolution: most specific wins

---

## Definition of Done Checklist

- [x] Subtype taxonomy for each of 5 domains
- [x] At least 2 sources per domain
- [x] Taxonomies support inheritance
- [x] Ready for PR

---

## Follow-Up Considerations

1. **Variant level:** Should subtypes have further sub-subtypes? (e.g., `code.cli.interactive` vs `code.cli.batch`)
2. **Cross-domain subtypes:** How to handle `code.api` that's also documentation (`write.technical`)?
3. **Subtype detection:** Can praxis auto-detect subtype from project structure?

---

## Handoff Summary

**Researched:** Subtype taxonomies for all 5 Praxis domains based on industry standards and academic frameworks.

**Key findings:**
- Code subtypes align with software industry taxonomy (Apps/Tools/Infrastructure)
- Create subtypes follow UNESCO cultural industries and Blair Neal's creative tech taxonomy
- Write subtypes based on IEEE technical writing research
- Learn subtypes grounded in Bloom's taxonomy and knowledge dimensions
- Observe subtypes informed by Tiago Forte's PKM frameworks

**Confidence:** High for Code, Write, Learn. Medium for Create, Observe (more subjective domains).

**Time spent:** Within 30-minute time box.
