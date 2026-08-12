from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from ....core.database import get_async_session
from ....models.user import User
from ....models.advertisement import Advertisement
# from ....models.user import Payment

router = APIRouter()

@router.get("/")
async def get_bot_stats(session: AsyncSession = Depends(get_async_session)):
    users_query = select(func.count(User.id))
    total_users = (await session.execute(users_query)).scalar() or 0

    ads_query = select(func.count(Advertisement.id)).where(
        Advertisement.status == "approved"
    )
    total_ads = (await session.execute(ads_query)).scalar() or 0

    # # 3. Загальна сума зароблених грошей (наприклад, з таблиці платежів або суми оголошень)
    # revenue_query = select(func.sum(Payment.amount)).where(
    #     Payment.status == "success"
    # )
    # total_revenue = (await session.execute(revenue_query)).scalar() or 0
    total_revenue = 0

    return {
        "total_users": total_users,
        "total_ads": total_ads,
        "total_revenue": total_revenue,
    }