# Praxis Lifecycle — Draft

**File:** lifecycle.md
**Version:** v0.3
**Purpose:** Capture the canonical Praxis lifecycle, the role of Formalize as the structural hinge, and the allowed regression model.

> **Research basis:** Stage definitions and entry/exit criteria are grounded in established frameworks. See [Lifecycle Research](research/lifecycle-research.md) for detailed citations and methodology alignments.

---

## Canonical Praxis Lifecycle

Praxis organizes all work—creative, technical, and regulated—around a small, stable set of lifecycle stages. Each stage has a single responsibility and clear handoff criteria. Policy, privacy, and execution constraints are enforced consistently across all stages.

### 1. Capture

Collect raw inputs with minimal friction. Includes notes, images, references, ideas, and observations. No commitment or structure is required.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Any input exists |
| **Exit** | Input stored in retrievable location |
| **Framework** | GTD (Allen), Zettelkasten (Luhmann) |

### 2. Sense

Convert raw inputs into understanding. Includes light organization, tagging, summarization, and pattern recognition. Outputs remain environment-neutral and low-commitment.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Captured inputs exist |
| **Exit** | Inputs have meaning/context; problem can be articulated |
| **Framework** | Sensemaking (Weick), Cynefin (Snowden) |

### 3. Explore

Generate possibilities without obligation. Supports ideation, divergence, and speculative thinking. Abandonment is expected and safe.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Sense complete; problem understood |
| **Exit** | Multiple possibilities exist; can describe 2-3 directions |
| **Framework** | Double Diamond (divergent), Divergent Thinking (Guilford) |

### 4. Shape

Converge toward a viable direction. Includes selection, refinement, simplification, and preliminary structuring. Work remains reversible.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Multiple options exist from Explore |
| **Exit** | Single direction chosen; scope roughed out; major tradeoffs resolved |
| **Framework** | Shape Up (Singer), Double Diamond (convergent) |

### 5. Formalize (Structural Hinge)

Convert shaped thinking into durable, policy-bearing artifacts. Formalize establishes explicit intent, scope, constraints, and success criteria.
**Primary output:** Solution Overview Document (SOD).
Formalize is the boundary between exploration and execution.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Shape complete; direction chosen |
| **Exit** | SOD exists with scope, constraints, and success criteria |
| **Framework** | SRS (IEEE), Stage-Gate Business Case (Cooper) |

### 6. Commit

Explicitly decide to proceed. Locks scope and intent, allocates effort, and enforces policy invariants. Only a small subset of formalized work should reach this stage.

| Criterion | Description |
|-----------|-------------|
| **Entry** | SOD complete and validated |
| **Exit** | Explicit commitment to proceed; resources allocated |
| **Framework** | Stage-Gate Go/Kill (Cooper), Shape Up Betting Table |

**Go/No-Go Criteria:**

| Decision | Condition |
|----------|-----------|
| **Go** | SOD is complete and internally consistent |
| **Go** | Scope fits available appetite (time/effort budget) |
| **Go** | Dependencies are identified and unblocked |
| **Go** | Success criteria are measurable |
| **No-Go** | Uncertainty about scope or direction remains → regress to Formalize |
| **No-Go** | Dependencies are blocked with no clear resolution |
| **No-Go** | Appetite insufficient for defined scope → reduce scope or wait |

### 7. Execute

Produce the artifact. Includes coding, writing, illustration, or other implementation activities. AI behavior is tightly governed and driven by formalized intent.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Commit complete; resources allocated |
| **Exit** | Artifact produced per SOD specifications |
| **Framework** | Agile/Scrum Sprint, Shape Up Build Cycle |

### 8. Sustain

Maintain and govern delivered work. Includes updates, evaluation, optimization, and policy enforcement over time.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Execute complete; artifact delivered |
| **Exit** | Work retired or closed |
| **Framework** | ITIL Service Operation, DevOps Operate/Monitor |

> **Domain variance:** Sustain semantics vary by domain. For **Code**, this means maintenance, monitoring, and operations. For **Write** and **Create**, it may mean revision, republication, or audience engagement. For **Learn**, it means practice and retention. Domain-specific guidance is in development.

### 9. Close

End work intentionally and capture leverage. Includes archiving artifacts, capturing learnings, retiring work, and seeding future cycles.

| Criterion | Description |
|-----------|-------------|
| **Entry** | Sustain complete or explicit decision to end |
| **Exit** | Learnings captured; next cycle seeded if applicable |
| **Framework** | PMI Project Closure, Agile Retrospectives |

---

## Structural Spine

The lifecycle is reinforced by three non-optional structural guarantees:

- **Formalize** — thinking becomes durable intent
- **Commit** — intent becomes action
- **Close** — action becomes leverage

Together, they ensure AI-assisted work remains repeatable, governed, and cumulative without sacrificing creative flow.

---

