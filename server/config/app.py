from typing import Awaitable, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router
from config.dependencies import get_settings
from config.settings import Settings
from db.events import connect_to_db, close_db_connection


class AppComposer:
    app: FastAPI
    settings: Settings

    def __init__(self) -> None:
        self.app = FastAPI()
        self.settings = get_settings()

    def compose(self) -> FastAPI:
        self._register_startup_events()
        self._register_shutdown_events()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in self.settings.CORS_ALLOWED_ORIGINS],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self.app.include_router(api_router, prefix='/api')

        return self.app

    def _register_startup_events(self) -> Callable[[], Awaitable[None]]:
        """
        Actions to run on application startup.

        This function uses FastAPI app to store data
        in the state, such as db_engine.

        :return: function that actually performs actions.
        """
        @self.app.on_event('startup')
        async def _startup() -> None:
            connect_to_db(self.app)
            pass

        return _startup

    def _register_shutdown_events(self) -> Callable[[], Awaitable[None]]:
        """
        Actions to run on application's shutdown.

        :return: function that actually performs actions.
        """
        @self.app.on_event('shutdown')
        async def _shutdown() -> None:
            await close_db_connection(self.app)
            pass

        return _shutdown


def get_app() -> FastAPI:
    return AppComposer().compose()
