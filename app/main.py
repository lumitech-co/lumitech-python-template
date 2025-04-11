import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination
from starlette.middleware.sessions import SessionMiddleware

from app.database.engine import session_manager
from app.exceptions.handlers import internal_error_exception_handler, validation_error_exception_handler
from app.routes.misc import router as router_misc
from app.routes.user import router as router_user
from app.settings import settings

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(levelname)-9s %(asctime)-15s [%(name)s] %(filename)s/%(funcName)s: %(message)s",
)

ROUTERS = (
    router_user,
    router_misc,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    yield
    await session_manager.close_connection()


app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    responses={
        422: {
            "description": "Unprocessable Entity Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Validation Error",
                        "errors": [
                            {
                                "type": "string",
                                "loc": ["string"],
                                "msg": "string",
                            }
                        ],
                        "body": {},
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {"application/json": {"example": {"detail": "Internal Server Error"}}},
        },
    },
)

add_pagination(app)

app.add_exception_handler(RequestValidationError, validation_error_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(Exception, internal_error_exception_handler)

for router in ROUTERS:
    app.include_router(router)


def _openapi_schema() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    title = "FastAPI"
    version = "1.0.0"

    openapi_schema = get_openapi(title=title, version=version, routes=app.routes)
    openapi_schema["info"] = {"title": title, "version": version}

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = _openapi_schema  # type: ignore[method-assign]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.backend_host_url,
        settings.frontend_host_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
