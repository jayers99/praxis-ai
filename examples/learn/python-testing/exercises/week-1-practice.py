# Week 1 Practice: Basic pytest Examples

"""
Week 1 exercises: Test discovery, assertions, pytest CLI
"""

import pytest

# Example 1: Basic assertions
def test_string_operations():
    text = "pytest"
    assert text.upper() == "PYTEST"
    assert len(text) == 6
    assert "test" in text

# Example 2: Testing exceptions
def test_list_index_error():
    my_list = [1, 2, 3]
    with pytest.raises(IndexError):
        _ = my_list[10]

# Example 3: Custom failure messages
def test_dictionary_key():
    data = {"name": "pytest", "version": 7}
    assert "name" in data, "Expected 'name' key in data dictionary"
    assert data["version"] > 6, f"Expected version > 6, got {data['version']}"

# Example 4: Multiple assertions (shows which one fails)
def test_user_validation():
    user = {"name": "Alice", "age": 30, "active": True}
    assert user["name"] == "Alice"
    assert user["age"] >= 18
    assert user["active"] is True

# Example 5: Testing with different data types
def test_type_checking():
    value = 42
    assert isinstance(value, int)
    assert not isinstance(value, str)
    assert isinstance(value * 1.5, float)

# Example 6: String assertions with operators
def test_substring_matching():
    sentence = "pytest makes testing easier"
    assert sentence.startswith("pytest")
    assert sentence.endswith("easier")
    assert "testing" in sentence

# Example 7: List operations
def test_list_operations():
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert numbers[0] == 1
    assert numbers[-1] == 5
    assert sum(numbers) == 15

# Example 8: Exception with match pattern
def test_value_error_message():
    with pytest.raises(ValueError, match="invalid literal"):
        int("not_a_number")

# Example 9: Testing None
def test_none_checks():
    result = None
    assert result is None
    assert not result  # None is falsy

# Example 10: Boolean assertions
def test_boolean_logic():
    is_valid = True
    is_active = False
    assert is_valid
    assert not is_active
    assert is_valid and not is_active

# Checkpoint: All 10 basic test examples pass
# Run with: pytest week-1-practice.py -v
