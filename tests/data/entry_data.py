"""Shared test data for entry-related API tests."""

# Minimal and optional-field entries that should insert without errors.
VALID_ENTRIES = [
    {"company": "Github", "job_title": "Python Developer"},
    {"company": "Microsoft", "job_title": "Data Analyst", "status": "Accepted"},
]

# Entries with empty, whitespace, or None required fields — should raise EntryException.
MISSING_FIELD_ENTRIES = [
    {"company": "Github", "job_title": "      "},
    {"company": "Microsoft", "job_title": None, "status": "Accepted"},
    {"company": "", "job_title": "Data Analyst"},
    {"company": "   ", "job_title": "Devops", "status": "Rejected"},
    {"company": "  ", "job_title": "  ", "status": "Unknown"},
]

# Entries with non-string field values — should raise EntryException.
INVALID_FIELD_ENTRIES = [
    {"company": "Github", "job_title": True},
    {"company": 1, "job_title": "Python Dev", "status": "Accepted"},
    {"company": True, "job_title": "Data Analyst"},
    {"company": "Apple", "job_title": 1, "status": False},
    {"company": False, "job_title": -9, "status": 1},
]

# Row counts for bulk insert tests.
INSERT_COUNTS = [1, 10, 50, 100, 999]

# Number of entries pre-populated for read and filter tests.
ENTRY_GENERATOR_COUNT = 30
