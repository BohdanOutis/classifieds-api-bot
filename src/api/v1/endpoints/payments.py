from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
import structlog

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from ..schemas.payment import PaymentResponse, PaymentCreate
from ..services.payment_service import create_payment_record, validate_payment_service
from ..services.users import verify_user_exists

logger = structlog.get_logger()

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PaymentResponse)
async def add_payment(
    data: PaymentCreate,
    session: AsyncSession = Depends(get_async_session)
):
    user = await verify_user_exists(session, data.tg_id)

    await validate_payment_service(session, data)

    payload = data.model_dump(exclude={"tg_id"})
    payload["user_id"] = user.id
            
    payment = await create_payment_record(session, **payload)
    logger.info("payment_created", service_type=payment.service_type, payment_id=payment.id, user_id=payment.user_id, ad_id=payment.ad_id)
    return payment