from typing import TYPE_CHECKING

from fastapi import Request

if TYPE_CHECKING:
    from logging import Logger


def get_logger(request: Request) -> "Logger":
    return request.state.logger
