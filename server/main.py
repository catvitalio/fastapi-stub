import uvicorn

from config.dependencies import get_settings


def main() -> None:
    settings = get_settings()

    uvicorn.run(
        'config.app:get_app',
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS_COUNT,
        log_level=settings.LOG_LEVEL.value,
        factory=True,
    )


if __name__ == "__main__":
    main()
