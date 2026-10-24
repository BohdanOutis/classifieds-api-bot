import time
import structlog
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .v1.services.users import expire_vip_statuses
from src.api.v1.router import router as api_v1_router
from ..core.security import verify_api_key
from ..core.database import get_async_session
from src.core.database import async_sessionmaker

logger = structlog.get_logger()

async def check_vip_job():
    async with async_sessionmaker() as session:
        try:
            count = await expire_vip_statuses(session=session)
            if count > 0:
                logger.info("vip_statuses_expired", count=count)
        except Exception as e:
            logger.error("vip_expiration_job_failed", error=str(e))

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("application_startup")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_vip_job, trigger="interval", minutes=720)
    scheduler.start()
    logger.info("scheduler_started", interval_minutes=720)

    yield

    logger.info("application_shutdown")
    scheduler.shutdown()
    logger.info("scheduler_stopped")

app = FastAPI(lifespan=lifespan)

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

@app.middleware("http")
async def structlog_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        "http_request_processed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round(duration * 1000, 2)
    )
    return response

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(
        "database_unhandled_error",
        error=str(exc),
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal database error. Please try again later."},
    )

app.include_router(
    api_v1_router,
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)]
)

@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(text("SELECT 1"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database is unhealthy: {str(e)}"
        )
    return {"status": "ok", "database": "connected"}