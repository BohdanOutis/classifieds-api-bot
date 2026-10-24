from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import httpx
import structlog

from ..services.parser import fetch_fresh_news
from ..services.publisher import publish_news_item

logger = structlog.get_logger()

async def parse_and_publish_job(bot: Bot, api_client: httpx.AsyncClient):
    fresh_news = await fetch_fresh_news(api_client=api_client)

    for item in fresh_news:
        await publish_news_item(bot, api_client, item)


def setup_scheduler(bot: Bot, api_client: httpx.AsyncClient) -> AsyncIOScheduler:
    logger.info("application_startup")
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        parse_and_publish_job,  
        trigger="interval",
        minutes=20,
        kwargs={"bot": bot, "api_client": api_client}
    )
    logger.info("scheduler_started", interval_minutes=20)
    return scheduler