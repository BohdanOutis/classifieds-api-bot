from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import structlog

from src.core.database import get_async_session
from ..schemas.user import UserResponse, UserCreate, UserUpdate, VIPActivationRequest
from src.models.user import User

from datetime import datetime, timezone, timedelta

logger = structlog.get_logger()

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_in: UserCreate, 
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.tg_id == user_in.tg_id)
    result = await session.execute(query)
    db_user = result.scalar_one_or_none()

    if db_user:
        logger.info("user_already_exists", user_id=db_user.id)
        return db_user

    new_user = User(
        tg_id=user_in.tg_id, 
        name=user_in.name,
    )
    session.add(new_user)
    await session.commit()
    logger.info("user_created", user_id=new_user.id, tg_id=new_user.tg_id)
    await session.refresh(new_user)
    
    return new_user

@router.patch("/{tg_id}/activate-vip")
async def activate_vip(
    tg_id: int = Path(..., description="User telegram id"),
    payload: VIPActivationRequest = None,
    session: AsyncSession = Depends(get_async_session)
):
    days = payload.days if payload else 30
    
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("user_not_found", tg_id=tg_id)
        raise HTTPException(
            status_code=404,
            detail="Користувача не знайдено"
        )

    now = datetime.now(timezone.utc)

    if user.vip_expires_at and user.vip_expires_at > now:
        user.vip_expires_at += timedelta(days=days)
    else:
        user.vip_expires_at = now + timedelta(days=days)

    user.is_vip = True
    await session.commit()

    logger.info("vip_activated_successfully", tg_id=tg_id, expires_at=str(user.vip_expires_at))

    return {
        "status": "success",
        "vip_expires_at": user.vip_expires_at,
        "is_vip": True
    }


@router.get("/by-username/{username}")
async def get_user_by_username(
    username: str, 
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(func.lower(User.name) == username.lower())
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("user_not_found", name=username.lower())
        raise HTTPException(
            status_code=404, 
            detail="Користувача не знайдено"
        )
    logger.info("user_found", name=username)
    return user

@router.get("/{tg_id}", response_model=UserResponse)
async def get_user(
    tg_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.tg_id==tg_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("user_not_found", tg_id=tg_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    logger.info("user_retrieved", user_id=user.id, tg_id=user.tg_id)
    return user


@router.patch("/{tg_id}", response_model=UserResponse)
async def update_user_data(
    tg_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> User:
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        logger.warning("user_not_found", tg_id=tg_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    logger.info("user_updated", user_id=user.id, tg_id=user.tg_id)
    return user