from aiogram import Bot

from app.settings import settings

bot = Bot(
    token=settings.TELEGRAM_TOKEN,
)
