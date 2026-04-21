"""
Shared test data for entry-related API tests.

These datasets are used across multiple test modules to validate:
- successful entry creation
- missing required fields
- invalid field types
- bulk insert behavior
"""

# Valid entry inputs that should be successfully inserted into the database.
# Includes both minimal valid data and cases with optional fields (e.g., status).
VALID_ENTRIES = [
    {"company": "Github", "job_title": "Python Developer"},
    {"company": "Microsoft", "job_title": "Data Analyst", "status": "Accepted"},
]

# Entries with missing or empty required fields.
# Covers cases like:
# - empty strings
# - whitespace-only values
# - None values
# These should trigger validation errors.
MISSING_FIELD_ENTRIES = [
    {"company": "Github", "job_title": "      "},
    {"company": "Microsoft", "job_title": None, "status": "Accepted"},
    {"company": "", "job_title": "Data Analyst"},
    {"company": "   ", "job_title": "Devops", "status": "Rejected"},
    {"company": "  ", "job_title": "  ", "status": "Unknown"},
]

# Entries with incorrect data types for fields.
# Ensures validation rejects non-string values (e.g., bool, int).
INVALID_FIELD_ENTRIES = [
    {"company": "Github", "job_title": True},
    {"company": 1, "job_title": "Python Dev", "status": "Accepted"},
    {"company": True, "job_title": "Data Analyst"},
    {"company": "Apple", "job_title": 1, "status": False},
    {"company": False, "job_title": -9, "status": 1},
]

# Different sizes for bulk insert tests.
# Used to verify behavior with varying dataset sizes.
INSERT_COUNTS = [1, 10, 50, 100, 999]

# Upper bound for random data generation (if used in tests).
# Helps control test size and execution time.
ENTRY_GENERATOR_COUNT = 30
