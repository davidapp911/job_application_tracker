"""
Test data for CLI tests.

- SINGLE_ROW_DB / MULTIPLE_ROW_DB: mocked get_all return values for list command tests
- SEARCH_FILTERS: args + expected filter dict pairs for search-by command tests
- UPDATE_CASES: args + expected data dict pairs for update command tests
"""

# Single-entry database state used to test list output for a minimal result set.
SINGLE_ROW_DB = [
    [
        {
            "id": 1,
            "company": "Google",
            "job_title": "Data Engineer",
            "status": "Awaiting response",
        }
    ]
]

# Multi-entry database state used to test list output across all rows.
MULTIPLE_ROW_DB = [
    [
        {
            "id": 1,
            "company": "Microsoft",
            "job_title": "DevOps",
            "status": "Pending start",
        },
        {
            "id": 2,
            "company": "Apple",
            "job_title": "ML Engineer",
            "status": "Rejected",
        },
        {
            "id": 3,
            "company": "Amazon",
            "job_title": "Python Dev",
            "status": "Awaiting response",
        },
        {
            "id": 4,
            "company": "Netflix",
            "job_title": "QA Developer",
            "status": "Pending start",
        },
        {
            "id": 5,
            "company": "Meta",
            "job_title": "Data Engineer",
            "status": "Sent",
        },
    ]
]

# Filter cases covering all single-field, two-field, three-field, and all-field combinations.
# Each case maps CLI args to the filter dict the command should pass to the API.
SEARCH_FILTERS = [
    # single filters
    {
        "args": ["--company", "Microsoft"],
        "filter": {
            "id": None,
            "company": "Microsoft",
            "job_title": None,
            "status": None,
        },
    },
    {
        "args": ["--job_title", "ML Engineer"],
        "filter": {
            "id": None,
            "company": None,
            "job_title": "ML Engineer",
            "status": None,
        },
    },
    {
        "args": ["--status", "Awaiting response"],
        "filter": {
            "id": None,
            "company": None,
            "job_title": None,
            "status": "Awaiting response",
        },
    },
    {
        "args": ["--id", "1"],
        "filter": {"id": 1, "company": None, "job_title": None, "status": None},
    },
    # two-field filters
    {
        "args": ["--company", "Netflix", "--job_title", "QA Developer"],
        "filter": {
            "id": None,
            "company": "Netflix",
            "job_title": "QA Developer",
            "status": None,
        },
    },
    {
        "args": ["--job_title", "Data Engineer", "--status", "Sent"],
        "filter": {
            "id": None,
            "company": None,
            "job_title": "Data Engineer",
            "status": "Sent",
        },
    },
    {
        "args": ["--company", "Apple", "--status", "Rejected"],
        "filter": {
            "id": None,
            "company": "Apple",
            "job_title": None,
            "status": "Rejected",
        },
    },
    {
        "args": ["--id", "2", "--company", "Apple"],
        "filter": {"id": 2, "company": "Apple", "job_title": None, "status": None},
    },
    # three-field filters
    {
        "args": [
            "--company",
            "Amazon",
            "--job_title",
            "Python Dev",
            "--status",
            "Awaiting response",
        ],
        "filter": {
            "id": None,
            "company": "Amazon",
            "job_title": "Python Dev",
            "status": "Awaiting response",
        },
    },
    {
        "args": [
            "--id",
            "3",
            "--job_title",
            "Python Dev",
            "--status",
            "Awaiting response",
        ],
        "filter": {
            "id": 3,
            "company": None,
            "job_title": "Python Dev",
            "status": "Awaiting response",
        },
    },
    # all fields
    {
        "args": [
            "--id",
            "5",
            "--company",
            "Meta",
            "--job_title",
            "Data Engineer",
            "--status",
            "Sent",
        ],
        "filter": {
            "id": 5,
            "company": "Meta",
            "job_title": "Data Engineer",
            "status": "Sent",
        },
    },
]

# Update cases covering single-field, two-field, and all-field combinations.
# Each case maps CLI args to the data dict the command should pass to the API.
UPDATE_CASES = [
    # single field
    {
        "args": ["--company", "Microsoft"],
        "data": {"company": "Microsoft", "job_title": None, "status": None},
    },
    {
        "args": ["--job_title", "DevOps"],
        "data": {"company": None, "job_title": "DevOps", "status": None},
    },
    {
        "args": ["--status", "Applied"],
        "data": {"company": None, "job_title": None, "status": "Applied"},
    },
    # two fields
    {
        "args": ["--company", "Google", "--job_title", "ML Engineer"],
        "data": {"company": "Google", "job_title": "ML Engineer", "status": None},
    },
    {
        "args": ["--company", "Apple", "--status", "Rejected"],
        "data": {"company": "Apple", "job_title": None, "status": "Rejected"},
    },
    {
        "args": ["--job_title", "Data Engineer", "--status", "Sent"],
        "data": {"company": None, "job_title": "Data Engineer", "status": "Sent"},
    },
    # all fields
    {
        "args": [
            "--company",
            "Amazon",
            "--job_title",
            "Python Dev",
            "--status",
            "Awaiting response",
        ],
        "data": {
            "company": "Amazon",
            "job_title": "Python Dev",
            "status": "Awaiting response",
        },
    },
]
