from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session
from src.models.ads_photo import AdvertisementPhoto
from ..schemas.photo import AdvertPhotoResponse

router = APIRouter()