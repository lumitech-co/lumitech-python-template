from typing import Annotated

from fastapi import Path, Query
from pydantic import PositiveInt

OrderByQuery = Annotated[str, Query(alias="orderBy")]
UserIdPath = Annotated[PositiveInt, Path(alias="userId")]
UserIdQuery = Annotated[PositiveInt, Query(alias="userId")]
