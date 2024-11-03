class DatabaseException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class LogicException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class ValidationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
