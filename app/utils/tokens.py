from datetime import UTC, datetime, timedelta
from typing import Any

from jwt import PyJWTError, decode, encode

from app.settings import settings


def create_jwt(*, data: dict[str, Any] | None = None, expire_time_s: int | None = None) -> str:
    data = data or {}
    if expire_time_s:
        data.update({"exp": datetime.now(UTC) + timedelta(seconds=expire_time_s)})
    return encode(data, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_jwt(token: str) -> dict[str, Any] | None:
    try:
        return decode(token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm)
    except PyJWTError:
        return None
