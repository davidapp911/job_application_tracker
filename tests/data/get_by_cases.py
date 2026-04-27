"""Test data for get_by API tests."""

# ID filters that return no results; "count" is db size at query time.
INVALID_ID_GET_BY = [
    {"count": 0, "filter": {"id": 999}},
    {"count": 30, "filter": {"id": 999}},
]

# Single-field filters with known matches in the dataset.
SINGLE_CONDITION_GET_BY = [
    {"filter": {"company": "Amazon"}},
    {"filter": {"job_title": "Python Dev"}},
    {"filter": {"status": "Pending start"}},
]

# Multi-field filters applied as logical AND.
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

# Valid filters that match no records in the dataset.
GET_BY_NO_MATCH = [
    {"filter": {"company": "Youtube"}},
    {"filter": {"job_title": "Teacher"}},
    {"filter": {"status": "Retired"}},
]

# Filters with unknown or malformed fields — should raise EntryException.
INVALID_FIELD_GET_BY = [
    {"filter": {"age": 21}},
    {"filter": {"job_title": "Teacher", "color": "Black"}},
    {"filter": {"statuss": "Retired"}},
]
