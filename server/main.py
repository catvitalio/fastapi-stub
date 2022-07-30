from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings


def get_application():
    _app = FastAPI()

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return _app


app = get_application()
