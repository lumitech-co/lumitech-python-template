from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()
metadata = Base.metadata


class BaseDBModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} (id={self.id})>"
