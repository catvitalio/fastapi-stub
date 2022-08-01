from typing import Callable, Awaitable

from db.events import connect_to_db, close_db_connection
from fastapi import FastAPI


def register_startup(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.

    This function uses FastAPI app to store data
    in the state, such as db_engine.

    :return: function that actually performs actions.
    """
    @app.on_event('startup')
    async def _startup() -> None:
        connect_to_db(app)
        pass

    return _startup


def register_shutdown(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application's shutdown.

    :return: function that actually performs actions.
    """
    @app.on_event('shutdown')
    async def _shutdown() -> None:
        await close_db_connection(app)
        pass

    return _shutdown
