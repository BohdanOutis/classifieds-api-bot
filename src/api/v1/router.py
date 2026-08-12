from fastapi import APIRouter
from src.api.v1.endpoints import ads, payments, users, photo, news, processed_news, stats

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(ads.router, prefix="/ads", tags=["Ads"])
router.include_router(payments.router, prefix="/payments", tags=["Payments"])
router.include_router(photo.router, prefix="/ads_photos", tags=["Advertisement photos"]) 
router.include_router(news.router, prefix="/news", tags=["News"])
router.include_router(processed_news.router, prefix="/processed_news", tags=["Processed news"])
router.include_router(stats.router, prefix="/stats", tags=["Statistics"])