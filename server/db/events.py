from asyncio import current_task

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from config.dependencies import get_settings


def connect_to_db(app: FastAPI) -> None:
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.
    """
    settings = get_settings()

    engine = create_async_engine(str(settings.DATABASE_URI), echo=settings.DATABASE_ECHO)
    session_factory = async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


async def close_db_connection(app: FastAPI) -> None:
    await app.state.db_engine.dispose()
