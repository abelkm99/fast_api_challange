from typing import cast

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.domain.commons.exceptions import BaseExceptionError


def base_exception_handler(request: Request, exc: Exception) -> Response:
    exc = cast(BaseExceptionError, exc)
    request.state.logger.error("Base Exception Occuered", exc_info=(type(exc), exc, exc.__traceback__))
    return JSONResponse(
        media_type="application/json",
        content={"error": exc.message},
        status_code=exc.status_code,
    )


def global_http_exception_handler(request: Request, exc: Exception) -> Response:
    http_exc = cast(HTTPException, exc)
    request.state.logger.error("Http Exception Occurred", exc_info=(type(exc), exc, exc.__traceback__))
    return JSONResponse(
        media_type="application/json",
        content={"error": str(exc)},
        status_code=http_exc.status_code,
    )


def global_exception_handler(request: Request, exc: Exception) -> Response:
    request.state.logger.error("Unhandlled Exception Occurred", exc_info=(type(exc), exc, exc.__traceback__))
    return JSONResponse(
        media_type="application/json",
        content={
            "error_message": "😭🙏🙏 Internal server error!! 😭😭🙏",
        },
        status_code=500,
    )


async def validation_exception_handler(request: Request, exc: Exception):
    exc = cast(RequestValidationError, exc)
    request.state.logger.error("Validation Exception Occurred", exc_info=(type(exc), exc, exc.__traceback__))

    def format_validation_error(error: RequestValidationError):
        formatted_errors = []
        for err in error.errors():
            field = ".".join(str(x) for x in err["loc"])
            message = err["msg"]
            formatted_errors.append(f"{field}: {message}")
        return formatted_errors

    return JSONResponse(
        media_type="application/json",
        content={
            "status_code": 422,
            "error": "Validation error",
            "extra": format_validation_error(exc),
        },
        status_code=422,
    )


def value_error_handler(request: Request, exc: Exception) -> Response:
    exc = cast(ValueError, exc)
    request.state.logger.error("ValueError Exception Occurred", exc_info=(type(exc), exc, exc.__traceback__))
    return JSONResponse(
        media_type="application/json",
        content={"value error": str(exc)},
        status_code=400,
    )


def register_exception_handlers(app: "FastAPI") -> "FastAPI":
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(BaseExceptionError, base_exception_handler)
    app.add_exception_handler(HTTPException, global_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    return app
