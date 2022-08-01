from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.dependencies import get_settings
from web.api.router import api_router
from web.events import register_startup, register_shutdown


def get_app() -> FastAPI:
    app = FastAPI()
    settings = get_settings()

    register_startup(app)
    register_shutdown(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(api_router, prefix='/api')

    return app
