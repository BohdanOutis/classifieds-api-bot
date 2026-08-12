import asyncio
import structlog
from structlog.typing import FilteringBoundLogger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from ..core.config import config
from .handlers import get_routers
from ..core.logging_config import get_structlog_config
from ..core.database import async_sessionmaker
from .middlewares.db import DbSessionMiddleware
from .middlewares.http_client import HttpClientMiddleware
from .tasks.scheduler import setup_scheduler
import httpx


logger: FilteringBoundLogger = structlog.get_logger()

async def main() -> None:
    import hupper
    
    # Hupper починає стежити за файлами. 
    # Якщо щось зміниться, він сам перезапустить цей же процес Python.
    reloader = hupper.start_reloader("src.bot.__main__.main")
    
    structlog.configure(**get_structlog_config(config.logs))

    bot = Bot(
        token=config.bot.token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()
    dp.include_routers(*get_routers())

    dp.update.middleware(DbSessionMiddleware(session_maker=async_sessionmaker))
    dp.update.middleware(HttpClientMiddleware(api_base_url=config.api.base_url))

    scheduler = setup_scheduler(bot, httpx.AsyncClient(base_url=config.api.base_url, timeout=10.0, follow_redirects=True))
    scheduler.start()

    await logger.ainfo("Starting polling...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await logger.ainfo("Bot stopped")


asyncio.run(main()) 