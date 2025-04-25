import logging
import os

from aiofiles import os as aio_os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy

from src.config.config import settings


logger = logging.getLogger(__name__)

session = AiohttpSession(
    api=TelegramAPIServer.from_base(settings.TELEGRAM_API_URL, is_local=True)
)

bot = Bot(
    token=settings.BOT_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)


async def create_tg_server_workdir():
    await aio_os.makedirs(
        os.path.join(
            str(settings.TG_SERVER_PATH),
            settings.BOT_TOKEN,
            settings.TG_SERVER_WORKDIR
        ),
        exist_ok=True,
    )
