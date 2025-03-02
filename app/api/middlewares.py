from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import MySettings
from app.logger import CustomLogger


async def add_logger_to_request_state(request: Request, call_next):
    request.state.logger = CustomLogger.get_logger()
    return await call_next(request)


def register_middlewares(app: "FastAPI") -> "FastAPI":
    app.add_middleware(BaseHTTPMiddleware, add_logger_to_request_state)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=MySettings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
