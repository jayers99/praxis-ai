# Praxis Worked Examples

This directory contains first-party worked examples demonstrating complete lifecycle progression for non-Code domains.

---

## Available Examples

### 1. Write Domain: Technical Article

**Path:** [`write/technical-article/`](write/technical-article/)

**Demonstrates:**
- Writing Brief (formalize artifact)
- Article progression: outline → drafts → final publication
- Revision process with client/reviewer feedback
- Post-publication sustain (updates, corrections)

**Best for learning:**
- How to use Writing Brief to lock thesis and scope
- How drafting iterations work in Execute stage
- When changes stay in Sustain vs. trigger new iteration

---

### 2. Create Domain: Design Exploration

**Path:** [`create/design-exploration/`](create/design-exploration/)

**Demonstrates:**
- Creative Brief (formalize artifact)
- Visual exploration (3 options, client selection)
- Design iteration with client feedback
- Final deliverables (print + social media variants)

**Best for learning:**
- How to use Creative Brief to bound creative intent
- How Explore stage works (multiple options, selection)
- When design changes are refinement vs. scope expansion

---

### 3. Learn Domain: Python Testing

**Path:** [`learn/python-testing/`](learn/python-testing/)

**Demonstrates:**
- Learning Plan (formalize artifact)
- Weekly learning rhythm (notes + exercises + reflection)
- Evidence of learning (test suite, teach colleague, work application)
- Ongoing practice in Sustain

**Best for learning:**
- How to use Learning Plan to structure self-directed learning
- How deliberate practice loops work (study → practice → reflect)
- What "evidence of learning" looks like (not just completion)

---

### 4. Observe Domain: Research Capture

**Path:** [`observe/research-capture/`](observe/research-capture/)

**Demonstrates:**
- Raw capture artifacts (notes, clips, links)
- NO formalize artifact (Observe is pre-formalization)
- Lifecycle: Capture → Sense → Explore → Shape → Close (no Execute)
- Domain transition pattern (Observe → Write)

**Best for learning:**
- How Observe domain differs (no formalize, no execution)
- When to transition from Observe to another domain
- How domain transitions create new projects

---

## How to Use These Examples

### 1. Read the README First
Each example has a detailed README explaining:
- What you'll learn
- Step-by-step walkthrough
- Files in the example (with descriptions)

### 2. Follow the Stage Progression
Read files in order (01 → 02 → 03 → ...):
- Capture files show raw inputs
- Sense/Explore/Shape show how structure emerges
- Formalize artifact (Brief/Plan) locks scope and intent
- Execute files show iteration and refinement
- Sustain shows post-delivery updates and decisions

### 3. Pay Attention to the Formalize Artifact
Each domain (except Observe) has a required formalize artifact:
- **Write:** `docs/brief.md` (Writing Brief)
- **Create:** `docs/brief.md` (Creative Brief)
- **Learn:** `docs/plan.md` (Learning Plan)
- **Observe:** _(none required)_

This is the **hard boundary** between discovery and execution.

### 4. Notice the Sustain Decisions
Each example shows what stays in Sustain (refinement) vs. what triggers a new iteration (scope change):
- **Write:** Typo fixes stay in Sustain, new sections trigger iteration
- **Create:** Color adjustments stay in Sustain, new deliverables trigger new project
- **Learn:** Weekly practice stays in Sustain, new learning goals trigger new project

### 5. Try It Yourself
After reading an example, try creating your own project:

```bash
# Write domain
praxis new my-article --domain write --privacy public
cd my-article
praxis templates render --stage formalize  # Creates docs/brief.md

# Create domain
praxis new my-design --domain create --privacy public
cd my-design
praxis templates render --stage formalize  # Creates docs/brief.md

# Learn domain
praxis new my-learning --domain learn --privacy personal
cd my-learning
praxis templates render --stage formalize  # Creates docs/plan.md

# Observe domain
praxis new research-notes --domain observe --privacy personal
cd research-notes
# No formalize needed, start capturing!
```

---

## Key Observations Across Examples

### Formalize is the Hinge
Every example (except Observe) demonstrates how Formalize changes the nature of work:
- **Before Formalize:** Discovery (what is this?)
- **After Formalize:** Refinement (how good can this be?)

### Lifecycle Stages are Consistent
All examples follow the same stage progression:
```
Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain → Close
```

Observe skips Formalize/Commit/Execute (pre-formalization by nature).

### Artifacts Vary by Domain
Each domain has appropriate artifacts:
- **Write:** Outlines, drafts, final article
- **Create:** Sketches, explorations, iterations, final designs
- **Learn:** Notes, exercises, reflections, evidence
- **Observe:** Raw captures (notes, clips, links, logs)

### Sustain is Active, Not Passive
All examples show Sustain as ongoing governance:
- Updates and corrections (Write, Create)
- Continued practice (Learn)
- Detecting scope change vs. refinement (all)

---

## Related Resources

- **Domain specifications:** [`core/spec/domains.md`](../core/spec/domains.md)
- **Lifecycle stages:** [`core/spec/lifecycle.md`](../core/spec/lifecycle.md)
- **User guide:** [`docs/guides/user-guide.md`](../docs/guides/user-guide.md)
- **Templates:** `src/praxis/templates/domain/{domain}/artifact/`

---

## Questions?

If you're unsure which example to start with:
- **Have a clear thesis to communicate?** → Write example
- **Have a creative vision to execute?** → Create example
- **Want to learn a new skill?** → Learn example
- **Capturing research without clear intent?** → Observe example

**All examples are in Sustain stage** (completed, stable, available for reference).
