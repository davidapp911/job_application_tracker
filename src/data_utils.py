"""
Data cleaning utilities for preparing input before it reaches the API layer.

Provides helpers to normalize and validate dictionaries used for filtering
and updating database records.
"""


# Utility functions for cleaning and preparing data before it reaches the API layer.
# Removes empty or invalid fields from the input dictionary.
# - Skips None values
# - Strips and ignores empty strings
# - Converts "id" field to integer
# - Preserves non-string values as-is
def filter_empty_fields(data: dict, include_empty_str: bool = True) -> dict:
    """
    Cleans a dictionary by removing empty or invalid values.

    - Skips None values
    - Strips and ignores empty strings (when include_empty_str is True)
    - Converts the "id" field to an integer
    - Preserves non-string values as-is

    Args:
        data (dict): Raw input dictionary.
        include_empty_str (bool): When True, strips empty strings. When False,
            only strips None values and lets empty strings through for validation.

    Returns:
        dict: Cleaned dictionary with only valid fields.
    """
    output = {}

    for k, v in data.items():
        if v is None:
            continue

        if k == "id":
            if isinstance(v, bool):
                raise ValueError("Invalid id value: {v}")

            try:
                output[k] = int(v)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid id value: {v}")
            continue

        if isinstance(v, str):
            if include_empty_str and v.strip() == "":
                continue
            output[k] = v
        else:
            output[k] = v

    return output
