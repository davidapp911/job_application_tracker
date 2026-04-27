"""Test data for delete-related API tests."""

# Valid deletions; "count" is db size, "id" is the entry to remove.
DELETE_VALID_ID_CASES = [
    {"count": 1, "id": 1},
    {"count": 30, "id": 14},
]

# Non-existent IDs (empty db or missing entry) — should raise EntryException.
DELETE_INVALID_ID_CASES = [
    {"count": 0, "id": 1},
    {"count": 1, "id": 2},
    {"count": 30, "id": 999},
]

# delete_all with varying db sizes.
DELETE_ALL_CASES = [
    {"count": 0},
    {"count": 1},
    {"count": 30},
]
