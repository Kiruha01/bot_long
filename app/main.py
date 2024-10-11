from fastapi import FastAPI
from loguru import logger

from app.api.router import router
from app.bot.bot import bot
from app.logger import init_logging
from app.settings import settings


async def startup() -> None:
    init_logging()
    wh_url = f"{settings.BASE_URL}/examer_wh/"
    logger.info(f"Webhook url: {wh_url}")
    await bot.set_webhook(url=wh_url)


def get_application() -> FastAPI:
    """Create configured server application instance."""
    application = FastAPI(
        openapi_url=None,
        docs_url=None,
        redoc_url=None,
    )

    application.add_event_handler("startup", startup)
    # application.add_event_handler("shutdown", partial(shutdown, bot))

    application.include_router(router)

    return application
