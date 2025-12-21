# Praxis Lifecycle — Draft

**File:** lifecycle-draft.md  
**Version:** v0.1  
**Purpose:** Capture the canonical Praxis lifecycle, the role of Formalize as the structural hinge, and the allowed regression model.

---

## Canonical Praxis Lifecycle

Praxis organizes all work—creative, technical, and regulated—around a small, stable set of lifecycle stages. Each stage has a single responsibility and clear handoff criteria. Policy, privacy, and execution constraints are enforced consistently across all stages.

### 1. Capture
Collect raw inputs with minimal friction. Includes notes, images, references, ideas, and observations. No commitment or structure is required.

### 2. Sense
Convert raw inputs into understanding. Includes light organization, tagging, summarization, and pattern recognition. Outputs remain environment-neutral and low-commitment.

### 3. Explore
Generate possibilities without obligation. Supports ideation, divergence, and speculative thinking. Abandonment is expected and safe.

### 4. Shape
Converge toward a viable direction. Includes selection, refinement, simplification, and preliminary structuring. Work remains reversible.

### 5. Formalize (Structural Hinge)
Convert shaped thinking into durable, policy-bearing artifacts. Formalize establishes explicit intent, scope, constraints, and success criteria.  
**Primary output:** Solution Overview Document (SOD).  
Formalize is the boundary between exploration and execution.

### 6. Commit
Explicitly decide to proceed. Locks scope and intent, allocates effort, and enforces policy invariants. Only a small subset of formalized work should reach this stage.

### 7. Execute
Produce the artifact. Includes coding, writing, illustration, or other implementation activities. AI behavior is tightly governed and driven by formalized intent.

### 8. Sustain
Maintain and govern delivered work. Includes updates, evaluation, optimization, and policy enforcement over time.

### 9. Close
End work intentionally and capture leverage. Includes archiving artifacts, capturing learnings, retiring work, and seeding future cycles.

---

## Structural Spine

The lifecycle is reinforced by three non-optional structural guarantees:

- **Formalize** — thinking becomes durable intent  
- **Commit** — intent becomes action  
- **Close** — action becomes leverage  

Together, they ensure AI-assisted work remains repeatable, governed, and cumulative without sacrificing creative flow.

---

## Stage → Allowed Regressions Table

This table defines the only permitted backward transitions between lifecycle stages. Any regression outside this table is invalid and must fail validation.

| Current Stage | Allowed Regression To | Purpose / Rationale | Required Action |
|--------------|----------------------|---------------------|-----------------|
| Capture | — | Entry stage | — |
| Sense | Capture | Missing or incorrect raw inputs | Amend captured material |
| Explore | Sense, Capture | Weak understanding or insufficient inputs | Update sense artifacts |
| Shape | Explore, Sense | Direction is unclear or premature | Re-open exploration |
| Formalize | Shape, Explore | Intent or scope is unstable | Update SOD before proceeding |
| Commit | Formalize | Scope, constraints, or priorities changed | Revise and re-validate SOD |
| Execute | Commit, Formalize | Implementation reveals intent gaps | Pause execution; re-commit |
| Sustain | Execute, Commit | Defects, enhancements, or drift | Re-enter governed execution |
| Close | Capture | Seed new work from outcomes | Start a new lifecycle |

### Structural Rules
1. No regression may skip required artifacts (e.g., SOD required for Formalize).
2. Formalize is a hard boundary; late stages cannot regress to early exploration without re-formalization.
3. Execution is never speculative; ambiguity discovered during Execute forces a return to Formalize.
4. Close is terminal; it may only seed a new Capture.

---

## Lifecycle Diagram (Conceptual)

```
 ┌─────────┐
 │ Capture │◄───────────────┐
 └────┬────┘                │
      │                     │
 ┌────▼────┐                │
 │  Sense  │◄──────────┐    │
 └────┬────┘           │    │
      │                │    │
 ┌────▼────┐           │    │
 │ Explore │◄──────┐   │    │
 └────┬────┘       │   │    │
      │            │   │    │
 ┌────▼────┐       │   │    │
 │  Shape  │◄──────┘   │    │
 └────┬────┘           │    │
      │                │    │
 ┌────▼───────────────┐│    │
 │     Formalize      │◄┘    │
 │ (SOD / Contract)   │◄─────┘
 └────┬───────────────┘
      │
 ┌────▼────┐
 │ Commit  │◄───────┐
 └────┬────┘        │
      │             │
 ┌────▼────┐        │
 │ Execute │◄───────┘
 └────┬────┘
      │
 ┌────▼────┐
 │ Sustain │◄───────┐
 └────┬────┘        │
      │             │
 ┌────▼────┐        │
 │  Close  │────────┘
 └─────────┘
```

---

## Notes

- Early stages prioritize creative flow and reversibility.
- Formalize is both a stage and a contract boundary.
- Post-Formalize stages are governed, deterministic, and policy-enforced.
- The model supports mutable privacy, late-bound environment rendering, and local-only AI where required.
