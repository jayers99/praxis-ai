# Policy Engine Commentary: Deep Synthesis

**Date:** 2025-12-27  
**Author:** Antigravity (Review Agent)  
**Context:** Reviewing the Sense/Explore artifact against the full Praxis documentation corpus.

---

## Executive Summary

The initial `01-sense-explore.md` captured the **essence** of the Policy Engine correctly but **underestimated its scope**. After reading the complete documentation corpus, the Policy Engine is not simply a validator—it is the **Governance Layer incarnate**. It must unify:

1. **Lifecycle enforcement** (`lifecycle.md`)
2. **Privacy invariants** (`privacy.md`)
3. **Domain-specific artifact requirements** (`domains.md`, `formalize.md`)
4. **Stage regression rules** (`lifecycle.md` Table 104-118)
5. **External constraints overlay** (`external-constraints.md`)
6. **Dynamic AI instruction generation** (`ai-guards.md`)

This commentary refines the original analysis.

---

## 1. Refined Definition

### The Policy Engine is a **Four-Stage Pipeline**:

```
INPUT → VALIDATE → RESOLVE → OUTPUT
```

1. **INPUT**: `praxis.yaml` + User Context (ENV, `~/.ai-guards/`)
2. **VALIDATE**: Schema correctness + Invariants (e.g., "No Execute without SOD")
3. **RESOLVE**: Merge Project + User + Domain rules into a unified "Behavior Contract"
4. **OUTPUT**: 
   - `praxis validate` exit code (CLI)
   - Generated `CLAUDE.md` / `.cursorrules` (Dynamic AI Instructions)

### Evidence from Docs:

- **`layer-model.md`** (Lines 72-102): "Governance is procedural authority... applies across domains and projects."
- **`ai-guards.md`** (Lines 129-150): "AI front-end files are rendered artifacts... `= (core user guards) + (env overlay) + (project domain guards)`."
- **`README.md`** (Line 19): "Behavior is resolved deterministically by: `Domain + Stage + Privacy + Environment → Behavior`."

**Implication:** The Policy Engine is not a "validator." It is a **compiler** that transforms configuration into executable governance.

---

## 2. Critical Missing Element: ADR-002

The original Sense/Explore document **did not reference ADR-002** (`validation-model.md`), which is **the most important document for this spike**.

### Key Decisions from ADR-002:

| Position | Implication for Pydantic Implementation |
|----------|----------------------------------------|
| **Config Scope** (Lines 20-38) | Root `praxis.yaml` is the single source of truth. Simple. |
| **Validation Depth** (Lines 42-73) | Schema + Filesystem checks. **NOT** deep content parsing. |
| **Stage Tracking** (Lines 75-92) | Manual declaration. No state machine. Git is the audit log. |
| **Regression Enforcement** (Lines 96-114) | **Advisory warnings**, not blocking errors. |
| **Multi-Domain** (Lines 132-155) | Single domain per project (v1). No composition needed yet. |

### The Validation Rules Table (Lines 188-196) is the **Core Contract**:

```
| Rule | Severity | Trigger |
| Missing formalize artifact | Error | stage ≥ commit AND artifact not found |
| Invalid stage regression | Warning | Transition not in allowed table |
| Privacy downgrade | Warning | privacy_level decreased from prior commit |
```

**This is what we prototype.**

---

## 3. The "Unification Problem" — Clarified

The original document worried about implementing "CUE-style unification" in Pydantic. After reading the full corpus, this concern is **valid but overstated**.

### What Actually Needs to Merge:

1. **Project Config** (`praxis.yaml`):
   ```yaml
   domain: code
   stage: execute
   privacy_level: confidential
   ```

2. **User Context** (`~/.ai-guards/env.md` or `ENV=work`):
   ```yaml
   environment: Work
   external_constraints:
     - FDIC-regulated
     - No public AI with raw content
   ```

