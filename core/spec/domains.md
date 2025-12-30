# Praxis: Domain Definitions

> **Research basis:** See [docs/research/domains-research.md](research/domains-research.md) for full prior art, sources, and rationale.

---

## 1. Code

**Intent:** Functional systems and tools  
**Formalize artifact:** Solution Overview Document (SOD)  
**Confidence:** HIGH

### Subtypes

| Subtype | Description |
|---------|-------------|
| `code.cli` | Command-line tools and utilities |
| `code.library` | Reusable packages and modules |
| `code.api` | HTTP/REST/GraphQL services |
| `code.webapp` | Web applications with UI |
| `code.infrastructure` | IaC, DevOps, platform tooling |
| `code.script` | One-off automation scripts |

### Primary Artifacts

- Source code (Python, shell, config)
- Executables / CLIs
- Infrastructure definitions (IaC, manifests)
- Tests (unit, integration, contract)

### Supporting Artifacts

- System Overview Documents (SOD)
- Architecture diagrams
- ADRs
- API specs

### Boundary

- **In scope:** Output is executable/runnable code
- **Out of scope:** AI-generated art (even if tooling is code), documentation-only

### AI Permissions

| Operation | Permission |
|-----------|------------|
| suggest | ✓ |
| complete | ✓ |
| generate | ? (ask) |
| transform | ? (ask) |
| execute | ? (ask) |

---

## 2. Create

**Intent:** Aesthetic and expressive output (any medium)  
**Formalize artifact:** Creative Brief _(draft)_  
**Confidence:** HIGH

### Subtypes

| Subtype | Description |
|---------|-------------|
| `create.visual` | Static images, illustrations, graphics |
| `create.audio` | Music, sound design, podcasts |
| `create.video` | Film, animation, motion graphics |
| `create.interactive` | Games, installations, experiences |
| `create.generative` | AI-generated or algorithmic art |
| `create.design` | UI/UX, product design, crafts |

### Primary Artifacts

- Compositions (visual, audio, spatial, textural)
- Performances (recorded or live)
- Generated works (images, audio, video)
- Design studies and explorations

### Supporting Artifacts

- Style guides
- Prompt sets
- Reference collections
- Iteration snapshots

### Boundary

- **In scope:** Primary purpose is aesthetic/emotional response
- **Out of scope:** Functional documentation, executable code
- **Key test:** "Does ambiguity invite imagination, or does clarity invite action?"

### AI Permissions

| Operation | Permission |
|-----------|------------|
| suggest | ✓ |
| complete | ✓ |
| generate | ✓ |
| transform | ✓ |
| execute | — |

---

## 3. Write

**Intent:** Structured externalized thought  
**Formalize artifact:** Writing Brief _(draft)_  
**Confidence:** MEDIUM (boundary with Create needs attention)

### Subtypes

| Subtype | Description |
|---------|-------------|
| `write.technical` | Documentation, tutorials, specs |
| `write.business` | Reports, proposals, memos |
| `write.narrative` | Essays, personal stories (not fiction) |
| `write.academic` | Research papers, theses |
| `write.journalistic` | Articles, news, long-form journalism |

> **Note:** Fiction and poetry belong to **Create**, not Write.

### Primary Artifacts

- Essays
- Technical documents
- Philosophical writing
- Narrative prose

### Supporting Artifacts

- Outlines
- Drafts
- Citations
- Revision logs

### Boundary

- **In scope:** Primary purpose is information transfer or argumentation
- **Out of scope:** Primary purpose is aesthetic/emotional response
- **Key test:** "Clarity invites action (Write) vs. ambiguity invites imagination (Create)"

### AI Permissions

| Operation | Permission |
|-----------|------------|
| suggest | ✓ |
| complete | ✓ |
| generate | ? (ask) |
| transform | ? (ask) |
| execute | — |

---

## 4. Observe

