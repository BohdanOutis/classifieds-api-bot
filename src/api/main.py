from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..tasks.scheduler import check_expired_vip_statuses
from src.api.v1.router import router as api_v1_router
from ..core.security import verify_api_key

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


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_v1_router,
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)]
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}