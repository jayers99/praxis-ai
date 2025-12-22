# Praxis Lifecycle — Draft

**File:** lifecycle.md
**Version:** v0.2
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

## Regression Triggers

A regression occurs when the current stage cannot be completed due to gaps in prior stages. Triggers are detected manually (author recognizes friction) or via policy validation failure.

| Current Stage | Trigger Condition | Target Stage | Required Response |
|---------------|-------------------|--------------|-------------------|
| Sense | Raw inputs are missing, incomplete, or incorrect | Capture | Amend captured material before resuming |
| Explore | Understanding is insufficient to generate options | Sense | Strengthen sense artifacts |
| Shape | No viable direction emerges; exploration was premature | Explore | Re-open divergent exploration |
| Formalize | Intent or scope remains unstable after shaping | Shape | Continue convergence before formalizing |
| Commit | Constraints, priorities, or scope changed since formalization | Formalize | Revise and re-validate SOD |
| Execute | Implementation reveals ambiguous or contradictory intent | Formalize | Pause execution; clarify and re-commit |
| Execute | Scope creep detected during implementation | Commit | Re-evaluate commitment decision |
| Sustain | Defect root cause is a design flaw, not implementation bug | Formalize | Fix design before patching symptoms |
| Sustain | Enhancement requires scope expansion | Commit | Treat as new commitment decision |

### Detection Methods

1. **Manual recognition** — Author encounters friction, confusion, or repeated rework
2. **Policy validation failure** — Automated check fails (e.g., missing SOD at Execute)
3. **Peer review feedback** — Collaborator identifies upstream gaps
4. **Retrospective analysis** — Post-hoc review reveals stage was entered prematurely

### Regression Process

1. **Halt** — Stop work in current stage
2. **Document** — Record regression rationale (why, what's missing)
3. **Regress** — Move to target stage and address gap
4. **Re-validate** — Ensure target stage outputs are now complete
5. **Resume** — Progress forward through stages again

---

## Stage Completion Protocol

Upon completing each lifecycle stage:

1. **Verify** — Confirm all stage artifacts and acceptance criteria are met
2. **Commit** — Create a git commit summarizing the stage deliverables
3. **Push** — Push to remote to preserve progress and enable collaboration
4. **Advance** — Update `praxis.yaml` to the next stage

This ensures progress is preserved, enables seamless handoff between sessions, and maintains a clear audit trail of lifecycle progression.

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
