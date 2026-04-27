"""Test data for filter_empty_fields: normalization, ID conversion, and edge cases."""

# Each case maps "entry_data" (raw input) to "expected" (cleaned output).
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

# Numeric string IDs (including zero-padded) normalized to int; int IDs passed through.
ID_CONVERSION = [
    {"id_data": {"id": "00000001"}, "expected": 1},
    {"id_data": {"id": "2347"}, "expected": 2347},
    {"id_data": {"id": 9999}, "expected": 9999},
]

# Valid ID inputs that should pass validation unchanged.
VALID_ID = [
    {"id": 100},
]

# Non-numeric strings, booleans, and whitespace IDs — should raise ValueError.
INVALID_IDS = [
    {"id": "abc"},
    {"id": False},
    {"id": "  "},
    {"id": "01 23"},
]

# include_empty_str=False: None stripped, empty and whitespace strings pass through.
INCLUDE_EMPTY_STR_FALSE = [
    # None stripped, empty string passes through
    {
        "entry_data": {"company": "", "job_title": None},
        "expected": {"company": ""},
    },
    # Whitespace-only string passes through
    {
        "entry_data": {"company": "   "},
        "expected": {"company": "   "},
    },
    # None removed, valid string kept
    {
        "entry_data": {"company": None, "job_title": "Engineer"},
        "expected": {"job_title": "Engineer"},
    },
    # Both None fields stripped, valid field kept
    {
        "entry_data": {"company": None, "job_title": None, "status": "Rejected"},
        "expected": {"status": "Rejected"},
    },
    # All None → empty dict
    {
        "entry_data": {"company": None, "job_title": None},
        "expected": {},
    },
]


# Scenarios combining valid, empty, and ID-normalized fields with extra keys.
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
