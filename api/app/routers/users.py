from fastapi import APIRouter, Depends, HTTPException, Security
from starlette import status

from app.auth import session_cookie_scheme
from app.db.generated.models import User
from app.db.generated.users import AsyncQuerier, UpdateUserParams
from app.db.queriers import get_user_async_querier
from app.schemas.users import UpdateUserSchema

router = APIRouter(
    prefix="/users", tags=["users"], dependencies=[Security(session_cookie_scheme)]
)


@router.get("/", response_model=User)
async def get_user(id: str, querier: AsyncQuerier = Depends(get_user_async_querier)):
    user = querier.get_user(id=id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.patch("/{id}", response_model=User)
async def update_user(
    id: str,
    body: UpdateUserSchema,
    querier: AsyncQuerier = Depends(get_user_async_querier),
):
    user = querier.update_user(
        UpdateUserParams(id=id, **body.model_dump(exclude_none=True))
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return user
