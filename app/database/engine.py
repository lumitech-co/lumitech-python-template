from collections.abc import AsyncIterator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.exceptions.database import DatabaseInitializationError
from app.settings import settings

Base = declarative_base()
metadata = Base.metadata


class DatabaseSessionManager:
    def __init__(self, db_url: str, engine_kwargs: dict[str, Any] | None = None) -> None:
        self._engine: AsyncEngine | None = create_async_engine(
            db_url, pool_size=30, pool_pre_ping=True, pool_recycle=1800, max_overflow=15, **(engine_kwargs or {})
        )
        self.session_maker: async_sessionmaker[AsyncSession] | None = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            bind=self._engine,
        )

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        if self.session_maker is None:
            raise DatabaseInitializationError

        session = self.session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close_connection(self) -> None:
        if self._engine is None:
            raise DatabaseInitializationError
        await self._engine.dispose()

        self._engine = None
        self.session_maker = None


session_manager: DatabaseSessionManager = DatabaseSessionManager(settings.db_url, {"echo": settings.echo_sql})
