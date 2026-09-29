from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..services.parser import fetch_fresh_news
from ..services.publisher import publish_news_item
from ...tasks.scheduler import check_expired_vip_statuses

import httpx

async def parse_and_publish_job(bot: Bot, api_client: httpx.AsyncClient):
    fresh_news = await fetch_fresh_news(api_client=api_client)

    for item in fresh_news:
        await publish_news_item(bot, api_client, item)

def setup_scheduler(bot: Bot, api_client: httpx.AsyncClient) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        parse_and_publish_job,
        trigger="interval",
        minutes=20,
        kwargs={"bot": Bot, "api_client": api_client}
    )

    scheduler.add_job(
        check_expired_vip_statuses,
        trigger="interval",
        minutes=720,
    )

    return scheduler