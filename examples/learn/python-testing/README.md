# Example: Learning Skill — "Python Testing with pytest"

**Domain:** Learn  
**Subtype:** skill  
**Final Stage:** Sustain

---

## What you'll learn

This example demonstrates a complete lifecycle for a learning project:

- How to use a **Learning Plan** (`docs/plan.md`) to formalize your learning goals, scope, and evidence criteria
- How to progress through stages with learning work: Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain
- How learning artifacts (notes, exercises, reflections) build toward skill mastery
- How to balance structured learning (courses, books) with hands-on practice

---

## Prerequisites

- Basic familiarity with the Praxis lifecycle (see `docs/guides/user-guide.md`)
- Understanding of the Learn domain (see `core/spec/domains.md`)

---

## Project context

This example shows a 4-week self-directed learning project to master pytest fundamentals for writing effective Python unit tests. The goal is to transition from basic assert statements to confident use of fixtures, parametrization, and mocking in a work context.

**Outcome:** Can write comprehensive test suites for Python projects without constant documentation lookups.

---

## Step-by-step walkthrough

### 1. Capture (Raw learning inputs)

**File:** `01-capture-resources.md`

Collected learning resources:
- pytest official documentation
- "Python Testing with pytest" book (Brian Okken)
- Team's existing test suite (real-world reference)
- Colleague recommendations (specific topics to focus on)

### 2. Sense (Learning path emerges)

**File:** `02-sense-gaps.md`

Identified knowledge gaps and priorities:
- Current state: Can write basic assertions, unfamiliar with fixtures
- Target state: Confident using fixtures, parametrization, mocking
- Key themes: Test organization, setup/teardown patterns, test data management
- Motivation: Team adopting pytest, need working knowledge for upcoming project

### 3. Explore (Learning approach options)

**File:** `03-explore-approaches.md`

Evaluated different learning strategies:
- Book-first approach (read → practice)
- Project-based approach (build → learn as needed)
- **Selected:** Hybrid approach (structured learning + hands-on exercises)

### 4. Shape (Learning plan structure)

**File:** `04-shape-milestones.md`

Defined 4-week learning path:
- Week 1: pytest basics (setup, assertions, test discovery)
- Week 2: Fixtures (scope, conftest.py, fixture composition)
- Week 3: Parametrization (test variations, data-driven tests)
- Week 4: Mocking (unittest.mock, monkeypatch, testing external dependencies)

### 5. Formalize (Lock learning goals)

**File:** `docs/plan.md` ✅ **Required artifact**

Created the Learning Plan, which locks:
- Learning Goal: Master pytest fundamentals for professional Python testing
- Scope: Core pytest features (fixtures, parametrization, mocking)
- Evidence: Write test suite for personal project, pass practice exam, teach colleague
- Time commitment: 5 hours/week for 4 weeks

**This is the hard boundary.** After this point, iteration is refinement of practice, not discovering what to learn.

### 6. Commit (Decide to proceed)

**File:** `06-commit-schedule.md`

Explicit commitment to learning:
- Allocated 5 hours/week (Mon/Wed/Sat mornings)
- Purchased book and set up practice environment
- Informed team of learning goal (accountability)
- Scheduled check-in with colleague in Week 4

### 7. Execute (Active learning)

**Files in `notes/`, `exercises/`, `reflections/`:**
- `notes/week-1-basics.md` — Conceptual notes from book/docs
- `exercises/week-1-practice.py` — Hands-on coding exercises
- `reflections/week-1-retrospective.md` — What worked, what struggled with
- (Repeated for weeks 2, 3, 4)

**Evidence artifact:** `exercises/final-project-tests/` — Comprehensive test suite for personal CLI tool

### 8. Sustain (Maintain and apply)

**File:** `08-sustain-practice.md`

Post-learning activities:
- Applied pytest to work project (team code review)
- Taught colleague basic fixtures (reinforced understanding)
- Identified advanced topics for future learning (property-based testing with Hypothesis)
- Weekly practice: Review 1 pytest feature to maintain fluency

---

## Lifecycle progression

```
Capture → Sense → Explore → Shape → Formalize → Commit → Execute → Sustain
   ↓         ↓        ↓        ↓         ↓          ↓         ↓         ↓
resources  gaps   approach milestones  plan    schedule  study+practice  apply
```

**Key observation:** Formalize (the Learning Plan) is where learning goals are locked. Before that, we're discovering what to learn. After that, we're executing the learning and refining our understanding.

---

## Files in this example

```
examples/learn/python-testing/
├── README.md                           # This file
├── praxis.yaml                         # Project configuration
├── 01-capture-resources.md             # Learning resources collected
├── 02-sense-gaps.md                    # Knowledge gaps identified
├── 03-explore-approaches.md            # Learning strategies evaluated
├── 04-shape-milestones.md              # 4-week plan roughed out
├── docs/
│   └── plan.md                         # Learning Plan (formalize artifact)
├── 06-commit-schedule.md               # Commitment and schedule
├── notes/
│   ├── week-1-basics.md                # Conceptual notes
│   ├── week-2-fixtures.md
│   ├── week-3-parametrization.md
│   └── week-4-mocking.md
├── exercises/
│   ├── week-1-practice.py              # Hands-on coding
│   ├── week-2-fixtures-practice.py
│   ├── week-3-parametrize-practice.py
│   ├── week-4-mocking-practice.py
│   └── final-project-tests/            # Evidence of learning (test suite)
├── reflections/
│   ├── week-1-retrospective.md         # Weekly reflections
│   ├── week-2-retrospective.md
│   ├── week-3-retrospective.md
│   └── week-4-retrospective.md
└── 08-sustain-practice.md              # Ongoing practice and application
```

---

## How to use this example

1. **Read through the files in order** (01 → 02 → 03 → ... → 08)
2. **Pay special attention to `docs/plan.md`** — This is the required formalize artifact for Learn domain
3. **Notice the shift at Formalize** — Before: discovering what to learn. After: executing learning plan
4. **Notice the weekly rhythm** — Notes → Exercises → Reflection creates deliberate practice loop
5. **Try it yourself:**
   ```bash
   praxis new my-learning --domain learn --privacy personal
   cd my-learning
   # Follow the pattern demonstrated in this example
   praxis templates render --stage formalize  # Generates docs/plan.md
   ```

---

## Related resources

- **Learn domain specification:** `core/spec/domains.md`
- **Lifecycle stages:** `core/spec/lifecycle.md`
- **Learning Plan template:** `src/praxis/templates/domain/learn/artifact/plan.md`
- **User guide:** `docs/guides/user-guide.md`
