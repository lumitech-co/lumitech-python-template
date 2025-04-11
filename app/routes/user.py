from typing import Any

from fastapi import APIRouter, Response, status

from app.database.models import User
from app.manager.user import user_manager
from app.routes.dependencies import DatabaseSessionDependency
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.utils.constants import DEFAULT_DESC, DEFAULT_ORDER_BY
from app.utils.pagination import Page
from app.utils.types import OrderByQuery, UserIdPath

router = APIRouter(tags=["Users"], prefix="/users")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Bad Request Error",
            "content": {"application/json": {"example": {"detail": "'Bad request' or 'Invalid value for 'orderBy'"}}},
        },
    },
    response_model=Page[UserRead],
)
async def fetch_users(
    *, order_by: OrderByQuery = DEFAULT_ORDER_BY, desc: bool = DEFAULT_DESC, session: DatabaseSessionDependency
) -> Any | None:
    return await user_manager.fetch(order_by=order_by, desc=desc, session=session)


@router.get(
    "/{userId}",
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "description": "Bad Request Error",
            "content": {"application/json": {"example": {"detail": "Bad request"}}},
        },
        404: {
            "description": "Not Found Error",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
    response_model=UserRead,
)
async def fetch_user(user_id: UserIdPath, session: DatabaseSessionDependency) -> User:
    return await user_manager.fetch_one(id=user_id, session=session)


@router.post("", response_model=UserRead)
async def create_user(user_create: UserCreate, session: DatabaseSessionDependency) -> User:
    return await user_manager.create(user_create, session)


@router.patch(
    "/{userId}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "Not Found Error",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
    response_model=UserRead,
)
async def update_user(user_id: UserIdPath, user_update: UserUpdate, session: DatabaseSessionDependency) -> User:
    return await user_manager.update(user_id, user_update, session)


@router.delete(
    "/{userId}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {
            "description": "Not Found Error",
            "content": {"application/json": {"example": {"detail": "User not found"}}},
        },
    },
)
async def delete_user(user_id: UserIdPath, session: DatabaseSessionDependency) -> Response:
    return await user_manager.delete(user_id, session)
