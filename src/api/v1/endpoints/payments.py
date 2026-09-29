from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.models.payments import Payment
from ..schemas.payment import PaymentResponse, PaymentCreate

router = APIRouter()

@router.post("/")
async def add_payment(
    data: PaymentCreate,
    session: AsyncSession = Depends(get_async_session)
):
    payment = Payment(
        PaymentCreate
    )

@router.get("/")
async def add_payment(
    data: PaymentCreate,
    session: AsyncSession = Depends(get_async_session)
):
    pass