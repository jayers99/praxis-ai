# Contributing to Praxis AI

This repository follows a structured "Mini-Praxis" lifecycle for contributions. This document defines the framework for interactions, specifically optimizing for AI-driven automation where agents read this file to structure valid GitHub Issues.

## Core Principles

1.  **Structure First**: All requests must follow the defined schemas to be valid.
2.  **Mini-Praxis**: Feature requests follow a simplified lifecycle (Raw $\to$ Shaped $\to$ Formalized) to ensure clarity before execution.
3.  **Automation Ready**: The formats below are strict to enable AI parsing and validation.

---

## 1. Contribution Types

We accept three primary types of contributions. Label your issue accordingly.

| Type | Purpose | Key Requirement |
| :--- | :--- | :--- |
| **Feature Request** | New functionality or capability | Must follow the **Mini-SOD** format |
| **Bug Fix** | Correcting unintended behavior | Must have Reproduction Steps |
| **Chore** | Maintenance, refactoring, docs | Must have Clear Acceptance Criteria |

---

## 2. Feature Request Framework

Feature requests are the most complex contribution type. They adhere to the **Mini-Praxis** process. The goal is to produce a "Formalized" artifact that is ready for execution.

### 2.1 Metadata Fields (Required)

You must fill out the front-matter or top-level metadata for every feature request.

*   **Priority**:
    *   `High`: Critical to core value or blocks other work.
    *   `Medium`: Important value add, schedule normally.
    *   `Low`: Nice to have, fill-in work.
*   **Size**:
    *   `Small`: < 1 Day (Quick wins, minor adjustments)
    *   `Medium`: 2-3 Days (Standard component work)
    *   `Large`: 1 Week (Significantly complex, may need breaking down)
*   **Type**:
    *   `Feature`: Delivers end-user value.
    *   `Spike`: Buys information/decisions (output is knowledge, NOT code).
*   **Maturity**:
    *   `Raw`: Early idea. Needs shaping. (Corresponds to Praxis `Capture`, `Sense`)
    *   `Shaped`: Problem is clear, solution is rough. (Corresponds to Praxis `Explore`, `Shape`)
    *   `Formalized`: Ready to build. (Corresponds to Praxis `Formalize` $\to$ `Commit`)

### 2.2 The Standard Format (Mini-SOD)

All Feature Requests must use this structure. If the maturity is `Formalized`, **Gherkin is mandatory**.

#### 1. Problem Statement
*What is the problem? Why is this valuable? Who is it for?*

#### 2. Success Criteria
*Bulleted list of conditions that mean "we are done".*

#### 3. Scope Boundaries
*   **In Scope**: What we WILL do.
*   **Out of Scope**: What we definitely WON'T do.

#### 4. Gherkin Specification (Mandatory for 'Formalized')
*Required for Development/Code generation.*

```gherkin
Feature: [Feature Name]

  Scenario: [Happy Path]
    Given [Context]
    When [Action]
    Then [Outcome]
```

#### 5. Risks & Constraints
*Security, Privacy, or Performance considerations.*

### 2.3 Lifecycle Mapping Reference

For users familiar with the full Praxis lifecycle, here is how the simplified status maps:

| Mini-Praxis Label | Canonical Stages |
| :--- | :--- |
| **Maturity: Raw** | Capture $\to$ Sense |
| **Maturity: Shaped** | Explore $\to$ Shape |
| **Maturity: Formalized** | Formalize $\to$ Commit |
| **(Execution)** | Execute $\to$ Sustain $\to$ Close |

---

## 3. Bug Fix Framework

Use for defect reports.

*   **Priority**: High | Medium | Low
*   **Severity**: Critical | Major | Minor
*   **Context**:
    *   **Current Behavior**: What is happening?
    *   **Expected Behavior**: What should happen?
    *   **Reproduction Steps**: 1. 2. 3. ...
    *   **Logs/Screenshots**: (Optional but recommended)

---

## 4. Chore Framework

Use for non-user-facing improvements.

*   **Goal**: What needs to be improved?
*   **Rationale**: Why is this necessary now?
*   **Acceptance Criteria**: clear definition of done.

---

## 5. Label Progression

As work progresses, update the `maturity` label:

| Transition | When |
| :--- | :--- |
| `raw` → `shaped` | Problem and solution approach are clear |
| `shaped` → `formalized` | Ready to implement (Gherkin written if feature) |
| Close issue | PR merged with "Fixes #N" in commit/PR body |

**Batch selection pattern:**
```bash
# Find ready-to-implement issues
gh issue list --label "maturity: shaped" --label "size: small"
gh issue list --label "maturity: formalized" --label "type: feature"
```
