from pydantic import BaseModel, ConfigDict
from typing import Optional, List

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
    status: Optional[str] = None
    wp_post_id: Optional[int] = None

class AdvertResponse(AdvertisemenBase):
    id: int
    user_id: int
    status: str
    wp_post_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)