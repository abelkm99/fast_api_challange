import datetime
from typing import Any

import bcrypt
import jwt

from app.config import MySettings
from app.core.domain.user.exceptions import AccessTokenExpiredError, InvalidTokenError


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
    except InvalidTokenError as e:
        raise InvalidTokenError() from e
    except jwt.ExpiredSignatureError as e:
        raise AccessTokenExpiredError() from e
    except jwt.PyJWTError as e:
        raise Exception() from e


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    hash_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hash_password)


def hash_password(*, password: str):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")
