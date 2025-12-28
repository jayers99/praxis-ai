# Praxis Policy Engine: Sense & Explore

**Date:** 2025-12-27
**Status:** Explore Phase (Spike #3)
**Context:** Defining the "Brain" of Praxis before implementing the CLI.

---

## 1. Definition (Sense)

The **Policy Engine** is the deterministic logic core of Praxis. It is the function that resolves:
$$ f(Domain, Stage, Privacy, Environment) \rightarrow Behavior $$

It is responsible for:
1.  **Validation**: Is this `praxis.yaml` valid? (Schema)
2.  **Enforcement**: Are we allowed to be in this state? (Invariants)
    *   *Example:* Can we be in `Execute` stage without a `SOD.md`? (No)
    *   *Example:* Can we have `privacy: public` and a `.env` file? (No)
3.  **Projection**: Given the current user context (Environment), what tools/rules apply?

In the "Three-Layer Model" (Opinions $\to$ Governance $\to$ Execution), the Policy Engine **IS** the implementation of the **Governance Layer**.

---

## 2. The Five Whys (Root Cause Analysis)

1.  **Why do we need a Policy Engine?**
    *   To enforce rules like "No execution without formalization" or "No secrets in public repos."

2.  **Why can't we just trust the user/AI to remember these rules?**
    *   AI generates content faster than humans can verify governance. AI has no memory of implicit constraints. Humans forget.

3.  **Why is speed/memory a problem?**
    *   Because Praxis mixes "creative/messy" work (Capture/Explore) with "regulated/strict" work (Execute/Sustain).

4.  **Why do we mix these modes?**
    *   To allow innovation ("Home" context) to eventually become durable products ("Work" code). The transition (Formalize) is difficult.

5.  **Why is the Policy Engine the solution?**
    *   It provides the **Hard Boundary** (Formalize) that mechanically prevents the "messy" mode from leaking into the "strict" mode. It enables **safe velocity**.

---

## 3. Logic Gaps & Risks (Explore)

### 3.1 The "Unification" Problem (CUE vs Pydantic)
*   **The Theory (ADR-001):** Governance is the *intersection* (unification) of constraints.
    *   *Project says:* "I am Code domain".
    *   *User says:* "I am at Work".
    *   *Result:* Union of `Code Rules` + `Work Rules`.
*   **The Concern:** Pydantic is primarily an *input validator*, not a unification engine.
*   **The Risk:** Implementing "Merge Logic" in Python might become complex spaghetti code (if/else chains) compared to CUE's native lattice merging.
*   **Mitigation:** We must design the Pydantic models to explicitly handle "Overlay" logic (Base Config + Overlay = Final Config).

### 3.2 The Usage Gap
*   **Current Reality:** We edit markdown files manually.
*   **Desired Reality:** `praxis validate` CLI runs in CI or pre-commit hooks.
*   **Gap:** How does the Policy Engine influence the *AI Agent's* behavior in real-time?
    *   *Hypothesis:* The Policy Engine generates the `CLAUDE.md` / `.cursorrules` file dynamically. It acts as a compiler.

### 3.3 The "Environment" Source
*   `praxis.yaml` has `privacy`.
*   But where does `environment` come from? `ENV` var? A user profile config?
*   **Decision:** The Policy Engine typically inputs the Project Config (`praxis.yaml`) AND the User Context (Ephemeral/Env Var).

---

## 4. Best Practices (Research)

*   **Schema as Code:** Defining the schema in Pydantic allows us to generate JSON Schema for editor autocomplete (VS Code validation for `praxis.yaml`).
*   **Fail Fast:** Validation should happen at "Save" or "Commit" time.
*   **Distinguish "Invalid Schema" vs "Policy Violation":**
    *   *Invalid Schema:* `stage: "magic_stage"` (Type Error).
    *   *Policy Violation:* `stage: "execute"` without `SOD.md` (Logic Error).
    *   *Pydantic handles Type Errors natively. Logic Errors require `model_validator`.*

---

## 5. Next Steps (Shape)

Move from **Explore** to **Shape**:
1.  Define the `PraxisContext` model (Domain + Stage + Privacy).
2.  Define the `Invariant` protocol (Input $\to$ Bool).
3.  Draft `prototype.py` to prove Pydantic can handle the "No SOD at Execute" logic elegantly.
