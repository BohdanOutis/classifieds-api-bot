from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class AdvertPhotoBase(BaseModel):
    advert_id: int

class AdvertPhotoCreate(AdvertPhotoBase):
    file_ids: List[str]

class AdvertPhotoResponse(AdvertPhotoBase):
    id: int
    file_id: str
    model_config = ConfigDict(from_attributes=True)