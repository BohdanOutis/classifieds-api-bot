from fastapi import FastAPI

from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..tasks.scheduler import check_expired_vip_statuses
from src.api.v1.router import router as api_v1_router

# scheduler = AsyncIOScheduler()

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     scheduler.add_job(
#         check_expired_vip_statuses,
#         trigger='interval',
#         minutes=15,
#         id="check_vip_expiration",
#         replace_existing=True
#     )

#     scheduler.start()
#     yield
#     scheduler.shutdown()

app = FastAPI()
app.include_router(api_v1_router, prefix="/api/v1")