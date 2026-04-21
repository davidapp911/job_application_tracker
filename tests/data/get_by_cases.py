"""
Shared test data for get_by API tests.

These cases validate:
- retrieval by valid filters (single and multiple conditions)
- behavior when no matching records exist
- handling of invalid IDs and fields
"""

# Cases where filtering by ID should return no results because the ID does not exist.
# "count" represents how many entries exist in the database before the query.
INVALID_ID_GET_BY = [
    {"count": 0, "filter": {"id": 999}},
    {"count": 30, "filter": {"id": 999}},
]

# Cases using a single filter condition.
# Verifies that queries correctly return entries matching one field.
SINGLE_CONDITION_GET_BY = [
    {"filter": {"company": "Amazon"}},
    {"filter": {"job_title": "Python Dev"}},
    {"filter": {"status": "Pending start"}},
]

# Cases using multiple filter conditions.
# Ensures that all conditions are applied together (logical AND behavior).
MULTIPLE_CONDITION_GET_BY = [
    {"filter": {"company": "Amazon", "job_title": "Python Dev"}},
    {"filter": {"job_title": "Python Dev", "status": "Pending start"}},
    {"filter": {"company": "Amazon", "status": "Pending start"}},
    {
        "filter": {
            "company": "Amazon",
            "job_title": "Python Dev",
            "status": "Pending start",
        }
    },
]

# Valid filter fields that should return no results.
# Tests behavior when the dataset contains no matching entries.
GET_BY_NO_MATCH = [
    {"filter": {"company": "Youtube"}},
    {"filter": {"job_title": "Teacher"}},
    {"filter": {"status": "Retired"}},
]

# Cases with invalid or unsupported fields in the filter.
# Ensures the API rejects unknown fields or malformed queries.
INVALID_FIELD_GET_BY = [
    {"filter": {"age": 21}},
    {"filter": {"job_title": "Teacher", "color": "Black"}},
    {"filter": {"statuss": "Retired"}},
]
