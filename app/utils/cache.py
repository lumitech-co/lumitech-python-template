import asyncio
import socket
from functools import cache

from redis import exceptions
from redis.asyncio import BlockingConnectionPool, Redis
from redis.asyncio.retry import Retry
from redis.backoff import ConstantBackoff

from app.settings import settings
from app.utils.constants import ONE_MINUTE_SECONDS

REDIS_MAX_RETRIES = 10
REDIS_MAX_CONNECTIONS = 20
REDIS_CACHE_RETRYABLE_ERRORS = (
    ConnectionError,
    exceptions.ConnectionError,
    exceptions.TimeoutError,
    exceptions.BusyLoadingError,
    asyncio.exceptions.TimeoutError,
    socket.gaierror,
)


def async_redis_connection_pool() -> BlockingConnectionPool:
    return BlockingConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        decode_responses=True,
        socket_keepalive=True,
        max_connections=REDIS_MAX_CONNECTIONS,
        timeout=ONE_MINUTE_SECONDS,
        retry=Retry(
            backoff=ConstantBackoff(ONE_MINUTE_SECONDS),
            retries=REDIS_MAX_RETRIES,
            supported_errors=REDIS_CACHE_RETRYABLE_ERRORS,  # type: ignore[arg-type]
        ),
        protocol=3,
    )


@cache
def async_redis() -> Redis:
    return Redis.from_pool(async_redis_connection_pool())
