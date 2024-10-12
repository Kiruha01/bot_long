import loguru
from aiogram import Dispatcher, types
from aiogram.filters import Command

from app.bot.bot import bot
from app.examer.controller import controller

dp = Dispatcher()


@dp.message()
async def message_handler(message: types.Message) -> None:
    try:
        loguru.logger.info(f"{message.text} from {message.from_user.id}")  # type: ignore
        if message.text is None:
            return

        if "examer.ru" not in message.text or not message.text.startswith("http"):
            await bot.send_message(chat_id=message.from_user.id, text="Неверная ссылка")  # type: ignore
            return

        if not await controller.check_auth():
            await controller.auth()

        await bot.send_message(chat_id=message.from_user.id, text="Ищу ответы....")  # type: ignore

        test = await controller.process_link(message.text)

        await bot.send_message(
            chat_id=message.from_user.id,
            text=(
                f"Всего баллов: {test.score}\n"
                "🌚 - сколько баллов дает задание\n"
                f"Примерное время выполнения теста: {test.avg_time} минут"
            ),
        )  # type: ignore

        for task in test.get_tasks():
            await bot.send_message(chat_id=message.from_user.id, text=task.formatted_question)  # type: ignore

    except Exception as e:
        loguru.logger.opt(exception=e).error("Error processing message")
        await bot.send_message(chat_id=message.from_user.id, text="Что-то пошло не так. Гляньте логи")  # type: ignore


@dp.message(Command("start"))
async def start_handler(message: types.Message) -> None:
    await bot.send_message(
        chat_id=message.from_user.id, text="Скидывай ссылку на examer"
    )
