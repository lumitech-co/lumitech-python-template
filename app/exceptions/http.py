from fastapi import HTTPException, status


class HTTPBadRequestException(HTTPException):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail or "Bad request",
        )


class HTTPUnauthorizedException(HTTPException):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail=detail or "Unauthorized",
        )


class HTTPForbiddenException(HTTPException):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail or "Access denied",
        )


class HTTPNotFoundException(HTTPException):
    def __init__(self, model_name: str, obj_id: int | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_name} with ID {obj_id} not found" if obj_id else f"{model_name} not found",
        )


class HTTPConflictException(HTTPException):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail or "Conflict",
        )


class HTTPInternalServerException(HTTPException):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail or "Internal Server Error",
        )
