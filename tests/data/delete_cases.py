"""
Test data for delete-related API tests.

These cases cover:
- successful deletions using valid IDs
- error handling for invalid or non-existent IDs
- bulk deletion scenarios (delete all entries)
"""

# Cases where deletion should succeed.
# "count" represents how many entries exist before deletion.
# "id" is a valid identifier that should be removed.
DELETE_VALID_ID_CASES = [
    {"count": 1, "id": 1},
    {"count": 30, "id": 14},
]

# Cases where deletion should fail due to invalid or non-existent IDs.
# Includes scenarios where:
# - the database is empty
# - the ID does not exist within the current dataset
DELETE_INVALID_ID_CASES = [
    {"count": 0, "id": 1},
    {"count": 1, "id": 2},
    {"count": 30, "id": 999},
]

# Cases for deleting all entries in the database.
# "count" represents the number of entries present before the operation.
DELETE_ALL_CASES = [
    {"count": 0},
    {"count": 1},
    {"count": 30},
]
