from app.core.domain.commons.exceptions import BaseExceptionError


class EmailNotProvidedError(BaseExceptionError):
    def __init__(
        self,
        message="Email must be provided",
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class EmailAlreadyExistsError(BaseExceptionError):
    def __init__(
        self,
        message="Email already exists",
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class UserNotFoundError(BaseExceptionError):
    def __init__(
        self,
        message="User not found",
        status_code: int = 404,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class UserNotActivatedError(BaseExceptionError):
    def __init__(
        self,
        message="User not activated",
        status_code: int = 401,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class IncorrectPasswordError(BaseExceptionError):
    def __init__(
        self,
        message="Incorrect password",
        status_code: int = 401,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class AuthenticationFailedError(BaseExceptionError):
    def __init__(
        self,
        message="Authentication Failed",
        status_code: int = 401,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class InvalidTokenError(BaseExceptionError):
    def __init__(
        self,
        message="Invalid token provided",
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class AccessTokenExpiredError(BaseExceptionError):
    def __init__(
        self,
        message="Access token expired",
        status_code: int = 401,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class RefreshTokenExpiredError(BaseExceptionError):
    def __init__(
        self,
        message="Refresh token expired",
        status_code: int = 401,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)


class RefreshTokenNotProvidedError(BaseExceptionError):
    def __init__(
        self,
        message="No refresh token found in header",
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message=self.message, status_code=self.status_code)
