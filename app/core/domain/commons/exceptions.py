class BaseExceptionError(Exception):
    def __init__(self, *, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotImplementError(BaseExceptionError):
    def __init__(self, *, message: str = "Not implemented", status_code: int = 500) -> None:
        super().__init__(message=message, status_code=status_code)
