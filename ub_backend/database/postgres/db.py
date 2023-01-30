from contextvars import ContextVar, Token
from typing import Union

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from ub_backend.core.config import app_config


session_context: ContextVar[str] = ContextVar("session_context")
session_context.set(" ")


def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


engine: AsyncEngine = create_async_engine(
    app_config.postgres.uri, echo=True, pool_recycle=3600
)

async_session_factory = sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)
session: Union[Session, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)

Base = declarative_base()


async def get_db():
    db = session()
    try:
        yield db
    finally:
        await db.close()
