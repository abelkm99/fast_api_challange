from app.core.domain.commons.exceptions import BaseExceptionError


class PostTextNotProvidedError(BaseExceptionError):
    def __init__(
        self,
        message="Post text must be provided",
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class PostPayloadTooLargeError(BaseExceptionError):
    def __init__(
        self,
        message="Post payload exceeds the maximum allowed size (1 MB)",
        status_code: int = 413,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class PostNotFoundError(BaseExceptionError):
    def __init__(
        self,
        message="Post not found",
        status_code: int = 404,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)
