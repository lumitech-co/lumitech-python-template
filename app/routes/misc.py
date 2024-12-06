from fastapi import APIRouter, Response, status
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse, PlainTextResponse

router = APIRouter(tags=["Miscellaneous"])


@router.get(
    "/healthcheck",
    status_code=status.HTTP_200_OK,
)
def healthcheck() -> Response:
    return Response(status_code=status.HTTP_200_OK)


@router.get("/docs", include_in_schema=False)
def swagger() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="FastAPI")


@router.get("/redoc", include_in_schema=False)
def redoc() -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="FastAPI")


@router.get("/robots.txt", response_class=PlainTextResponse, include_in_schema=False)
def robots() -> str:
    return """User-Agent: *\nDisallow: /"""
