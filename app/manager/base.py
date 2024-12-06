from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from fastapi import Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.http import HTTPBadRequestException, HTTPNotFoundException
from app.repository.base import BaseRepository, DBModelType, SchemaCreateType, SchemaUpdateType
from app.utils.constants import DEFAULT_DESC, DEFAULT_ORDER_BY

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)  # type: ignore[type-arg]


class BaseManager(Generic[DBModelType, RepositoryType, SchemaCreateType, SchemaUpdateType]):
    def __init__(self, db_model: type[DBModelType], repository: type[RepositoryType]) -> None:
        self.db_model = db_model
        self.repository = repository(self.db_model)

    async def fetch_one(
        self,
        *,
        filters: list[Any] | None = None,
        order_by: str = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> DBModelType:
        try:
            order_by = getattr(self.db_model, order_by)
        except AttributeError:
            raise HTTPBadRequestException from None

        if kwargs:
            for key in kwargs:
                if not hasattr(self.db_model, key):
                    raise HTTPBadRequestException

        db_obj = await self.repository.fetch_one(
            filters=filters, order_by=order_by, desc=desc, session=session, **kwargs
        )

        if not db_obj:
            raise HTTPNotFoundException(model_name=self.db_model.__name__)

        return db_obj

    async def fetch(
        self,
        *,
        filters: list[Any] | None = None,
        order_by: str = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        offset: int | None = None,
        limit: int | None = None,
        session: AsyncSession,
        **kwargs: Any,
    ) -> Sequence[DBModelType] | None:
        try:
            order_by = getattr(self.db_model, order_by)
        except AttributeError:
            raise HTTPBadRequestException from None

        if kwargs:
            for key in kwargs:
                if not hasattr(self.db_model, key):
                    raise HTTPBadRequestException

        return await self.repository.fetch(
            filters=filters, order_by=order_by, desc=desc, offset=offset, limit=limit, session=session, **kwargs
        )

    async def create(self, create_obj: SchemaCreateType, session: AsyncSession) -> DBModelType:
        return await self.repository.create(create_obj, session)

    async def update(self, db_obj_id: int, update_obj: SchemaUpdateType, session: AsyncSession) -> DBModelType:
        db_obj = await self.fetch_one(id=db_obj_id, session=session)
        return await self.repository.update(db_obj, update_obj, session)

    async def delete(self, db_obj_id: int, session: AsyncSession) -> Response:
        db_obj = await self.repository.fetch_one(id=db_obj_id, session=session)

        if not db_obj:
            raise HTTPNotFoundException(model_name=self.db_model.__name__)

        await self.repository.delete(db_obj, session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
