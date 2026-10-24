from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import Optional, List
import structlog

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.models.user import User
from src.models.advertisement import Advertisement
from ..schemas.ad import AdvertCreate, AdvertResponse, AdvertUpdate

logger = structlog.get_logger()

router = APIRouter()

@router.post("/", response_model=AdvertResponse, status_code=status.HTTP_201_CREATED)
async def add_advertisement(
    advert: AdvertCreate,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.tg_id == advert.tg_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("user_not_found", user_tg_id=advert.tg_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Користувача не знайдено в базі"
        )
    
    new_advert = Advertisement(
        user_id=user.id,
        name=advert.name,
        description=advert.description,
        price=advert.price
    )

    session.add(new_advert)
    await session.commit()
    await session.refresh(new_advert)
    logger.info("advert_created", advert_id=new_advert.id, user_id=new_advert.user_id)
    return new_advert


@router.get("/{advert_id}", response_model=AdvertResponse)
async def get_advert_by_id(
    advert_id: int = Path(..., ge=1, description="ID оголошення повинен бути >= 1"),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Advertisement, User.tg_id)
        .join(User, Advertisement.user_id == User.id)
        .where(Advertisement.id == advert_id))
    result = await session.execute(query)
    row = result.first()

    if not row:
        logger.warning("advert_not_found", advert_id=advert_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    advert, tg_id = row
    advert_data = AdvertResponse.model_validate(advert)
    advert_data.tg_id = tg_id
    logger.info("advert_retrieved", advert_id=advert_data.id)
    return advert_data


@router.get("/", response_model=List[AdvertResponse])
async def get_advertisements(
    tg_id: Optional[int] = Query(None, description="Фільтр за ID користувача"),
    status: Optional[str] = Query(None, description="Фільтр за статусом (pending, active тощо)"),
    limit: int = Query(20, ge=1, le=100, description="Amount of elements on the page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    session: AsyncSession = Depends(get_async_session)
):
    query = (
        select(Advertisement)
        .options(selectinload(Advertisement.advertisement_photo))
    )

    if tg_id is not None:
        query = query.join(User).where(User.tg_id == tg_id)

    if status is not None:
        query = query.where(Advertisement.status == status)

    query = query.order_by(Advertisement.id.asc()).limit(limit).offset(offset)

    result = await session.execute(query)
    logger.info("adverts_retrieved", limit=limit, offset=offset)
    return result.scalars().all()


@router.patch("/{advert_id}", response_model=AdvertResponse)
async def update_advertisement(
    advert_in: AdvertUpdate,
    advert_id: int = Path(..., ge=1, description="ID оголошення повинен бути >= 1"),
    session: AsyncSession = Depends(get_async_session)
):
    query = select(Advertisement).where(Advertisement.id == advert_id)
    result = await session.execute(query)
    advert = result.scalar_one_or_none()

    if not advert:
        logger.warning("advert_not_found", advert_id=advert_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advertisement not found"
        )

    update_data = advert_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(advert, field, value)

    await session.commit()
    await session.refresh(advert)
    logger.info("advert_updated", advert_id=advert.id)
    return advert