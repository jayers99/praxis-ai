# Learning Plan

**Domain:** Learn

<!-- This template implements the Formalize Spine from lifecycle.md.
     All five sections are required before proceeding to Commit. -->

---

## 1. Intent & Outcome

### Learning Goal

Master pytest fundamentals (fixtures, parametrization, mocking) to write comprehensive, maintainable test suites for Python projects without requiring constant documentation lookups.

### Why

**Problem solved:** Current knowledge gap prevents effective contribution to team's testing practices. Can write basic assertions but struggle with fixtures and mocking, limiting test quality and maintenance.

**Opportunity unlocked:** Confident pytest skills enable participation in team's testing infrastructure, improve code quality, and prepare for upcoming project requiring high test coverage.

### Why Now

- **Project deadline:** Team project starts in 5 weeks (need working knowledge before then)
- **Team context:** Team standardizing on pytest, moving away from unittest
- **Accountability:** Colleague available for weekly check-ins and final review
- **Momentum:** High motivation after reading pytest testimonials

---

## 2. Scope & Boundaries

### In Scope

**Core pytest features:**
- Test discovery and organization (test_*.py, conftest.py)
- Assertions (assert, raising exceptions, custom messages)
- Fixtures (function/class/module/session scope, fixture composition)
- Parametrization (@pytest.mark.parametrize, parametrized fixtures)
- Mocking (unittest.mock integration, monkeypatch fixture)
- Test markers and selection (pytest.mark, -k flag)

**Application context:**
- Personal CLI project (realistic practice environment)
- Team's existing test suite (real-world reference)
- Simple examples (isolated feature practice)

### Out of Scope (Non-Goals)

- Advanced pytest plugins (defer to future learning)
- Property-based testing (Hypothesis integration)
- pytest plugin development
- CI/CD integration (separate learning goal)
- Test performance optimization
- Non-Python testing frameworks

### Assumptions

- Have basic Python proficiency (functions, classes, modules)
- Understand testing concepts (unit vs. integration, assertions)
- Have personal CLI project suitable for test practice
- Can dedicate 5 hours/week consistently for 4 weeks
- Access to "Python Testing with pytest" book (purchased)

### Dependencies

- **Book:** "Python Testing with pytest" by Brian Okken (purchased Nov 1)
- **Practice environment:** Personal CLI project repository (exists)
- **Review partner:** Colleague available for Week 4 check-in (confirmed)
- **Documentation:** pytest official docs (free, online)

---

## 3. Constraints

### Time Constraints

- **Total time:** 20 hours over 4 weeks
- **Weekly schedule:** 5 hours/week (Monday 1h, Wednesday 2h, Saturday 2h)
- **Deadline:** Complete by November 30 (before team project kickoff Dec 5)

### Tooling & Environment

- **Python version:** 3.10+ (team standard)
- **pytest version:** 7.x (latest stable)
- **Editor:** VS Code with pytest extension (for test discovery UI)
- **Practice repo:** Personal CLI project (existing, needs tests)

### Learning Style Preferences

- **Format:** Hands-on practice > passive reading
- **Pacing:** Weekly rhythm with reflection
- **Validation:** Small examples → personal project application
- **Retention:** Weekly retrospectives, teach-to-learn (colleague demo)

### Budget/Resource Constraints

- **Book:** $35 (purchased)
- **Additional resources:** Free (docs, tutorials, examples)
- **No budget for:** Courses, workshops, paid tutorials

---

## 4. Execution Framing

### Approach

**Resources (prioritized):**
1. "Python Testing with pytest" book (primary)
2. pytest official documentation (reference)
3. Team's test suite (real-world examples)
4. Real Python tutorials (supplementary)

**Experiments / practice:**
- Isolated exercises (small, focused feature tests)
- Personal project application (realistic context)
- Team code exploration (understand patterns in practice)

**Notes format:**
- Weekly notes (conceptual understanding, key insights)
- Code comments in exercises (annotate learning)
- Retrospectives (what worked, what struggled with, what to revisit)

### Milestones

**Week 1 (Nov 4-10):** pytest Basics
- Read book chapters 1-2
- Complete 10 basic test exercises
- Write tests for CLI argument parsing
- **Checkpoint:** Can write discoverable test file with clear assertions

**Week 2 (Nov 11-17):** Fixtures
- Read book chapters 3-4
- Practice fixture scopes and conftest.py
- Create fixtures for personal project
- **Checkpoint:** Understand when/why to use each fixture scope

**Week 3 (Nov 18-24):** Parametrization
- Read book chapter 5
- Parametrize tests for edge cases
- Refactor personal project tests (eliminate duplication)
- **Checkpoint:** Can write parametrized tests without docs lookup

**Week 4 (Nov 25-30):** Mocking
- Read book chapter 6
- Mock HTTP requests and file I/O
- Mock external API in personal project
- **Checkpoint:** Confident mocking external dependencies
- **Final evidence:** Teach colleague fixtures (30-min demo)

### Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Schedule slips (miss weekly sessions) | Medium | High | Block calendar time, accountability with colleague |
| Concepts don't stick (passive reading) | Medium | High | Hands-on exercises mandatory, reflection after each session |
| Personal project too complex for practice | Low | Medium | Start with simple modules (CLI parsing), not full application |
| Get stuck on advanced topics (lose momentum) | Medium | Medium | Defer to "Out of Scope", focus on core competencies only |

### Open Questions

- Should I learn pytest-cov (coverage plugin) in Week 4? → **Deferred:** Out of scope, team has coverage tooling already
- Is 4 weeks enough time? → **Validated:** Colleague confirmed this is realistic timeline for basics

---

## 5. Commit Criteria

### Evidence of Learning

**Demonstrable skills:**
1. Write comprehensive test suite for personal CLI project (50+ tests, 80%+ coverage)
2. Explain fixtures and parametrization to colleague (teach-to-learn validation)
3. Refactor team test to use fixtures instead of setup/teardown (apply in work context)

**Conceptual understanding:**
- Can explain when to use each fixture scope (function vs. class vs. module vs. session)
- Can describe difference between unittest.mock and monkeypatch (when to use each)
- Can identify when parametrization is appropriate (vs. multiple test functions)

### Success Criteria

1. **Test suite complete:** Personal CLI project has 50+ tests using fixtures, parametrization, and mocking
2. **Coverage target:** 80%+ test coverage for core modules (pytest-cov metric)
3. **Teach demonstration:** Successfully teach colleague basic fixtures (30-minute demo in Week 4)
4. **Work application:** Refactor at least 1 team test to use pytest patterns (code review approved)
5. **No documentation dependency:** Can write test with fixtures and parametrization without referring to docs
6. **Retention validated:** Explain pytest concepts to colleague without preparation (proves internalization)

**Definition of done:** All 6 success criteria met, colleague confirms readiness for team project work.

---

<!-- Reference: See core/spec/lifecycle.md for Formalize Spine definition -->
