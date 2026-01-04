# Week 1 Notes: pytest Basics

**Week:** Nov 4-10, 2025  
**Topic:** Test discovery, assertions, pytest CLI

---

## Key Concepts Learned

### Test Discovery
- pytest looks for `test_*.py` or `*_test.py` files
- Test functions must start with `test_`
- Can organize tests in directories (pytest searches recursively)
- conftest.py is special (shared fixtures, but learned more in Week 2)

### Assertions
- Use plain `assert` statements (no assertEqual or assertRaises)
- pytest introspection shows detailed failure messages automatically
- `pytest.raises()` for exception testing
- Can add custom failure messages: `assert x == y, "Expected x to equal y"`

### Running Tests
- `pytest` — run all tests
- `pytest -v` — verbose output (shows individual test names)
- `pytest -k "test_name"` — run specific tests by name pattern
- `pytest path/to/test.py::test_function` — run single test

---

## Examples Practiced

```python
# Basic assertion
def test_addition():
    assert 1 + 1 == 2

# Exception testing
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        result = 1 / 0

# Custom failure message
def test_user_creation():
    user = create_user("Alice")
    assert user.name == "Alice", f"Expected 'Alice', got '{user.name}'"
```

---

## Personal Project Application

Created `tests/test_cli_parser.py` with 8 tests:
- Test valid argument parsing
- Test missing required arguments (assert raises)
- Test invalid flag combinations
- Test help text output

---

## Reflection

**What worked well:**
- pytest's failure messages are incredibly helpful (shows diffs automatically)
- Plain assert feels natural compared to unittest methods

**What struggled with:**
- Organizing tests into classes vs. functions (when to use each?)
- Understanding pytest vs. unittest differences (still some confusion)

**What to revisit:**
- Test organization patterns (will learn more as project grows)
