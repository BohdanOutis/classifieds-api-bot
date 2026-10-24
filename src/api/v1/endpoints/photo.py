from fastapi import APIRouter, Depends, Query, status
from typing import List
import structlog

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.models.ads_photo import AdvertisementPhoto
from ..schemas.photo import AdvertPhotoResponse, AdvertPhotoCreate

logger = structlog.get_logger()

router = APIRouter()

@router.post("/", response_model=List[AdvertPhotoResponse], status_code=status.HTTP_201_CREATED)
async def add_photos(
    data: AdvertPhotoCreate,
    session: AsyncSession = Depends(get_async_session)
):
    photos_to_add = [
        AdvertisementPhoto(advert_id=data.advert_id, file_id=file_id) 
        for file_id in data.file_ids
    ]
    session.add_all(photos_to_add)
    await session.commit()

    for photo in photos_to_add:
        await session.refresh(photo)

    logger.info("photos_created")

    return photos_to_add

@router.get("/", response_model=List[AdvertPhotoResponse])
async def get_advertisement_photos(
    advert_id: int = Query(..., description="ID оголошення, фото якого шукаємо"),
    session: AsyncSession = Depends(get_async_session)
):
    query = select(AdvertisementPhoto).where(AdvertisementPhoto.advert_id == advert_id)
    result = await session.execute(query)
    logger.info("photos_retrieved", advert_id=advert_id)
    return result.scalars().all()