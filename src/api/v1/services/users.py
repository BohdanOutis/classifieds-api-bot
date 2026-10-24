from fastapi import HTTPException, status
from datetime import datetime, timezone
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from ....models.user import User
import structlog

logger = structlog.get_logger()

async def expire_vip_statuses(session: AsyncSession) -> int:
    now = datetime.now(timezone.utc)
    stmt = (
        update(User)
        .where(
            User.is_vip == True,
            User.vip_expires_at <= now
        )
        .values(is_vip=False)
    )
    result = await session.execute(stmt)
    await session.commit()
    count = result.rowcount
    logger.info("vip_statuses_expired_successfully", users_vip_count=count)
    return count

async def verify_user_exists(session: AsyncSession, tg_id: int):
    stmt = select(User).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        logger.warning("user_not_found_for_payment", tg_id=tg_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found for payment"
        )
    return user