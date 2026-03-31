from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.exceptions import IncorrectTokenException, NoAccessTokenHTTPException
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


# Query параметр нельзя использовать в pydantic схеме
# pydantic не привязан к FastAPI
# а FastAPI привязан к pydantic

# class PaginationParams(BaseModel):
#     page: int | None = Query(None, gt=1)
#     per_page: int | None = Query(None, gt=1, lt=30)


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
         raise NoAccessTokenHTTPException()
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenException()
    return data["user_id"]


UserIdDepends = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
