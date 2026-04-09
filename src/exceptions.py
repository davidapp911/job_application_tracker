__all__ = [
    "EntryException",
    "MissingCompany",
    "MissingJobTitle",
    "MissingUpdateFields",
    "MissingSearchCriteria",
    "EntryNotFound",
]


class EntryException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


class MissingCompany(EntryException):
    def __init__(self) -> None:
        super().__init__("Company name is required.")


class MissingJobTitle(EntryException):
    def __init__(self) -> None:
        super().__init__("Job title is required.")


class MissingUpdateFields(EntryException):
    def __init__(self) -> None:
        super().__init__("No fields provided for update.")


class MissingSearchCriteria(EntryException):
    def __init__(self) -> None:
        super().__init__("No search criteria provided.")


class EntryNotFound(EntryException):
    def __init__(self, value) -> None:
        super().__init__(f"Entry with id {value} not found.")
