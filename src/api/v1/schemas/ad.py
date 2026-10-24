from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from .photo import AdvertPhotoResponse

class AdvertisementStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    SOLD = "SOLD"

class AdvertisemenBase(BaseModel):
    name: str
    description: str
    price: int
    category: str = "other"

class AdvertCreate(AdvertisemenBase):
    tg_id: int

class AdvertUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category: Optional[str] = None
    status: Optional[AdvertisementStatus] = None
    wp_post_id: Optional[int] = None

class AdvertResponse(AdvertisemenBase):
    id: int
    user_id: int
    tg_id: Optional[int] = None
    status: AdvertisementStatus
    wp_post_id: Optional[int] = None
    photos: List[AdvertPhotoResponse] = Field(default = [], alias="advertisement_photo")

    model_config = ConfigDict(from_attributes=True)