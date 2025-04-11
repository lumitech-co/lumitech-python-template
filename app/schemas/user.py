from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.utils.mixins import (
    CreatedAtComputeMixin,
    EmailLowerCaseMixin,
    PasswordComplexityMixin,
    PasswordHashMixin,
    UpdatedAtComputeMixin,
)


class UserBase(BaseModel, EmailLowerCaseMixin):
    email: str


class UserCreate(
    UserBase,
    PasswordComplexityMixin,
    PasswordHashMixin,
    EmailLowerCaseMixin,
    CreatedAtComputeMixin,
    UpdatedAtComputeMixin,
):
    email: EmailStr = Field(max_length=100)
    password: str = Field(max_length=50)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    email: str
    id: int


class UserUpdate(BaseModel, UpdatedAtComputeMixin):
    email: EmailStr | None = Field(None, max_length=100)
