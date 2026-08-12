from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.models.news_sources import NewsSources
from ..schemas.news_source import NewsSourceRespose

router = APIRouter()

@router.get("/", response_model=List[NewsSourceRespose])
async def get_active_sources(
    session: AsyncSession = Depends(get_async_session)
):
    query = select(NewsSources).where(NewsSources.is_active == True)
    result = await session.execute(query)
    return list(result.scalars().all())