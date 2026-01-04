# Week 1 Retrospective

**Week:** Nov 4-10, 2025  
**Hours logged:** 5.5 hours (30 min over budget, but worth it)

---

## What Went Well

✓ **Consistent schedule:** Hit all 3 sessions (Mon/Wed/Sat) as planned  
✓ **Hands-on practice:** 10 isolated examples made concepts concrete  
✓ **Personal project application:** Wrote 8 real tests for CLI parser  
✓ **pytest introspection:** Failure messages are incredibly helpful (better than unittest)

---

## What Was Challenging

✗ **Test organization:** Unsure when to use classes vs. functions (deferred to future)  
✗ **Conftest mystery:** Book mentioned conftest.py but didn't explain yet (Week 2 topic)  
✗ **Too many flags:** pytest CLI has dozens of options, focused on basics only

---

## Key Insights

1. **Plain assert is powerful:** pytest's introspection makes assert better than unittest methods
2. **Failure messages matter:** Custom messages help future debugging (used sparingly)
3. **Test naming:** Descriptive test names (`test_user_creation_with_valid_data`) are self-documenting

---

## Retention Check (Can I explain without docs?)

**Question:** How does pytest find tests?  
**Answer:** Looks for `test_*.py` or `*_test.py` files, functions starting with `test_`, searches directories recursively. ✓

**Question:** How do I test exceptions?  
**Answer:** Use `pytest.raises(ExceptionType)` as context manager. Can add `match` parameter for message checking. ✓

---

## Adjustments for Next Week

- Week 2 will cover fixtures (most anticipated topic)
- Expect fixtures to take more practice time (book warned this is biggest learning curve)
- Continue personal project tests (add fixture-based tests)

---

## Accountability Check-in (Friday Nov 8)

**Colleague feedback:** "Great progress! pytest basics look solid. Fixtures next week will unlock a lot."

---

**Status:** Week 1 complete, ready for Week 2 (Fixtures)
