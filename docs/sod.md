# Statement of Direction (SOD)

**Domain:** Code

<!-- This template implements the Formalize Spine from lifecycle.md.
     All five sections are required before proceeding to Commit. -->

---

## 1. Intent & Outcome

<!-- What problem are we solving? Why now? Who benefits?
     Good example: "Users cannot reset passwords without contacting support,
     causing 50+ tickets/week. Self-service reset reduces support load and
     improves user experience." -->

### Problem Statement

<!-- One-paragraph statement of intent -->

### Audience

<!-- Who benefits from this solution? -->

### Why Now

<!-- What makes this timely or urgent? -->

---

## 2. Scope & Boundaries

<!-- What's in, what's out, what are we assuming?
     Good example: In: password reset via email. Out: SMS/phone reset.
     Assumption: Email delivery is reliable. Dependency: SMTP service. -->

### In Scope

-

### Out of Scope (Non-Goals)

-

### Assumptions

<!-- What are we taking for granted? -->

-

### Dependencies

<!-- External systems, teams, or artifacts this work depends on -->

-

---

## 3. Constraints

<!-- Boundaries that limit how we solve the problem.
     Good example: Must use existing auth library. No new dependencies.
     Privacy: PII-bearing. Time cap: 2 weeks max effort. -->

### Technical Constraints

<!-- Tooling, libraries, patterns, or architecture limits -->

-

### Environment Constraints

<!-- Deployment targets, infrastructure, or platform limits -->

-

### Privacy Classification

<!-- public | internal | confidential | pii-bearing -->

-

### Time/Effort Cap

<!-- Maximum investment before re-evaluation -->

-

---

## 4. Execution Framing

<!-- How do we start? What could go wrong? What don't we know yet?
     Good example: First increment: email-only reset for existing users.
     Risk: Token expiry UX confusion. Open question: Rate limiting strategy. -->

### First Executable Increment

<!-- Smallest slice that delivers value and validates approach -->

-

### Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
|      |            |        |            |

### Open Questions / Spikes

<!-- Unknowns that must be resolved before or during execution -->

-

---

## 5. Commit Criteria

<!-- Unambiguous definition of success. When are we done?
     Use Gherkin format for testable criteria. -->

### Success Criteria

-

### Acceptance Criteria

<!-- Use Given-When-Then format for testable acceptance criteria.
     Prefer declarative style (behavior) over imperative (UI steps).
     One behavior per scenario. Include edge cases and error paths.

     See: opinions/code/testing.md for BDD best practices -->

```gherkin
Feature: <Feature name>

  Scenario: <Happy path scenario>
    Given <initial context>
    When <action occurs>
    Then <expected outcome>

  Scenario: <Edge case or error path>
    Given <context>
    When <action>
    Then <outcome>
```

---

## Key Decisions

<!-- Major architectural or design choices made during shaping -->

-

---

<!-- Reference: See core/spec/lifecycle.md for Formalize Spine definition -->
