from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import PlainTextResponse

from app.db.generated.guilds import AsyncQuerier
from app.db.generated.models import Guild
from app.db.utils import get_async_querier
from app.schemas.guilds import CreateGuildSchema, UpdateGuildSchema

router = APIRouter(tags=["guilds"], prefix="/guilds")


@router.get("/", response_model=list[Guild])
async def list_guilds(querier: AsyncQuerier = Depends(get_async_querier)):
    return [g async for g in querier.retrieve_guilds()]


@router.get("/{id}", response_model=Guild)
async def get_guild(id: str, querier: AsyncQuerier = Depends(get_async_querier)):
    guild = await querier.retrieve_guild(id=id)
    if guild is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Guild {id=} not found"
        )
    return guild


@router.post("/", response_model=Guild)
async def create_guild(
    body: CreateGuildSchema, querier: AsyncQuerier = Depends(get_async_querier)
):
    guild = await querier.create_guild(**body.model_dump())
    if guild is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return guild


@router.patch("/{id}", response_model=Guild)
async def update_guild(
    id: str, body: UpdateGuildSchema, querier: AsyncQuerier = Depends(get_async_querier)
):
    guild = await querier.update_guild(id=id, **body.model_dump(exclude_none=True))
    if guild is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return guild


@router.delete("/{id}", response_class=PlainTextResponse)
async def delete_guild(id: str, querier: AsyncQuerier = Depends(get_async_querier)):
    guild_id = await querier.delete_guild(id=id)
    if guild_id is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return guild_id
