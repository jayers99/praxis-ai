# Opinions Framework Enhancement

**Domain:** Write  
**Stage:** Capture  
**Date:** 2025-12-28

---

## Project Intent

Define and document the aspirational opinions framework for Praxis — a structured set of first principles, quality gates, and guidance for each Domain × Lifecycle Stage cell.

### What This Project Produces

Structured documentation (opinions) that:
1. Guide AI-assisted work within each domain at each stage
2. Integrate with Praxis's policy engine via a defined contract
3. Are research-backed (key influencers, first principles, consensus)

### Why Write Domain (Not Learn)

| Consideration | Write ✓ | Learn |
|---------------|---------|-------|
| Primary output | Documentation artifacts | Competency/skill |
| Formalize artifact | Writing Brief | Learning Plan |
| Success measure | Quality of written opinions | Demonstrated capability |

Learning happens *during* this project, but the deliverable is written structure, not competency.

---

## Raw Inputs

### Problem Statement

The opinions framework needs:
- Clear structure per domain
- Defined contract with Praxis (what artifact shape does the policy engine expect?)
- Research-backed first principles (not ad-hoc preferences)

### Strategic Insight (Condensed)

> **Core realization:** This is a multidimensional matrix problem (Domain × Stage = 45 cells), not a linear documentation task. The temptation is to parallelize immediately; the discipline is to define structure first.

**Key constraints identified:**

1. **Structure precedes content.** Before generating 45 cells of opinions, define what a complete opinion artifact looks like: influencers → extracted principles → consensus synthesis → prioritized gates (must-have vs. nice-to-have).

2. **Contract before execution.** The interface between opinions and Praxis must be explicit. What artifact shape does `praxis validate` expect? Without this contract, research output may not integrate.

3. **Foundations require audit.** Lifecycle stage and domain definitions may contain ambiguity that would propagate into every cell. Refine the matrix axes before populating the matrix.

4. **Tracer bullet before parallelization.** Run one domain×stage cell end-to-end, single-threaded, to discover the real shape of the work. Then parallelize with confidence.

5. **Separation of concerns.** Multi-agent orchestration (how to run 8 agents) is distinct from opinion content (what agents produce). Keep these in separate workstreams.

6. **Validate against reality.** Use a concrete project (e.g., render-run) as acceptance test. Opinions that don't improve real work are academic exercises.

**Proposed research pipeline per cell:**
```
Influencers → First Principles → Consensus → Prioritization → Contract Validation
```

This pipeline produces artifacts that are traceable (who said this?), principled (why does it matter?), and actionable (what do I do?).

### Initial Observations (from comments)

1. This is fundamentally a **multidimensional matrix** problem (Domain × Stage)
2. Before parallelizing research, we need:
   - Refined lifecycle stage definitions (remove ambiguity)
   - Refined domain definitions (same)
   - Defined opinions ↔ Praxis contract
   - Template for opinion folder structure
3. Tracer bullet approach: run single-threaded through one cell first
4. Multi-agent orchestration is a *separate* concern from opinion content

### Proposed Opinion Structure (first thoughts)

```
Per Cell (Domain × Stage):
├── key-influencers.md     # Authoritative sources
├── first-principles.md    # Extracted principles
│   ├── Must-have (gates)
│   └── Nice-to-have (guidance)
├── quality-gates.md       # Checkpoints before next stage
├── anti-patterns.md       # What to avoid
└── opinion.md             # Consolidated synthesis
```

### Hierarchical Inheritance Model

Opinions aren't flat — they form a **tree structure** with inheritance:

```
Domain (e.g., Code)
├── First Principles (apply to all Code projects)
│
├── Subtype: CLI
│   ├── CLI-specific principles (inherit from Code)
│   │
│   └── Subtype: CLI-Python
│       └── Python-specific CLI principles (inherit from CLI + Code)
│
├── Subtype: Library
│   └── Library-specific principles
│
└── Subtype: API
    └── Subtype: REST API
        └── REST-specific principles
```

**Example for Write domain:**