**Intent:** Capture without judgment or refinement (any sense)  
**Formalize artifact:** _(none required—Observe is pre-Formalize by nature)_  
**Confidence:** HIGH

### Subtypes

| Subtype | Description |
|---------|-------------|
| `observe.notes` | Text-based raw capture |
| `observe.bookmarks` | Links, references, citations |
| `observe.clips` | Screenshots, quotes, snippets |
| `observe.logs` | Journals, daily notes, activity records |
| `observe.captures` | Photos, recordings, sensory data |

### Primary Artifacts

- Visual captures (photos, screenshots, sketches)
- Audio captures (recordings, samples, voice memos)
- Sensory notes (textures, tastes, smells described)
- Raw notes / brain dumps

### Supporting Artifacts

- Tags
- Timestamps
- Minimal metadata

### Boundary

- **In scope:** Raw capture, minimal processing, no synthesis
- **Out of scope:** Analysis, interpretation, structured output
- **Key test:** "Captured for later processing, or processed now?"

### AI Permissions

| Operation | Permission |
|-----------|------------|
| suggest | ✓ |
| complete | ✗ (blocked) |
| generate | ✗ (blocked) |
| transform | ✗ (blocked) |
| execute | — |

> **Rationale:** Observe domain blocks AI generation to preserve raw capture authenticity.

---

## 5. Learn

**Intent:** Internal model and skill formation  
**Formalize artifact:** Competency Target _(draft)_  
**Confidence:** HIGH

### Subtypes

| Subtype | Description |
|---------|-------------|
| `learn.skill` | Procedural knowledge, how-to |
| `learn.concept` | Theoretical understanding, mental models |
| `learn.practice` | Exercises, drills, deliberate practice |
| `learn.course` | Structured learning path |
| `learn.exploration` | Self-directed discovery |

### Primary Artifacts

- Study notes
- Practice exercises
- Concept maps
- Skill logs

### Supporting Artifacts

- Reading lists
- Flashcards
- Summaries

### Boundary

- **In scope:** Goal is internal capability formation
- **Out of scope:** Production-grade artifacts for external use
- **Key test:** "Is this for me to get better, or for others to use?"

### AI Permissions

| Operation | Permission |
|-----------|------------|
| suggest | ✓ |
| complete | ✓ |
| generate | ✓ |
| transform | ✓ |
| execute | — |

---

## Domain Transitions

Artifacts can move between domains through explicit transitions:

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

### Transition Requirements

| From → To | Requirement |
|-----------|-------------|
| Observe → Write | Summary/thesis statement present |
| Observe → Learn | Learning goal identified |
| Write → Code | Technical specification present |
| Learn → Code | Working prototype exists |
| * → Create | Aesthetic intent declared |

---

## Cross-Domain Rules

1. **Single domain:** Artifacts belong to exactly one domain at creation
2. **Explicit transitions:** Promotion across domains requires stage transition
3. **Domain determines:**
   - Storage location
   - AI permissions
   - Quality bar
   - Allowed automation
4. **Hybrid projects:** Projects can span domains; each artifact is assigned individually

---

## AI Permission Modifiers

### By Privacy Level

| Privacy Level | Effect |
|---------------|--------|
| Public | `generate`/`transform` → Ask, `publish` → ✓ |
| Personal | Default permissions |
| Confidential | All operations → Ask |
| Restricted | `generate`/`transform` → ✗, `execute` → ✗ |

### By Environment

| Environment | Effect |
|-------------|--------|
| Home | Default permissions |
| Work | `execute` → Ask, `publish` → Ask |

---

## Why This Matters

Domain classification enables:
- **Domain-aware AI prompts** — Different behavior per domain
- **Schema validation** — Enforce domain-specific rules
- **Safer reuse** — Know what you're importing
- **Clean project histories** — Consistent organization
- **Late binding of intent** — Observe now, decide later

---

## References

- [Domains Research](research/domains-research.md) — Full prior art and sources
- [Lifecycle Stages](lifecycle.md) — Stage definitions
