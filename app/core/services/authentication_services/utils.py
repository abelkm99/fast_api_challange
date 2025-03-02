import datetime
from typing import Any

import jwt

from app.config import MySettings
from app.core.domain.commons.exceptions import BaseExceptionError


def generate_new_token(data: dict[str, Any], expires_delta: datetime.timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, MySettings.SECRET_KEY, algorithm=MySettings.ALGORITHM)  # type: ignore


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, MySettings.SECRET_KEY, algorithms=[MySettings.ALGORITHM])  # type: ignore
    except jwt.PyJWTError as e:  # type: ignore
        raise BaseExceptionError(message="ERROR DECODING TOKEN", status_code=401) from e
