from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.engine import session_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    yield
    await session_manager.close_connection()


app = FastAPI(lifespan=lifespan)
