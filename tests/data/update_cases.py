"""
Shared test data for update-related API tests.

These cases validate:
- full updates where all fields are modified
- partial updates where only a subset of fields change
- None-mixed updates where None fields are silently dropped (no-op)
- rejection of invalid payloads (wrong types, empty values, unknown fields)
"""

# Cases where all updatable fields are provided.
# Verifies that a full replacement of entry data works correctly.
FULL_UPDATE = [
    {
        "new_data": {
            "company": "Google",
            "job_title": "Platform Engineer",
            "status": "Accepted",
        },
    },
]

# Cases where only a subset of fields is updated.
# Ensures partial updates do not affect other existing fields.
PARTIAL_UPDATE = [
    {"new_data": {"company": "Google"}},
    {"new_data": {"job_title": "AI Engineer"}},
    {"new_data": {"status": "Awaiting Response"}},
]

# Cases where None values are mixed with valid fields.
# None fields are stripped before validation (no-op), and only valid fields are applied.
NONE_MIXED_UPDATE = [
    {"new_data": {"company": None, "job_title": "Engineer"}, "applied": {"job_title": "Engineer"}},
    {"new_data": {"company": "Google", "status": None}, "applied": {"company": "Google"}},
    {"new_data": {"company": None, "job_title": "DevOps", "status": None}, "applied": {"job_title": "DevOps"}},
]


# Cases that should fail validation during update operations.
# Covers:
# - incorrect data types
# - empty or whitespace-only strings
# - None values
# - unknown or unsupported fields
# - attempts to modify restricted fields (e.g., id)
# - mixed valid and invalid data
# - empty payloads
INVALID_UPDATE_PAYLOADS = [
    # Wrong types
    {"new_data": {"company": 123}},  # int instead of str
    {"new_data": {"job_title": ["Engineer"]}},  # list instead of str
    {"new_data": {"company": True}},  # bool instead of str
    # Invalid string values
    {"new_data": {"company": ""}},  # empty string
    {"new_data": {"job_title": "   "}},  # whitespace-only
    # None values
    {"new_data": {"company": None}},
    {"new_data": {"job_title": None}},
    # Unknown / unsupported fields
    {"new_data": {"salary": "100k"}},  # field not in model
    {"new_data": {"location": "Remote"}},
    # Attempt to update ID (if disallowed)
    {"new_data": {"id": "123"}},
    {"new_data": {"id": 999}},
    # Mixed valid + invalid (should still fail)
    {"new_data": {"company": "Google", "job_title": ""}},
    # Completely empty payload (depends on your design)
    {"new_data": {}},
]
