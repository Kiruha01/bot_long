import loguru
from aiogram import Dispatcher, types

from app.bot.bot import bot

dp = Dispatcher()


@dp.message()
async def message_handler(message: types.Message) -> None:
    loguru.logger.info(f"{message.text} from {message.from_user.id}")  # type: ignore
    await bot.send_message(chat_id=message.from_user.id, text=message.text)  # type: ignore