## Two Modes of Iteration

Formalize is the inflection point where the _nature_ of iteration changes.

### Discovery Iteration (Pre-Formalize)

Stages: Capture → Sense → Explore → Shape

- **Purpose:** Find out what the thing _is_
- **Character:** Divergent, then convergent; cheap to abandon
- **Question:** "What are we making?"
- **Cost of change:** Low—nothing is committed
- **Failure mode:** Safe abandonment; discard and restart

Iteration here reshapes the work itself. Each loop through Explore ↔ Shape refines _what_ you're building, not _how well_ you're building it.

### Refinement Iteration (Post-Formalize)

Stages: Execute → Sustain

- **Purpose:** Make the thing as _good_ as it can be
- **Character:** Incremental improvement within fixed scope
- **Question:** "How good can this get?"
- **Cost of change:** Higher—scope is locked, effort invested
- **Failure mode:** Regression to Formalize (expensive reset)

Iteration here polishes quality without changing identity. The thing is defined; you're perfecting its execution.

### Why This Matters

Recognizing which mode you're in prevents two common failures:

1. **Premature refinement** — Polishing something whose identity isn't settled (wasted effort)
2. **Scope creep in execution** — Discovering what the thing _is_ while trying to build it (expensive rework)

Formalize is the explicit moment where you declare: "The thing is now defined. Further iteration is refinement, not discovery."

---

## Stage → Allowed Regressions Table

This table defines the only permitted backward transitions between lifecycle stages. Any regression outside this table is invalid and must fail validation.

| Current Stage | Allowed Regression To | Purpose / Rationale                       | Required Action              |
| ------------- | --------------------- | ----------------------------------------- | ---------------------------- |
| Capture       | —                     | Entry stage                               | —                            |
| Sense         | Capture               | Missing or incorrect raw inputs           | Amend captured material      |
| Explore       | Sense, Capture        | Weak understanding or insufficient inputs | Update sense artifacts       |
| Shape         | Explore, Sense        | Direction is unclear or premature         | Re-open exploration          |
| Formalize     | Shape, Explore        | Intent or scope is unstable               | Update SOD before proceeding |
| Commit        | Formalize             | Scope, constraints, or priorities changed | Revise and re-validate SOD   |
| Execute       | Commit, Formalize     | Implementation reveals intent gaps        | Pause execution; re-commit   |
| Sustain       | Execute, Commit       | Defects, enhancements, or drift           | Re-enter governed execution  |
| Close         | Capture               | Seed new work from outcomes               | Start a new lifecycle        |

### Structural Rules

1. No regression may skip required artifacts (e.g., SOD required for Formalize).
2. Formalize is a hard boundary; late stages cannot regress to early exploration without re-formalization.
3. Execution is never speculative; ambiguity discovered during Execute forces a return to Formalize.
4. Close is terminal; it may only seed a new Capture.

---

## Regression Triggers

A regression occurs when the current stage cannot be completed due to gaps in prior stages. Triggers are detected manually (author recognizes friction) or via policy validation failure.

| Current Stage | Trigger Condition                                             | Target Stage | Required Response                       |
| ------------- | ------------------------------------------------------------- | ------------ | --------------------------------------- |
| Sense         | Raw inputs are missing, incomplete, or incorrect              | Capture      | Amend captured material before resuming |
| Explore       | Understanding is insufficient to generate options             | Sense        | Strengthen sense artifacts              |
| Shape         | No viable direction emerges; exploration was premature        | Explore      | Re-open divergent exploration           |
| Formalize     | Intent or scope remains unstable after shaping                | Shape        | Continue convergence before formalizing |
| Commit        | Constraints, priorities, or scope changed since formalization | Formalize    | Revise and re-validate SOD              |
| Execute       | Implementation reveals ambiguous or contradictory intent      | Formalize    | Pause execution; clarify and re-commit  |
| Execute       | Scope creep detected during implementation                    | Commit       | Re-evaluate commitment decision         |
| Sustain       | Defect root cause is a design flaw, not implementation bug    | Formalize    | Fix design before patching symptoms     |
| Sustain       | Enhancement requires scope expansion                          | Commit       | Treat as new commitment decision        |

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

```text
 ┌─────────┐
 │ Capture │◄────────────────────┐
 └────┬────┘                     │
      │                          │
 ┌────▼────┐                     │
 │  Sense  │◄───────────────┐    │
 └────┬────┘                │    │
      │                     │    │
 ┌────▼────┐                │    │
 │ Explore │◄──────┐        │    │
 └────┬────┘       │        │    │
      │            │        │    │
 ┌────▼────┐       │        │    │
 │  Shape  │◄──────┘        │    │
 └────┬────┘                │    │
      │                     │    │
 ┌────▼───────────────┐     │    │
 │     Formalize      │◄────┘    │
 │ (SOD / Contract)   │◄─────────┘
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
