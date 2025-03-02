from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.home_router import home_page_router
from app.api.middlewares import register_middlewares
from app.config import MySettings


def register_router(app: FastAPI) -> FastAPI:
    from app.api.v1 import api_v1_router

    app.include_router(home_page_router)
    app.include_router(api_v1_router)
    return app


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


def create_app():
    app = FastAPI(
        title=f"AI-Underwriter - {MySettings.ENVIRONMENT.name}",
        lifespan=lifespan,
    )
    register_router(app)
    app = register_middlewares(app)
    return register_exception_handlers(app)


__all__ = ["create_app"]
