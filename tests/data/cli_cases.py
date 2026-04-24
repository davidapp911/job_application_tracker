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
