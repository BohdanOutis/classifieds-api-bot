from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import structlog

from ..schemas.payment import PaymentCreate
from src.models.advertisement import Advertisement, AdvertisementStatus

async def get_ad_or_404(session: AsyncSession, advert_id):
    query = (
        select(Advertisement)
        .where(Advertisement.id == advert_id)
    )
    result = await session.execute(query)
    advert = result.scalar_one_or_none()
    if not advert:
        raise HTTPException(
            status_code=404,
            detail="Advert not found"
        )
    return advert