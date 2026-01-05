# Guardrail Test Scenarios

This directory contains test scenarios and validation documentation for Praxis guardrails defined in `../guardrails.md`.

## Purpose

Each guardrail should have corresponding test scenarios that demonstrate:

1. **When the guardrail triggers** — Specific conditions that activate the guardrail
2. **Expected AI behavior** — What the AI assistant should do when triggered
3. **Conflict detection** — How the guardrail identifies inconsistencies
4. **Resolution steps** — The process for resolving conflicts
5. **Edge cases** — Boundary conditions and non-triggering scenarios

## Test Files

- **g1-consistency-test.md** — Test scenarios for G1 (Bidirectional Consistency Propagation)

## Test Format

Each test scenario document should include:

### Required Sections

1. **Scenario Description** — What change is being made
2. **Test Setup** — Initial state and the change being tested
3. **Expected Behavior** — Step-by-step walkthrough of guardrail execution
4. **Test Result** — Pass/fail with rationale

### Example Test Structure

```markdown
## Test Scenario N: [Name]

### Scenario Description
Brief description of what's being tested.

### Test Setup
Initial state and the change being applied.

### Expected Behavior
Step-by-step walkthrough following the guardrail ritual.

### Test Result
✅ PASS / ❌ FAIL with explanation
```

## Running Tests

These are **theoretical validation tests** for guardrail design. They demonstrate:

- The guardrail correctly identifies when it should trigger
- The dependency graph is accurate
- The ritual steps are comprehensive
- AI assistants have clear guidance

**These are NOT automated tests.** They serve as:
- Design validation
- Documentation for AI assistants
- Reference scenarios for code review

## Adding New Tests

When adding a new guardrail to `../guardrails.md`:

1. Create a corresponding test file: `{guardrail-id}-test.md`
2. Include at least 3 test scenarios:
   - Normal triggering case
   - Edge case / boundary condition
   - Non-triggering case (to verify specificity)
3. Document expected behavior for each scenario
4. Update this README to list the new test file

## Maintenance

- Update tests when guardrails are modified
- Add new scenarios as edge cases are discovered
- Remove or archive tests for deprecated guardrails
- Keep test scenarios aligned with the current version of each guardrail
