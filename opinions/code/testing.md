---
domain: code
version: "1.0"
status: draft
---

# Testing Methodology for Code Domain

> **Scope:** Testing guidance for AI-assisted code projects. Emphasizes tests-first development and high-quality test generation.
>
> **Reference:** See [TDD and BDD for AI Code Verification](../../research-library/patterns/tdd-bdd-ai-verification.md) for full research and 46 sources.

## Core Principles

### 1. Tests-First with AI

- **Statement:** Write tests before prompting for implementation; tests provide explicit, verifiable targets
- **Rationale:** AI models perform best with clear targets; tests enable automated feedback loops
- **Source:** Kent Beck (TDD), Claude Code best practices
- **Severity:** must-have

### 2. Context Isolation

- **Statement:** Separate test-writing from implementation to prevent AI "cheating"
- **Rationale:** Single-context prompts fail because AI carries forward implementation details; multi-agent achieves 84% TDD compliance vs 20% baseline
- **Source:** VibeTDD research, tdd-guard implementations
- **Severity:** should-have

### 3. BDD for Features, TDD for Components

- **Statement:** Use BDD (Given-When-Then) for feature-level acceptance criteria; use TDD for component-level implementation
- **Rationale:** BDD bridges stakeholders and developers; TDD ensures unit correctness
- **Source:** Dan North (BDD), Kent Beck (TDD)
- **Severity:** should-have

### 4. Mutation Testing Over Coverage

- **Statement:** Validate test effectiveness with mutation testing, not just line coverage
- **Rationale:** 100% coverage can yield 4% mutation score; coverage measures execution, not fault detection
- **Source:** MuTAP research, Meta ACH (73% acceptance rate)
- **Severity:** should-have

## TDD/BDD Fundamentals

### When to Use TDD

- Unit and component-level development
- Algorithmic or logic-heavy code
- Refactoring with behavior preservation
- Bug fixes (write failing test first)

### When to Use BDD

- Feature-level acceptance criteria
- Cross-functional requirements
- Stakeholder-visible behaviors
- Integration and end-to-end scenarios

### The Red-Green-Refactor Cycle

1. **Red:** Write a failing test
2. **Green:** Write minimal code to pass
3. **Refactor:** Improve design, keep tests green

**Common failure:** Skipping refactor step leads to messy code accumulation.

## AI Test Generation Patterns

### VibeTDD Batching

Traditional TDD causes context explosion with AI. Use focused batches instead:

- **Traditional:** Write test → implement → write test → implement
- **VibeTDD:** Write focused test batch → verify they fail → implement together

Key findings:
- AI excels as implementation assistant, not architect
- Vague prompts ("continue with next step") lead to scope creep
- Strict prompts ("Write only test cases for UserIdValidator") produce reliable results

### Multi-Step Prompting (Explain-Plan-Execute)

**Step 1 - Explain:** "Please explain the following function. Review what each element is doing precisely."

**Step 2 - Plan:** "Plan a set of unit tests that test the function's behavior for a wide range of inputs. Test edge cases the author may not have foreseen."

**Step 3 - Execute:** "Write unit tests following the cases above. Include helpful comments."

### Role Prompting

Assign a persona to shape AI approach:

```
You are a senior QA engineer with 10+ years in API testing.
Suggest edge cases for a payment gateway that handles:
- Credit cards, PayPal, gift cards
- Promo codes with various discount types
- Multi-currency transactions
```

### Few-Shot Examples

Provide high-quality examples to establish patterns:

```
### Example 1 Input:
def add(a: int, b: int) -> int:
    return a + b

### Example 1 Output:
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(0, 5) == 5

### New Function (generate similar tests):
def multiply(a: int, b: int) -> int:
    return a * b
```

### Constraint-Based Prompting

Explicitly specify requirements:

```
Generate unit tests for calculate_discount(price, discount_rate):
- MUST include edge cases: price=0, rate=0, rate=1
- MUST include invalid inputs: negative price, rate>1
- Use pytest with descriptive test names
- Follow Arrange-Act-Assert pattern
```

## BDD/Gherkin Best Practices

### Declarative Over Imperative

**Bad (imperative, UI-coupled):**
```gherkin
Scenario: User logs in
  When I click the "username" text field
  And I type "testuser"
  And I click the "Login" button
  Then I should see element with id "dashboard"
```

**Good (declarative, behavior-focused):**
```gherkin
Scenario: Valid credentials grant access
  Given a registered user with valid credentials
  When the user attempts to log in
  Then the user should see their dashboard
```

### One Behavior Per Scenario

Each scenario should have one When-Then pair:

```gherkin
# Good: separate scenarios
Scenario: Adding item to cart
  When user adds item to cart
  Then cart shows 1 item

Scenario: Removing item from cart
  Given a cart with 1 item
  When user removes the item
  Then cart is empty
```

## Quality Issues in AI-Generated Tests

| Issue | Description | Detection |
|-------|-------------|-----------|
| Tautological assertions | Tests mirror implementation logic | Mutation testing |
| Missing edge cases | Only happy paths tested | Boundary analysis |
| Over-mocking | Mocks return exactly expected shapes | Review mock complexity |
| Brittle assertions | Tests break on valid refactors | Run after unrelated changes |
| Implementation leakage | Tests depend on internal details | Black-box review |

## Practitioner Checklists

### Before Prompting

- [ ] Define what behavior to test (not implementation)
- [ ] List expected edge cases and error conditions
- [ ] Prepare few-shot examples in your preferred style
- [ ] Set up mutation testing tooling

### During Prompting

- [ ] Use role prompting ("Act as a senior QA engineer")
- [ ] Apply multi-step pattern (Explain → Plan → Execute)
- [ ] Include explicit constraints (edge cases, invalid inputs)
- [ ] Request test-first (tests before implementation)

### After Generation

- [ ] Review for tautological assertions
- [ ] Verify edge cases are actually tested
- [ ] Check mock complexity (over-mocking?)
- [ ] Run mutation testing
- [ ] Add property-based tests for input spaces
- [ ] Validate tests fail without implementation

### For TDD Discipline

- [ ] Use VibeTDD batching or enforcement layers
- [ ] Consider multi-agent context isolation
- [ ] Verify red phase before green phase
- [ ] Confirm AI didn't modify tests to pass
- [ ] Keep cycles short (minutes, not hours)
- [ ] Preserve test intent during refactoring

### Human Review Checklist for AI-Generated Tests

| Check | Question | Red Flag |
|-------|----------|----------|
| Tautology | Does test mirror implementation? | Assertions match internal logic |
| Edge cases | Boundary conditions tested? | Only happy paths |
| Mocking | Mocks realistic? | Mocks return exact expected shapes |
| Independence | Tests run in any order? | Shared state |
| Assertions | Meaningful assertions? | `assert True` or trivial |
| Naming | Names describe behavior? | Generic `test_1` names |
| Error paths | Exceptions tested? | Only success cases |
| Size | Test focused? | Testing multiple behaviors |

## What Remains Unsolved

1. **Semantic diversity:** AI tests lack variety of human intuition
2. **Domain context:** AI cannot infer business rules not in code
3. **Security testing:** Unit tests miss vulnerabilities; static analysis required
4. **Architecture decisions:** AI should not make strategic test design decisions

---

*Last updated: 2026-01-01*
