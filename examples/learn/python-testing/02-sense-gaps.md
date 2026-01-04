# Sense — Knowledge Gaps & Priorities

**Stage:** Sense  
**Date:** 2025-11-02

---

## Current State (What I Know)

- Basic Python testing concepts (assert, raising exceptions)
- Can write simple test functions with pytest
- Understand test discovery (test_*.py pattern)
- Basic pytest CLI usage (pytest, pytest -v)

---

## Target State (What I Need to Know)

### Core Competencies
1. **Fixtures:** Setup/teardown patterns, scope (function, class, module, session)
2. **Parametrization:** Testing multiple inputs efficiently
3. **Mocking:** Isolating units, testing without external dependencies
4. **Test organization:** conftest.py, markers, test classes

### Evidence of Learning
- Can write test suite for complex project without constant documentation lookups
- Can explain fixtures and parametrization to colleague
- Confident debugging test failures

---

## Knowledge Gaps (Prioritized)

**High Priority (Must Learn):**
1. Fixtures (setup/teardown, scope, conftest.py)
2. Parametrization (pytest.mark.parametrize)
3. Mocking (unittest.mock, monkeypatch)

**Medium Priority (Nice to Have):**
4. Markers (pytest.mark.skip, pytest.mark.xfail)
5. Plugins (pytest-cov for coverage, pytest-mock)

**Low Priority (Defer to Future):**
- Property-based testing (Hypothesis)
- Advanced fixtures (fixture factories, yield fixtures)
- pytest plugins development

---

## Learning Context

**Available time:** 5 hours/week for 4 weeks (20 hours total)  
**Learning style:** Hands-on > reading, prefer small examples over comprehensive docs  
**Practice environment:** Personal CLI project (realistic context for exercises)

---

**Next:** Explore different learning approaches (Explore stage)
