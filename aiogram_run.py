import asyncio
import logging

from aiogram.types import BotCommand, BotCommandScopeDefault

from src.config.create_bot import bot, dp
from src.handlers.start import start_router


async def set_commands():
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Start'),
        ],
        BotCommandScopeDefault(),
    )


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    dp.include_routers(
        start_router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
    )
    logger = logging.getLogger(__name__)
    asyncio.run(main())
