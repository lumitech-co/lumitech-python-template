from typing import Any

from fastapi import Response, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.database.base import Base
from app.exceptions.http import HTTPBadRequestException, HTTPNotFoundException
from app.repository.base import BaseRepository
from app.utils.constants import DEFAULT_DESC, DEFAULT_ORDER_BY
from app.utils.misc import camel_to_snake
from app.utils.pagination import Page


class BaseManager[DBModelType: Base, SchemaCreateType: BaseModel, SchemaUpdateType: BaseModel]:
    def __init__(
        self,
        db_model: type[DBModelType],
        repository: type[BaseRepository[DBModelType, SchemaCreateType, SchemaUpdateType]],
    ) -> None:
        self.db_model = db_model
        self.repository = repository(self.db_model)

    def _get_order_by(self, order_by: str) -> Any:
        order_by = camel_to_snake(order_by)

        if order_by in {"id", "created_at", "updated_at"}:
            return order_by

        try:
            return getattr(self.db_model, order_by)
        except AttributeError as exc:
            raise HTTPBadRequestException(detail="Invalid value for `orderBy`") from exc

    def _validate_kwargs(self, **kwargs: Any) -> None:
        if kwargs:
            for key in kwargs:
                if not hasattr(self.db_model, key):
                    raise HTTPBadRequestException(detail="Invalid field provided")

    async def fetch_one(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[ExecutableOption] | None = None,
        order_by: str = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> DBModelType:
        order_by = self._get_order_by(order_by)
        self._validate_kwargs(**kwargs)

        db_obj = await self.repository.fetch_one(
            filters=filters, options=options, order_by=order_by, desc=desc, session=session, **kwargs
        )

        if not db_obj:
            raise HTTPNotFoundException(model_name=self.db_model.__name__)

        return db_obj

    async def fetch_paginated(
        self,
        *,
        filters: list[Any] | None = None,
        options: list[ExecutableOption] | None = None,
        order_by: str = DEFAULT_ORDER_BY,
        desc: bool = DEFAULT_DESC,
        session: AsyncSession,
        **kwargs: Any,
    ) -> Page[DBModelType]:
        order_by = self._get_order_by(order_by)
        self._validate_kwargs(**kwargs)

        return await self.repository.fetch_paginated(
            filters=filters, options=options, order_by=order_by, desc=desc, session=session, **kwargs
        )

    async def exists(self, session: AsyncSession, *, filters: list[Any] | None = None, **kwargs: Any) -> bool:
        self._validate_kwargs(**kwargs)
        return await self.repository.exists(session, filters=filters, **kwargs)

    async def create(self, create_obj: SchemaCreateType, session: AsyncSession) -> DBModelType:
        return await self.repository.create(create_obj, session)

    async def update(self, db_obj_id: int, update_obj: SchemaUpdateType, session: AsyncSession) -> DBModelType:
        db_obj = await self.fetch_one(id=db_obj_id, session=session)
        return await self.repository.update(db_obj, update_obj, session)

    async def update_bulk(
        self, payload: dict[str, Any], session: AsyncSession, *, filters: list[Any] | None = None, **kwargs: Any
    ) -> None:
        self._validate_kwargs(**kwargs)
        return await self.repository.update_bulk(session=session, payload=payload, filters=filters, **kwargs)

    async def delete(self, db_obj_id: int, session: AsyncSession) -> Response:
        db_obj = await self.repository.fetch_one(id=db_obj_id, session=session)

        if not db_obj:
            raise HTTPNotFoundException(model_name=self.db_model.__name__)

        await self.repository.delete(db_obj, session)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    async def delete_bulk(self, session: AsyncSession, *, filters: list[Any] | None = None, **kwargs: Any) -> None:
        self._validate_kwargs(**kwargs)
        return await self.repository.delete_bulk(filters=filters, session=session, **kwargs)
