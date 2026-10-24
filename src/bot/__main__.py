import asyncio
import structlog
from structlog.typing import FilteringBoundLogger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
import httpx

from ..core.config import config
from .handlers import get_routers
from ..core.logging_config import get_structlog_config
from ..core.database import async_sessionmaker
from .middlewares.db import DbSessionMiddleware
from .middlewares.http_client import HttpClientMiddleware
from .tasks.scheduler import setup_scheduler

structlog.configure(**get_structlog_config(config.logs))

logger: FilteringBoundLogger = structlog.get_logger()

async def main() -> None:

    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    await set_commands(bot)

    dp = Dispatcher()
    dp.include_routers(*get_routers())

    dp.update.middleware(DbSessionMiddleware(session_maker=async_sessionmaker))
    dp.update.middleware(HttpClientMiddleware(api_base_url=config.api.base_url))

    api_client = httpx.AsyncClient(base_url=config.api.base_url, timeout=10.0, follow_redirects=True)

    scheduler = setup_scheduler(bot, api_client)
    scheduler.start()

    await logger.ainfo("Starting polling...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await api_client.aclose()
        scheduler.shutdown()
        logger.info("scheduler_stopped")
        await logger.ainfo("Bot stopped")

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустити бота"),
        BotCommand(command="/profile", description="Профіль"),
        BotCommand(command="/create", description="Створити оголошення"),
        BotCommand(command="/vip", description="Придбати VIP"),
        BotCommand(command="/help", description="Отримати допомогу")
    ]
    await bot.set_my_commands(commands)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("bot_stopped_manually")