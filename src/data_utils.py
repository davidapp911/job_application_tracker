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
def filter_empty_fields(data: dict) -> dict:
    """
    Cleans a dictionary by removing empty or invalid values.

    - Skips None values
    - Strips and ignores empty strings
    - Converts the "id" field to an integer
    - Preserves non-string values as-is

    Args:
        data (dict): Raw input dictionary.

    Returns:
        dict: Cleaned dictionary with only valid fields.
    """
    # Dictionary to store cleaned key-value pairs.
    output = {}

    # Iterate through all provided fields.
    for k, v in data.items():
        # Skip fields with None values.
        if v is None:
            continue

        # Special handling for "id" field: ensure it is an integer.
        if k == "id":
            # Attempt to convert id to integer.
            try:
                output[k] = int(v)
            # Raise a clear error if conversion fails.
            except (ValueError, TypeError):
                raise ValueError(f"Invalid id value: {v}")
            continue

        # Handle string values: ignore empty or whitespace-only strings.
        if isinstance(v, str):
            # Only include non-empty strings.
            if v.strip() != "":
                output[k] = v
        # Preserve non-string values without modification.
        else:
            output[k] = v

    # Return the cleaned dictionary.
    return output
