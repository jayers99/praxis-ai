# Governance Gap Analysis (Revised)

**Date:** 2025-12-27
**Scope:** Review of `docs/`, `CLAUDE.md`, `CONTRIBUTING.md`, and `docs/ai-guards/models/`.

## Executive Summary
This report analyzes the governance state of the Praxis repository. It identifies conflicts between documentation and reality, lists actions taken to resolve them, and highlights future architectural shifts.

---

## 1. Resolved Conflicts (Actions Taken)

### 1.1 Policy Engine Ambiguity
*   **Conflict**: Documentation favors CUE; Execution favors Pydantic. Logic was "half-baked".
*   **Resolution**: Updated **Issue #3** (Priority: High) to explicitly serve as the stabilization spike for this decision.
*   **Status**: `In Progress` (Issue #3).
*   **Note**: Policy validation is deferred to later in the lifecycle.

### 1.2 Missing "Mini-Praxis" Workflow
*   **Gap**: Need a defined process for generating feature requests that adhere to the new `CONTRIBUTING.md` standards.
*   **Resolution**: Created **Issue #46** ("Feature: Mini-Praxis Process for Issue Generation").
*   **Status**: `Planned`.

---

## 2. Structural Observations

### 2.1 AI Guards Architecture
*   **Current State**: `CLAUDE.md` is static.
*   **Future State**: `CLAUDE.md` will be dynamically generated context.
*   **Data Source**: User-level models found in `docs/ai-guards/models/`:
    *   `user.md`: Core user preferences and environment settings.
    *   `user-code.md`: Coding domain specific guardrails.
    *   These files serve as the "Memory" source for future dynamic generation.

### 2.2 Maturity Model Mapping
*   **Observation**: `CONTRIBUTING.md` uses a 3-stage maturity model (`Raw`, `Shaped`, `Formalized`).
*   **Canonical Lifecycle**: Uses 9 stages (`Capture`...`Close`).
*   **Refinement Needed**: Future documentation must explicitly map these:
    *   `Raw` $\to$ `Capture`, `Sense`
    *   `Shaped` $\to$ `Explore`, `Shape`
    *   `Formalized` $\to$ `Formalize` (and beyond for Execution)

### 2.3 Gherkin Requirements
*   **Observation**: `CONTRIBUTING.md` mandates Gherkin for `Formalized` features.
*   **Action Required**: Ensure `docs/sod.md` is updated to reflect this requirement so the "Formalize Contract" is consistent across artifacts.

---

## 3. Risk Assessment

*   **Low Risk**: The "Policy Engine" delay is acceptable as validation is deferred.
*   **Medium Risk**: "Mini-Praxis" automation is needed soon to prevent disparate issue formats.
*   **High Risk**: None currently. Governance is converging.

---

## 4. Next Steps

1.  **Execute Issue #3**: Define the structure for the Policy Engine (even if implementation is deferred).
2.  **Execute Issue #46**: Build the "Mini-Praxis" issue generator.
3.  **Update `docs/sod.md`**: Add Gherkin specification as a standard section.
