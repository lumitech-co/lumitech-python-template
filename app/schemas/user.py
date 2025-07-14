from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseCreateSchema, BaseReadSchema, BaseUpdateSchema
from app.utils.mixins import EmailLowerCaseMixin, PasswordComplexityMixin, PasswordHashMixin


class UserBase(BaseModel, EmailLowerCaseMixin):
    email: str


class UserCreate(BaseCreateSchema, UserBase, PasswordComplexityMixin, PasswordHashMixin, EmailLowerCaseMixin):
    email: EmailStr = Field(max_length=100)
    password: str = Field(max_length=50)


class UserRead(BaseReadSchema, UserBase):
    pass


class UserUpdate(BaseUpdateSchema):
    email: EmailStr | None = Field(None, max_length=100)
