"""
Shared test data for filter/normalization utilities.

These cases verify:
- removal of empty/whitespace/None fields
- ID normalization (string -> int)
- handling of valid vs invalid IDs
- behavior with mixed/extra inputs
"""

# Cases where empty, whitespace-only, or None values should be removed.
# "entry_data" is the raw input; "expected" is the cleaned result after filtering.
FILTER_MISSING_FIELD = [
    {
        "entry_data": {"company": "Github", "job_title": "      "},
        "expected": {"company": "Github"},
    },
    {
        "entry_data": {"company": "Microsoft", "job_title": None, "status": "Accepted"},
        "expected": {"company": "Microsoft", "status": "Accepted"},
    },
    {
        "entry_data": {"company": "", "job_title": "Data Analyst"},
        "expected": {"job_title": "Data Analyst"},
    },
    {
        "entry_data": {"company": "   ", "job_title": "Data Engineer"},
        "expected": {"job_title": "Data Engineer"},
    },
    {
        "entry_data": {"company": "   ", "job_title": "Devops", "status": "Rejected"},
        "expected": {"job_title": "Devops", "status": "Rejected"},
    },
    {
        "entry_data": {"company": "  ", "job_title": "  ", "status": "Unknown"},
        "expected": {"status": "Unknown"},
    },
]

# Cases for normalizing the "id" field.
# Accepts numeric strings (including zero-padded) and integers; outputs integer form.
ID_CONVERSION = [
    {"id_data": {"id": "00000001"}, "expected": 1},
    {"id_data": {"id": "2347"}, "expected": 2347},
    {"id_data": {"id": 9999}, "expected": 9999},
]

# Valid ID inputs that should pass validation unchanged.
VALID_ID = [
    {"id": 100},
]

# Invalid ID inputs that should fail validation.
# Includes non-numeric strings, booleans, whitespace, and malformed numeric strings.
INVALID_IDS = [
    {"id": "abc"},
    {"id": False},
    {"id": "  "},
    {"id": "01 23"},
]

# Mixed input scenarios combining valid fields, empty values, and extra keys.
# Verifies that:
# - empty/None/whitespace values are removed
# - valid IDs are normalized
# - unrelated keys are preserved if not explicitly filtered
FILTER_MIXED_INPUT = [
    {
        "entry_data": {"id": 10, "company": "Github", "job_title": ""},
        "expected": {"id": 10, "company": "Github"},
    },
    {
        "entry_data": {
            "id": "100",
            "company": "   ",
            "job_title": None,
            "status": "Rejected",
        },
        "expected": {"id": 100, "status": "Rejected"},
    },
    {
        "entry_data": {"id": "0", "company": "Microsoft", "random_key": "random_value"},
        "expected": {"id": 0, "company": "Microsoft", "random_key": "random_value"},
    },
    {
        "entry_data": {"id": "63", "company": " ", "random_key": " "},
        "expected": {"id": 63},
    },
]
