from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.database import get_async_session
from src.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from src.models.user import User, UserRole
from ..schemas.auth import UserCreate, UserResponse, TokenResponse, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.email == user_in.email)
    existing_user = (await session.execute(query)).scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=UserRole.USER,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
):
    query = select(User).where(User.email == form_data.username)
    user = (await session.execute(query)).scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(user.id, user.role.value)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(data: RefreshTokenRequest, session: AsyncSession = Depends(get_async_session)):
    payload = decode_token(data.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    result = await session.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User inactive or not found")

    access_token = create_access_token(user.id, user.role.value)
    new_refresh_token = create_refresh_token(user.id)

    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)