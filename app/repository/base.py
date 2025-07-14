from collections.abc import Sequence
from typing import Any

from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import delete, desc as sa_desc, exists as sa_exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.database.base import Base
from app.utils.constants import DEFAULT_DESC, DEFAULT_ORDER_BY
from app.utils.pagination import Page


class BaseRepository[DBModelType: Base, SchemaCreateType: BaseModel, SchemaUpdateType: BaseModel]:
    def __init__(self, db_model: type[DBModelType]) -> None:
        self.db_model = db_model

    async def fetch_one(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[ExecutableOption] | None = None,
        order_by: Any = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> DBModelType | None:
        filters = filters or []

        query = select(self.db_model).filter(*filters).filter_by(**kwargs)

        if order_by is not None:
            query = query.order_by(sa_desc(order_by) if desc else order_by)

        if options:
            query = query.options(*options)

        return (await session.execute(query)).scalars().first()

    async def fetch_paginated(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[ExecutableOption] | None = None,
        order_by: Any = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> Page[DBModelType]:
        filters = filters or []

        query = select(self.db_model).filter(*filters).filter_by(**kwargs)

        if order_by is not None:
            query = query.order_by(sa_desc(order_by) if desc else order_by)

        if options:
            query = query.options(*options)

        return await paginate(session, query)

    async def fetch_bulk(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[ExecutableOption] | None = None,
        order_by: Any = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        limit: int | None = None,
        session: AsyncSession,
        **kwargs: Any,
    ) -> Sequence[DBModelType] | None:
        filters = filters or []

        query = select(self.db_model).filter(*filters).filter_by(**kwargs)

        if order_by is not None:
            query = query.order_by(sa_desc(order_by) if desc else order_by)

        if options:
            query = query.options(*options)

        if limit is not None:
            query.limit(limit)

        return (await session.execute(query)).scalars().all()

    async def exists(self, session: AsyncSession, *, filters: list[Any] | None = None, **kwargs: Any) -> bool:
        filters = filters or []
        filters_by = [getattr(self.db_model, key) == value for key, value in kwargs.items()] if kwargs else []
        return bool((await session.execute(select(sa_exists().where(*filters, *filters_by)))).scalar())

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

    async def update_bulk(
        self,
        payload: dict[str, Any],
        session: AsyncSession,
        *,
        filters: list[Any] | None = None,
        is_flush: bool = False,
        **kwargs: Any,
    ) -> None:
        filters = filters or []

        await session.execute(update(self.db_model).filter(*filters).filter_by(**kwargs).values(payload))

        if is_flush:
            await session.flush()

        else:
            await session.commit()

    @staticmethod
    async def delete(db_obj: DBModelType, session: AsyncSession, *, is_flush: bool = False) -> None:
        if is_flush:
            await session.delete(db_obj)
            await session.flush()

        else:
            await session.delete(db_obj)
            await session.commit()

    async def delete_bulk(
        self, *, filters: list[Any] | None = None, session: AsyncSession, is_flush: bool = False, **kwargs: Any
    ) -> None:
        filters = filters or []

        await session.execute(delete(self.db_model).filter(*filters).filter_by(**kwargs))

        if is_flush:
            await session.flush()

        else:
            await session.commit()
