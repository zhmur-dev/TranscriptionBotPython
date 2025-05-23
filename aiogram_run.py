import asyncio
import logging

from aiogram.types import BotCommand, BotCommandScopeDefault

from src.config.create_bot import bot, create_tg_server_workdir, dp
from src.handlers.local import local_router
from src.handlers.questions import questions_router
from src.handlers.start import start_router
from src.handlers.yandex import yandex_router


async def set_commands():
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Start'),
            BotCommand(command='local', description='Transcribe from local file'),
            BotCommand(command='yandex', description='Transcribe from Yandex Disk'),
            BotCommand(command='questions', description='Extract questions from .txt file'),
        ],
        BotCommandScopeDefault(),
    )


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await create_tg_server_workdir()
    await set_commands()
    dp.include_routers(
        start_router,
        local_router,
        yandex_router,
        questions_router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
    )
    logger = logging.getLogger(__name__)
    asyncio.run(main())
