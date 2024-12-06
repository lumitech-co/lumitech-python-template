from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import session_manager

DatabaseSessionDependency = Annotated[AsyncSession, Depends(session_manager.get_session)]
