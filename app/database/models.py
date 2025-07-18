from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseDBModel


class User(BaseDBModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
