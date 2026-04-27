"""Test data for update-related API tests."""

# Full update: all updatable fields provided.
FULL_UPDATE = [
    {
        "new_data": {
            "company": "Google",
            "job_title": "Platform Engineer",
            "status": "Accepted",
        },
    },
]

# Partial update: only one field changed, others unaffected.
PARTIAL_UPDATE = [
    {"new_data": {"company": "Google"}},
    {"new_data": {"job_title": "AI Engineer"}},
    {"new_data": {"status": "Awaiting Response"}},
]

# None-mixed update: None fields are dropped; "applied" is the expected result.
NONE_MIXED_UPDATE = [
    {"new_data": {"company": None, "job_title": "Engineer"}, "applied": {"job_title": "Engineer"}},
    {"new_data": {"company": "Google", "status": None}, "applied": {"company": "Google"}},
    {"new_data": {"company": None, "job_title": "DevOps", "status": None}, "applied": {"job_title": "DevOps"}},
]


# Payloads that should fail validation: wrong types, empty values, unknown or restricted fields.
INVALID_UPDATE_PAYLOADS = [
    # wrong types
    {"new_data": {"company": 123}},
    {"new_data": {"job_title": ["Engineer"]}},
    {"new_data": {"company": True}},
    # empty/whitespace values
    {"new_data": {"company": ""}},
    {"new_data": {"job_title": "   "}},
    # None values (all-None triggers MissingUpdateFields)
    {"new_data": {"company": None}},
    {"new_data": {"job_title": None}},
    # unknown fields
    {"new_data": {"salary": "100k"}},
    {"new_data": {"location": "Remote"}},
    # restricted field (id is immutable)
    {"new_data": {"id": "123"}},
    {"new_data": {"id": 999}},
    # mixed valid + invalid
    {"new_data": {"company": "Google", "job_title": ""}},
    # empty payload
    {"new_data": {}},
]
