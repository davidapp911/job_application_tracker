"""Utilities for cleaning and normalizing input dicts before they reach the API layer."""


def filter_empty_fields(data: dict, include_empty_str: bool = True) -> dict:
    """Remove None values and, when include_empty_str is True, empty/whitespace strings.

    When include_empty_str is False, empty strings pass through for downstream validation.
    Converts the "id" key to int.
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
