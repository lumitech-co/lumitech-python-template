from typing import TypeVar

from fastapi import Query
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.customization import (
    CustomizedPage,
    UseFieldsAliases,
    UseIncludeTotal,
    UseName,
    UseParamsFields,
    UseQuotedCursor,
)

T = TypeVar("T")
PAGE_SIZE_DEFAULT = 10

Page = CustomizedPage[
    CursorPage[T],
    UseName("Paginated"),
    UseIncludeTotal(True),  # noqa: FBT003
    UseQuotedCursor(False),  # noqa: FBT003
    UseParamsFields(
        size=Query(PAGE_SIZE_DEFAULT, ge=1, le=100, alias="pageSize"),
        cursor=Query(None, alias="pageToken"),
    ),
    UseFieldsAliases(
        items="data",
        current_page="currentPage",
        current_page_backwards="currentPageBackwards",
        previous_page="previousPage",
        next_page="nextPage",
    ),
]
