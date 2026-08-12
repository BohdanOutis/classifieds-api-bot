from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.models.processed_news import ProcessedNews
from ..schemas.processed_news import ProcessedNewsCreate, ProcessedNewsResponse

router = APIRouter()

@router.get("/", response_model=bool)
async def is_news_processed(
    news_hash: str = Query(..., description="SHA-256 news hash"),
    session: AsyncSession = Depends(get_async_session), 
) -> bool:
    query = select(exists().where(ProcessedNews.news_hash == news_hash))
    result = await session.execute(query)
    return bool(result.scalar())

@router.post("/", response_model=ProcessedNewsResponse)
async def save_processed_news(
    data_in: ProcessedNewsCreate,
    session: AsyncSession = Depends(get_async_session), 
):
    data = data_in.model_dump(exclude_unset=True)
    news = ProcessedNews(**data)
    session.add(news)

    await session.commit()
    await session.refresh(news)
    return news