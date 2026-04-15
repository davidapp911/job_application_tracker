"""
Tests for the filter_empty_fields utility function.

These tests cover:
- Pass-through behavior for valid inputs
- Removal of None, empty, and whitespace-only values
- ID normalization and validation
- Mixed input scenarios (real-world cases)
- Edge cases like empty dictionaries
"""

import pytest
from src.data_utils import filter_empty_fields


# Ensures valid, non-empty inputs are returned unchanged
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {"company": "Github", "job_title": "Python Dev"},
            {"company": "Github", "job_title": "Python Dev"},
        ),
        (
            {"company": "Microsoft", "job_title": "DevOps"},
            {"company": "Microsoft", "job_title": "DevOps"},
        ),
    ],
)
def test_input_passes_through(test_input, expected):
    assert filter_empty_fields(test_input) == expected


# Verifies that None, empty strings, and whitespace-only values are removed
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"company": "Github", "job_title": None}, {"company": "Github"}),
        ({"company": "Github", "job_title": ""}, {"company": "Github"}),
        ({"company": "Github", "job_title": "   "}, {"company": "Github"}),
    ],
)
def test_removes_none_and_empty_values(test_input, expected):
    assert filter_empty_fields(test_input) == expected


# Confirms that string IDs are correctly converted to integers
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"id": "1"}, 1),
        ({"id": "9999999"}, 9999999),
    ],
)
def test_valid_id_conversion(test_input, expected):
    output = filter_empty_fields(test_input)
    assert output["id"] == expected


# Ensures invalid ID values raise a ValueError (non-numeric, bool, or whitespace)
@pytest.mark.parametrize(
    "test_input",
    [{"id": "abc"}, {"id": False}, {"id": "  "}],
)
def test_invalid_id(test_input):
    with pytest.raises(ValueError):
        filter_empty_fields(test_input)


# Verifies that integer IDs remain unchanged
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({"id": 100}, {"id": 100}),
        ({"id": 0}, {"id": 0}),
        ({"id": 99999}, {"id": 99999}),
    ],
)
def test_id_already_int(test_input, expected):
    assert filter_empty_fields(test_input) == expected


# Tests realistic scenarios with mixed valid, empty, and special-case fields
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {"id": 10, "company": "Github", "job_title": ""},
            {"id": 10, "company": "Github"},
        ),
        (
            {"id": "100", "company": "   ", "job_title": None, "status": "Rejected"},
            {"id": 100, "status": "Rejected"},
        ),
        (
            {"id": "0", "company": "Microsoft", "random_key": "random_value"},
            {"id": 0, "company": "Microsoft", "random_key": "random_value"},
        ),
    ],
)
def test_mixed_input(test_input, expected):
    assert filter_empty_fields(test_input) == expected


# Ensures function handles empty input gracefully
def test_empty_dictionary():
    assert filter_empty_fields({}) == {}
