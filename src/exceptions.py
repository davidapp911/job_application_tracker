"""
Custom exception classes for the job application tracker.

Defines domain-specific errors used across the API and CLI layers
to provide clear and consistent error handling.
"""

__all__ = [
    "EntryException",
    "MissingUpdateFields",
    "MissingSearchCriteria",
    "EntryNotFound",
]


# Base exception for all entry-related errors.
# Stores a message that can be displayed in the CLI layer.
class EntryException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


# Specific exception raised when no fields are provided for an update operation.
class MissingUpdateFields(EntryException):
    def __init__(self) -> None:
        super().__init__("No fields provided for update.")


# Specific exception raised when a Field is empty.
class EmptyField(EntryException):
    def __init__(self, field) -> None:
        super().__init__(f"Data for {field} is missing.")


# Specific exception raised when a Field has the wrong data type.
class WrongFieldType(EntryException):
    def __init__(self, field_type, value) -> None:
        super().__init__(f"Field must be of type {field_type}. {value}")


# Specific exception raised when a Field is not allowed.
class FieldNotAllowed(EntryException):
    def __init__(self, field) -> None:
        super().__init__(f"Field {field} is not allowed.")


# Specific exception raised when no filters are provided for a search operation.
class MissingSearchCriteria(EntryException):
    def __init__(self) -> None:
        super().__init__("No search criteria provided.")


# Specific exception raised when an entry with the given id does not exist.
class EntryNotFound(EntryException):
    def __init__(self, value) -> None:
        super().__init__(f"Entry with id {value} not found.")
