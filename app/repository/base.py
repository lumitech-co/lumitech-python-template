from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import desc as sa_desc, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import Base
from app.utils.constants import DEFAULT_DESC, DEFAULT_ORDER_BY

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaCreateType = TypeVar("SchemaCreateType", bound=BaseModel)
SchemaUpdateType = TypeVar("SchemaUpdateType", bound=BaseModel)


class BaseRepository(Generic[DBModelType, SchemaCreateType, SchemaUpdateType]):  # noqa: UP046
    def __init__(self, db_model: type[DBModelType]) -> None:
        self.db_model = db_model

    async def fetch_one(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[Any] | None = None,
        order_by: Any = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> DBModelType | None:
        filters = filters or []

        if desc:
            order_by = sa_desc(order_by)

        query = select(self.db_model).filter(*filters).filter_by(**kwargs).order_by(order_by)

        if options:
            query = query.options(*options)

        return (await session.execute(query)).scalars().first()

    async def fetch(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[Any] | None = None,
        order_by: Any = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> Any | None:
        filters = filters or []

        if desc:
            order_by = sa_desc(order_by)

        query = select(self.db_model).filter(*filters).filter_by(**kwargs).order_by(order_by)

        if options:
            query = query.options(*options)

        return await paginate(session, query)

    async def fetch_all(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[Any] | None = None,
        order_by: Any = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> Sequence[DBModelType] | None:
        filters = filters or []

        if desc:
            order_by = sa_desc(order_by)

        query = select(self.db_model).filter(*filters).filter_by(**kwargs).order_by(order_by)

        if options:
            query = query.options(*options)

        return (await session.execute(query)).scalars().all()

    async def create(
        self, create_obj: SchemaCreateType | dict[str, Any], session: AsyncSession, *, is_flush: bool = False
    ) -> DBModelType:
        db_obj = (
            self.db_model(**create_obj) if isinstance(create_obj, dict) else self.db_model(**create_obj.model_dump())
        )

        session.add(db_obj)

        if is_flush:
            await session.flush()

        else:
            await session.commit()
            await session.refresh(db_obj)

        return db_obj

    async def create_bulk(
        self, payload: list[dict[str, Any]], session: AsyncSession, *, is_flush: bool = False
    ) -> None:
        await session.execute(insert(self.db_model).values(payload))

        if is_flush:
            await session.flush()

        else:
            await session.commit()

    @staticmethod
    async def update(
        db_obj: DBModelType,
        update_obj: SchemaUpdateType | dict[str, Any],
        session: AsyncSession,
        *,
        is_flush: bool = False,
    ) -> DBModelType:
        data = update_obj if isinstance(update_obj, dict) else update_obj.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(db_obj, key, value)

        session.add(db_obj)

        if is_flush:
            await session.flush()

        else:
            await session.commit()
            await session.refresh(db_obj)

        return db_obj

    @staticmethod
    async def delete(db_obj: DBModelType, session: AsyncSession, *, is_flush: bool = False) -> None:
        if is_flush:
            await session.delete(db_obj)
            await session.flush()

        else:
            await session.delete(db_obj)
            await session.commit()
