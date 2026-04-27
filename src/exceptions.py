"""Domain-specific exceptions for the job application tracker."""

__all__ = [
    "EntryException",
    "MissingUpdateFields",
    "MissingSearchCriteria",
    "EntryNotFound",
]


class EntryException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


class MissingUpdateFields(EntryException):
    def __init__(self) -> None:
        super().__init__("No fields provided for update.")


class EmptyField(EntryException):
    def __init__(self, field) -> None:
        super().__init__(f"Data for {field} is missing.")


class WrongFieldType(EntryException):
    def __init__(self, field_type, value) -> None:
        super().__init__(f"Field must be of type {field_type}. {value}")


class FieldNotAllowed(EntryException):
    def __init__(self, field) -> None:
        super().__init__(f"Field {field} is not allowed.")


class MissingSearchCriteria(EntryException):
    def __init__(self) -> None:
        super().__init__("No search criteria provided.")


class EntryNotFound(EntryException):
    def __init__(self, value) -> None:
        super().__init__(f"Entry with id {value} not found.")


class WrongInputException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message
