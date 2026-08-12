from datetime import datetime, timezone
from sqlalchemy import update
from ..core.database import AsyncSession as AsyncSessionLocal
from ..models.user import User


async def check_expired_vip_statuses():
    async with AsyncSessionLocal() as session:
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

        updated_count = result.rowcount
        if updated_count > 0:
            print(f"⏰ [Cron] Скинуто VIP-статус для {updated_count} користувачів.")