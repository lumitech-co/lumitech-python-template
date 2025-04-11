import re
from datetime import UTC, datetime
from typing import Any

from pydantic import computed_field, field_validator, model_validator

from app.exceptions.http import HTTPBadRequestException
from app.utils.secrets import hash_secret


class PasswordHashMixin:
    @field_validator("password", mode="after", check_fields=False)
    @classmethod
    def hash_password(cls, v: str) -> str:
        return hash_secret(v)


class PasswordComplexityMixin:
    @field_validator("password", mode="before", check_fields=False)
    @classmethod
    def password_validator(cls, password: str) -> str:
        if not re.match(r"^(?=.*[A-Z])(?=.*\d)[\s\S]{8,50}$", password):
            raise HTTPBadRequestException(detail="Password must contain at least 1 uppercase letter and 1 number")
        return password


class PasswordMatchMixin:
    @model_validator(mode="before")
    @classmethod
    def verify_password_match(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data["password"] != data["password_confirm"]:
            raise HTTPBadRequestException(detail="Passwords do not match")
        return data


class EmailLowerCaseMixin:
    @field_validator("email", check_fields=False)
    @classmethod
    def change_email_case(cls, v: str | None) -> str | None:
        return v.lower() if v else None


class CreatedAtComputeMixin:
    @computed_field  # type: ignore[prop-decorator]
    @property
    def created_at(self) -> datetime:
        return datetime.now(UTC).replace(tzinfo=None)


class UpdatedAtComputeMixin:
    @computed_field  # type: ignore[prop-decorator]
    @property
    def updated_at(self) -> datetime:
        return datetime.now(UTC).replace(tzinfo=None)