3. **Domain Rules** (`docs/opinions/code/`):
   - "Code domain requires SOD at Formalize"
   - "Exit codes enum for CLI projects"

4. **Privacy Rules** (`privacy.md`):
   - "Confidential → No raw logs in SOD"

### The Merge Logic:

```python
final_behavior = (
    ProjectConfig.model +
    UserContext.overlay +
    DomainRules[config.domain] +
    PrivacyRules[config.privacy_level]
)
```

This is **not unification** (CUE's lattice merging). This is **layered composition** (Pydantic's `model_validate` + custom logic).

**Verdict:** Pydantic can handle this with explicit `@model_validator` methods.

---

## 4. The "AI Guards" Connection (Critical Insight)

The original document mentioned "the Policy Engine generates `CLAUDE.md`" as a hypothesis. **This is confirmed by `ai-guards.md`**.

### Lines 128-150 (ai-guards.md):

> "AI front-end files should:
> - Include or reference Praxis AI guard content
> - Contain no original logic
> 
> Conceptually:
> ```
> (core user guards) + (env overlay) + (project domain guards) = AI front-end file
> ```"

**This means:**
The Policy Engine is **not just a CLI validator**. It is the **source code generator** for AI instructions.

### Workflow:
```bash
$ praxis compile
# Reads: praxis.yaml, ~/.ai-guards/*, docs/opinions/code/
# Outputs: .cursorrules (for Cursor), CLAUDE.md (for Claude Code)
```

This is a **new requirement** not captured in the original Sense/Explore.

---

## 5. The Lifecycle Regression Table

The original document mentioned "No Execute without SOD" as an example invariant. **This is one rule in a comprehensive table.**

### From `lifecycle.md` (Lines 104-118):

| Current Stage | Allowed Regression To | Purpose / Rationale |
|---------------|----------------------|---------------------|
| Execute | Commit, Formalize | Implementation reveals intent gaps |
| Sustain | Execute, Commit | Defects, enhancements, or drift |
| Close | Capture | Seed new work from outcomes |

**This table must be encoded in the Policy Engine.**

### Pydantic Implementation:

```python
ALLOWED_REGRESSIONS = {
    Stage.EXECUTE: [Stage.COMMIT, Stage.FORMALIZE],
    Stage.SUSTAIN: [Stage.EXECUTE, Stage.COMMIT],
    Stage.CLOSE: [Stage.CAPTURE],
}

def validate_regression(from_stage: Stage, to_stage: Stage) -> ValidationResult:
    if to_stage in ALLOWED_REGRESSIONS.get(from_stage, []):
        return ValidationResult.OK
    return ValidationResult.WARNING("Invalid regression path")
```

**This is straightforward in Pydantic.**

---

## 6. Privacy as a Cross-Cutting Concern

The original document did not emphasize **Privacy** enough. `privacy.md` defines **5 levels** with **9 enforcement points**.

### Privacy enforces:

- **Storage locations** (Line 41-85)
- **AI tooling restrictions** (Line 42, 52, 63, 73, 83)
- **Artifact specificity** (Line 89-102)

### Example Invariant:

```python
@model_validator(mode='after')
def validate_privacy_storage(self):
    if self.privacy_level == PrivacyLevel.RESTRICTED:
        if self.storage_location != "local-only":
            raise ValueError("Restricted privacy requires local-only storage")
    return self
```

**This is critical for the "safe velocity" value proposition.**

---

## 7. External Constraints (The Missing Overlay)

`external-constraints.md` defines a **non-negotiable layer** that sits outside Praxis's three-layer model.

### Lines 46-64:

> "External Constraints sit _outside_ the three-layer system and apply pressure inward.
> - Principles must respect external constraints
> - Governance must operate within them
> - Execution must comply with them"

### Example:

