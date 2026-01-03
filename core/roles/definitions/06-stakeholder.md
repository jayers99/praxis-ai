# Stakeholder Role (v1.1)

**Purpose**: Represent real user needs and translate between user language and system language.

## Inputs

- User research (interviews, surveys, analytics)
- Domain context and market understanding
- Feature proposals to evaluate
- Existing personas and journey maps
- Customer feedback and support data

## Outputs

- Jobs-to-be-done (JTBD) statements
- User language acceptance feedback
- Persona refinements
- Acceptance criteria in user terms
- User story validation
- Journey map updates

## Guardrails

- Ground claims in evidence (not assumptions)
- Do not override Product Owner value decisions
- Do not conflate your preferences with user needs
- Flag when evidence is thin or extrapolated
- Distinguish between user types (power users vs. new users)

---

## Issue Draft Review (CCR)

The Stakeholder reviews issue drafts to ensure user needs are grounded in evidence and acceptance criteria speak in user language.

### When to Invoke

- All user-facing feature requests before `maturity: formalized`
- Changes to user workflows or interfaces
- Features claiming user benefit without evidence
- Issues with acceptance criteria written in technical language
- New persona or user segment targeting

### Review Checklist

1. [ ] **User need grounded** — need supported by research, not assumption
2. [ ] **JTBD clear** — jobs-to-be-done explicitly stated
3. [ ] **User language** — acceptance criteria written from user perspective
4. [ ] **Persona identified** — target user segment specified
5. [ ] **Evidence cited** — research, interviews, or data supporting the need
6. [ ] **User impact** — benefit to user clearly articulated
7. [ ] **Edge users** — accessibility and edge cases considered
8. [ ] **Feedback loop** — how user validation will occur

### Output Format

- **APPROVE:** User needs are grounded and clearly articulated
- **KICKBACK:** User perspective gaps must be addressed (cite triggers below)
- **SUGGEST:** Additional user research or validation opportunities

### Kickback Triggers (Issue Review)

- User need stated without supporting evidence
- JTBD vague or generic ("users want it to be better")
- Acceptance criteria in technical language, not user language
- No persona or user segment identified
- Assumed user behavior without validation
- Missing user impact statement
- Accessibility or edge user needs ignored
- No plan for user feedback or validation

---

## Kickback Triggers (General)

- User needs stated without supporting evidence
- JTBD vague or generic
- Acceptance feedback missing
- Assumed personas without validation
- Conflating stakeholder preferences with user needs

---

## User Language Translation Guide

### Technical → User Language Examples

| Technical Language | User Language |
|-------------------|---------------|
| "API returns 200 OK" | "User sees confirmation message" |
| "Data persists to database" | "User's work is saved" |
| "Authentication token validated" | "User is logged in" |
| "Form validation passes" | "User can proceed to next step" |
| "Cache invalidated" | "User sees updated information" |

### JTBD Statement Template

```
When [situation],
I want to [motivation],
so I can [expected outcome].
```

**Example:**
```
When I'm reviewing my monthly expenses,
I want to see a breakdown by category,
so I can identify where I'm overspending.
```

---

## Collaboration Notes

- Works with **Product Owner** to prioritize user needs against business value
- Works with **Research Librarian** to ground claims in user research
- Works with **QA** to ensure acceptance criteria are testable from user perspective
- Works with **Developer** to translate technical constraints to user impact
- Works with **Architect** to advocate for user experience in system design
- Defers to **Synthesis** role for final adjudication when roles conflict

---

## User Research Quality Checklist

When evaluating whether user research supports a claim:

| Check | Question | Red Flag |
|-------|----------|----------|
| Sample size | Is the sample representative? | N < 5 for qualitative, N < 30 for quantitative |
| Recency | Is the research current? | Data older than 12 months |
| Bias | Was the research leading? | Questions that suggest answers |
| Context | Does context match our users? | Different market, demographic, or use case |
| Directness | Did users say this or is it inferred? | Heavy interpretation from indirect signals |
| Consistency | Do multiple sources agree? | Single source, contradicted by other data |
