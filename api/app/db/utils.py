from contextlib import asynccontextmanager, contextmanager

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=not settings.IN_PRODUCTION,
    future=True,
)

sync_engine = create_engine(
    settings.DATABASE_URL_SYNC,
    echo=not settings.IN_PRODUCTION,
    future=True,
)

sync_session_maker = sessionmaker(
    bind=sync_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)


def get_db_sync():
    session = sync_session_maker()
    try:
        yield session
    except DatabaseError as e:
        logger.exception(e)
        raise
    finally:
        session.close()


async def get_db_async():
    session = async_session_maker()
    try:
        yield session
    except DatabaseError as e:
        logger.exception(e)
        raise
    finally:
        await session.close()


get_db_context_sync = contextmanager(get_db_sync)
get_db_context_async = asynccontextmanager(get_db_async)
