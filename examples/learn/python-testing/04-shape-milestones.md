# Shape — 4-Week Learning Plan

**Stage:** Shape  
**Date:** 2025-11-04

---

## Week 1: pytest Basics

**Learning Objectives:**
- Understand test discovery (naming conventions, directory structure)
- Write effective assertions (assert, assert raises, custom messages)
- Run tests with options (-v, -k, --markers)
- Understand test output (failures, tracebacks, diffs)

**Resources:**
- Book chapters 1-2
- pytest docs: Getting Started

**Exercises:**
- Write 10 simple test functions (various assertions)
- Test a calculator class (basic math operations)
- Practice pytest CLI options

**Application:**
- Write tests for CLI argument parsing in personal project

**Success Criteria:**
- Can write test file that pytest discovers automatically
- Understand pytest output when tests fail
- Comfortable with basic assertions

---

## Week 2: Fixtures

**Learning Objectives:**
- Understand fixture concept (setup/teardown without boilerplate)
- Use fixture scopes (function, class, module, session)
- Share fixtures via conftest.py
- Compose fixtures (fixtures using other fixtures)

**Resources:**
- Book chapters 3-4
- pytest docs: Fixtures

**Exercises:**
- Create fixtures for temporary files, database connections, mock data
- Experiment with fixture scopes (observe cleanup timing)
- Build conftest.py for shared fixtures

**Application:**
- Create fixtures for personal project (temp directories, config files, test data)

**Success Criteria:**
- Can explain when to use each fixture scope
- Comfortable creating and using conftest.py
- Understand fixture dependency injection

---

## Week 3: Parametrization

**Learning Objectives:**
- Use @pytest.mark.parametrize for test variations
- Parametrize fixtures for setup variations
- Use pytest.param for complex parametrization
- Understand parametrization + fixtures interaction

**Resources:**
- Book chapter 5
- pytest docs: Parametrizing Tests

**Exercises:**
- Parametrize tests with multiple input/output pairs
- Test edge cases using parametrization (empty strings, None, large numbers)
- Combine parametrization with fixtures

**Application:**
- Refactor personal project tests to use parametrization (eliminate duplication)

**Success Criteria:**
- Can write parametrized tests without referring to docs
- Understand when parametrization is appropriate (vs. multiple test functions)

---

## Week 4: Mocking

**Learning Objectives:**
- Mock external dependencies (API calls, database, filesystem)
- Use unittest.mock (Mock, MagicMock, patch)
- Use pytest's monkeypatch fixture
- Assert on mock calls (assert_called_with, call_count)

**Resources:**
- Book chapter 6
- pytest docs: Monkeypatch
- Python docs: unittest.mock

**Exercises:**
- Mock HTTP requests (requests library)
- Mock file I/O operations
- Mock environment variables (monkeypatch)

**Application:**
- Mock external API calls in personal project tests

**Success Criteria:**
- Can mock external dependencies confidently
- Understand difference between unittest.mock and monkeypatch
- Can verify mock interactions (call counts, arguments)

---

## Final Milestone (End of Week 4)

**Evidence of Learning:**
- Comprehensive test suite for personal CLI project (50+ tests, 80%+ coverage)
- Teach colleague basic fixtures (30-minute demo)
- Pass practice exam (if available) or complete practice project

---

## Schedule

- **Monday:** Reading session (1 hour)
- **Wednesday:** Practice exercises (2 hours)
- **Saturday:** Application to personal project (1.5 hours) + reflection (0.5 hours)

**Total:** 5 hours/week × 4 weeks = 20 hours

---

**Next:** Formalize this into a Learning Plan (Formalize stage)
