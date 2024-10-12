from typing import Callable

from fastapi import FastAPI, Request, Response
from loguru import logger

from app.api.router import router
from app.bot.bot import bot
from app.settings import settings


async def startup() -> None:
    # init_logging()
    wh_url = f"{settings.BASE_URL}examer_wh"
    logger.info(f"Webhook url: {wh_url}")

    cert = settings.get_cert_file()
    res = await bot.set_webhook(
        url=wh_url,
        certificate=cert,
    )
    logger.info(f"Webhook response: {res}")


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

    @application.middleware("http")
    async def logger_middleware(  # noqa: WPS430
        request: Request, call_next: Callable
    ) -> Response:
        logger.info(f"{request.method} {request.url}")
        return await call_next(request)

    return application
