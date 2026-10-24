from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
import structlog

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.models.processed_news import ProcessedNews
from ..schemas.processed_news import ProcessedNewsCreate, ProcessedNewsResponse

logger = structlog.get_logger()

router = APIRouter()

@router.get("/", response_model=bool)
async def is_news_processed(
    news_hash: str = Query(..., description="SHA-256 news hash"),
    session: AsyncSession = Depends(get_async_session), 
) -> bool:
    query = select(exists().where(ProcessedNews.news_hash == news_hash))
    result = await session.execute(query)
    logger.info("processed_news_retrieved", news_hash=news_hash[:8])
    return bool(result.scalar())

@router.post("/", response_model=ProcessedNewsResponse)
async def save_processed_news(
    data_in: ProcessedNewsCreate,
    session: AsyncSession = Depends(get_async_session), 
):
    data = data_in.model_dump(exclude_unset=True)
    news = ProcessedNews(**data)
    session.add(news)

    try:
        await session.commit()
        await session.refresh(news)
    except Exception as e:
        await session.rollback()
        logger.info("processed_news_save_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to save news (maybe hash duplicate)"
        )
    logger.info("processed_news_created", news_id=news.id, news_title=news.title)
    return news