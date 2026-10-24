from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import structlog

from ..schemas.payment import PaymentCreate
from ..schemas.payment import PaymentCreate, PaymentType
from ..schemas.ad import AdvertisementStatus
from ..services.ads import get_ad_or_404
from src.models.payments import Payment

logger = structlog.get_logger()

async def create_payment_record(session: AsyncSession, **kwargs):
    payment = Payment(**kwargs)

    session.add(payment)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        logger.warning("payment_already_exists", telegram_charge_id=payment.telegram_charge_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Payment with this charge ID already exists"
        )
    await session.refresh(payment)
    return payment

async def validate_payment_service(session: AsyncSession, data: PaymentCreate):
    if data.service_type == PaymentType.VIP_SUBSCRIPTION.value:
        data.ad_id = None
        
    elif data.service_type == PaymentType.PRODUCT_PURCHASE.value:
        if not data.ad_id:
            raise HTTPException(status_code=400, detail="Ad ID is required for product purchase")
        
        ad = await get_ad_or_404(session, data.ad_id)
        if ad.status == AdvertisementStatus.SOLD.value:
            raise HTTPException(status_code=400, detail="This product is already sold")