```
Write (domain)
├── First Principles (apply to all writing)
│
├── Subtype: Technical
│   ├── README
│   ├── API Specification
│   │   └── REST API Contract
│   └── Technical Paper
│
├── Subtype: Business
│   ├── RFP (Request for Proposal)
│   └── User Stories
│
└── Subtype: Creative
    ├── Blog Post
    └── Fiction
```

**Key insight:** When Praxis receives a context like "I'm writing a REST API specification," it should:
1. Load Write domain first principles
2. Inherit Technical subtype principles  
3. Inherit API Specification principles
4. Apply REST API-specific principles

This enables **specific guidance without redundancy** — shared principles live at the appropriate level of abstraction.

### The Praxis Contract Question

How does Praxis know which opinions apply? The contract must define:
- How to declare project subtype in `praxis.yaml`
- How inheritance resolution works (child overrides parent? merges?)
- What artifact shape the policy engine expects at each level

### User Interaction Patterns

**How do users consume opinions?** Two complementary patterns emerged:

#### Pattern A: CLI-Driven (`praxis opinions`)

User invokes a Praxis command to get opinion-based feedback:

```bash
praxis opinions          # "What am I missing? What should I do next?"
praxis opinions --stage  # "How strong is my work at this stage?"
```

**The challenge:** Most opinion-based feedback requires AI reasoning, not imperative code. The CLI can:
1. Validate structural requirements (artifacts exist, schema correct)
2. Identify gaps against opinions checklist
3. **Generate a prompt** that gives the AI:
   - Current stage/domain/subtype context
   - References to relevant opinion files
   - Direction on what "good" looks like
   - The user can then feed this prompt to their AI assistant

This keeps Praxis deterministic while leveraging AI for nuanced assessment.

#### Pattern B: AI-Native (Agent Awareness)

The AI agent already knows the Praxis context and proactively applies opinions:

```
User: "How can I make this better?"
AI: [Reads praxis.yaml, determines stage/domain/subtype]
    [Loads relevant opinions from docs/opinions/]
    [Compares current work against best practices]
    [Generates improvement suggestions with references]
```

This requires the AI to have:
- Awareness of `praxis.yaml` location and structure
- Knowledge of opinion file conventions
- Ability to resolve inheritance (domain → subtype → specific)

### Stage Transition Behavior

**When user promotes to next stage:** Should opinions be validated?

| Option | UX | Rigor |
|--------|-----|-------|
| **Blocking** | Slow, frustrating | High — forces quality gate |
| **Non-blocking** | Fast, smooth | Low — may skip important checks |
| **User choice** | Flexible | Medium — user decides per-transition |

**Proposed approach:** Ask at transition time:

```
Ready to advance from Shape → Formalize.

[ ] Compare current work against best-practice opinions (recommended)
[ ] Skip opinion validation and proceed

[Advance]
```

This respects user agency while nudging toward quality.

### Dependencies / Blockers

- Lifecycle stage definitions need review for clarity
- Domain definitions need review for gaps
- Praxis contract undefined (what does `praxis validate` expect from opinions?)
- **New:** Subtype taxonomy undefined (what subtypes exist per domain?)
- **New:** CLI verb design (`praxis opinions` or integrate into `praxis validate`?)
- **New:** AI agent integration pattern (how does agent discover opinions?)

---

## Candidate Stories

| # | Story | Size | Notes |
|---|-------|------|-------|
| 1 | Refine lifecycle stage definitions | M | Remove ambiguity |
| 2 | Refine domain definitions | M | Check for gaps |
| 3 | Define opinions ↔ Praxis contract | M | Interface definition |
| 4 | Define opinion folder structure template | S | What "complete" looks like |
| 5 | Tracer bullet: Code × Capture end-to-end | L | Single-threaded discovery |
| 6 | Document Code domain opinion generation process | S | Capture learnings |
| 7 | Validate against render-run project | M | Real-world test |

---

## Next Steps

When ready to progress to **Sense**:
1. Organize these raw inputs
2. Identify patterns and gaps
3. Make meaning of the observations

---

## Related Files

- `scratch/aspirational-opinions/` — Working scratch space
- `scratch/multi-agent/` — Orchestration (separate concern)
- `scratch/philosophy/classical-roots.md` — Philosophical grounding
- `docs/opinions/` — Target location for final opinions
