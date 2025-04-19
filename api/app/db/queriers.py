from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.generated import guilds, users
from app.db.utils import get_db_async, get_db_sync


def get_guild_querier(conn: Session = Depends(get_db_sync)):
    return guilds.Querier(conn)


async def get_guild_async_querier(conn: AsyncSession = Depends(get_db_async)):
    return guilds.AsyncQuerier(conn)


def get_user_querier(conn: Session = Depends(get_db_sync)):
    return users.Querier(conn)


async def get_user_async_querier(conn: AsyncSession = Depends(get_db_async)):
    return users.AsyncQuerier(conn)
