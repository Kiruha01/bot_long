from fastapi import APIRouter, BackgroundTasks, Request

from app.bot.bot import bot
from app.bot.handlers import dp

router = APIRouter()


@router.post("/examer_wh")
async def readw_root(r: Request, background_tasks: BackgroundTasks) -> None:
    background_tasks.add_task(dp.feed_raw_update, bot, await r.json())
