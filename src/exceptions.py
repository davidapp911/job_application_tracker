__all__ = ["EntryException", "MissingCompany", "MissingJobTitle"]


class EntryException(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message


class MissingCompany(EntryException):
    def __init__(self) -> None:
        super().__init__("Company name is missing")


class MissingJobTitle(EntryException):
    def __init__(self) -> None:
        super().__init__("Job title is missing")