- **Project says:** `privacy: confidential`
- **User ENV says:** `FDIC-regulated = true`
- **External Constraint:** "FDIC prohibits using cloud AI with customer data"
- **Policy Engine result:** Block execution if `CLAUDE.md` allows cloud AI.

**This requires the Policy Engine to load and merge `ENV` constraints.**

---

## 8. Gaps in the Original Analysis

### What Was Missing:

1. **ADR-002**: The validation model specification.
2. **AI Guard Generation**: The Policy Engine as a "compiler" for `.cursorrules`.
3. **Regression Table**: The complete lifecycle state machine.
4. **Privacy Cross-Cutting**: 5 levels × 9 enforcement points.
5. **External Constraints**: The "pressure from outside" overlay.

### What Was Correct:

1. The "Five Whys" root cause analysis.
2. The concern about "Unification" complexity (though manageable).
3. The "Schema vs Policy Violation" distinction.

---

## 9. Revised Scope for the Prototype

Based on the complete documentation review, the **minimal viable Policy Engine prototype** must demonstrate:

### Core Features:

1. **Schema Validation** (`praxis.yaml` → Pydantic model)
2. **Artifact Existence Check** (`stage >= formalize` → `docs/sod.md` exists?)
3. **Regression Validation** (Warn if transition not in allowed table)
4. **Privacy-Storage Coupling** (Error if `privacy=restricted` + `storage!=local`)

### Deferred (Future):

- AI Guard compilation (`.cursorrules` generation)
- Multi-domain composition
- Deep artifact content parsing
- External constraints overlay

---

## 10. Recommendation: Pivot from "Validation" to "Resolution"

The original Sense/Explore framed this as "Policy Validation." The full documentation reveals it should be **"Policy Resolution."**

### Rename the Concept:

- ❌ **Policy Validator** (Too narrow)
- ✅ **Policy Engine** (Accurate)
- ✅ **Governance Resolver** (Precise)

### Why This Matters:

The engine doesn't just say "yes/no." It **produces the compiled behavior contract** for both humans (CLI feedback) and AI (generated instructions).

---

## 11. Final Verdict on Pydantic vs CUE

### Pydantic Can Handle This:

- ✅ Schema validation (native)
- ✅ Cross-field invariants (`@model_validator`)
- ✅ Filesystem checks (custom logic)
- ✅ Regression table (Python dict lookup)
- ✅ Privacy-domain coupling (validator chains)

### Pydantic Struggles With:

- ⚠️ Unification (must implement merge logic explicitly)
- ⚠️ Declarative rules (code is imperative, not declarative)

### CUE Would Excel At:

- ✅ Native unification (lattice merging)
- ✅ Declarative constraints (more auditable)

### Decision:

**Use Pydantic for v1**. The "unification" problem is manageable with explicit overlay logic. CUE's learning curve is not justified given:
1. We have a **worked validation model** (ADR-002)
2. We can ship **faster** with Pydantic
3. We can **defer** CUE until proven necessary

---

## 12. Next Steps (Shape → Formalize)

1. **Build `prototype.py`** with the 4 core features listed in Section 9.
2. **Test against `template-python-cli`** (Issue #4's `praxis.yaml`).
3. **Document friction points** (Is manual stage tracking natural?).
4. **Update ADR-001** with the decision: "Pydantic (v1), CUE (deferred)."
5. **Transition to Formalize** by writing the SOD for `praxis-cli`.

---

## Appendix: Documentation Cross-Reference

| Concept | Primary Source | Lines |
|---------|---------------|-------|
| Policy Engine Definition | `README.md` | 19 |
| Three-Layer Model | `layer-model.md` | 27-139 |
| Validation Model | `adr/002-validation-model.md` | 20-196 |
| Lifecycle Regression Table | `lifecycle.md` | 104-118 |
| Privacy Enforcement | `privacy.md` | 89-112 |
| AI Guard Generation | `ai-guards.md` | 128-150 |
| External Constraints | `external-constraints.md` | 46-64 |
