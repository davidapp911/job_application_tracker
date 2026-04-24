"""
Tests for the filter_empty_fields utility function.

These tests cover:
- Pass-through behavior for valid, non-empty inputs
- Removal of None, empty, and whitespace-only values
- ID normalization (string → int) and validation
- Mixed input scenarios (real-world combinations)
- Edge cases such as empty dictionaries
"""

import pytest
from src.data_utils import filter_empty_fields
from tests.data.entry_data import VALID_ENTRIES
from tests.data.filter_cases import (
    FILTER_MISSING_FIELD,
    ID_CONVERSION,
    VALID_ID,
    INVALID_IDS,
    FILTER_MIXED_INPUT,
)


# Ensures valid, non-empty inputs are returned unchanged
@pytest.mark.data_utils
@pytest.mark.parametrize("case", VALID_ENTRIES)
def test_unchanged_input(case):
    assert filter_empty_fields(case) == case


# Verifies that None, empty strings, and whitespace-only values are filtered out
@pytest.mark.data_utils
@pytest.mark.parametrize("case", FILTER_MISSING_FIELD)
def test_removes_none_and_empty_values(case):
    assert filter_empty_fields(case["entry_data"]) == case["expected"]


# Confirms that numeric string IDs are converted to integers
@pytest.mark.data_utils
@pytest.mark.parametrize("case", ID_CONVERSION)
def test_valid_id_conversion(case):
    output = filter_empty_fields(case["id_data"])
    assert output["id"] == case["expected"]


# Ensures invalid ID values raise a ValueError (non-numeric strings, bools, or whitespace)
@pytest.mark.data_utils
@pytest.mark.parametrize("case", INVALID_IDS)
def test_invalid_id(case):
    with pytest.raises(ValueError):
        filter_empty_fields(case)


# Verifies that integer IDs remain unchanged
@pytest.mark.data_utils
@pytest.mark.parametrize("case", VALID_ID)
def test_id_already_int(case):
    assert filter_empty_fields(case) == case


# Tests mixed scenarios combining valid fields, empty values, and ID normalization
@pytest.mark.data_utils
@pytest.mark.parametrize("case", FILTER_MIXED_INPUT)
def test_mixed_input(case):
    assert filter_empty_fields(case["entry_data"]) == case["expected"]


# Ensures the function returns an empty dict when given empty input
@pytest.mark.data_utils
def test_empty_dictionary():
    assert filter_empty_fields({}) == {}
