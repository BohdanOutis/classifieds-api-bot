from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

class NewsSourceBase(BaseModel):
    name: str = Field(..., max_length=100)
    url: str = Field(..., max_length=255)
    is_active: bool = True

class NewsSourceCreate(NewsSourceBase):
    pass

class NewsSourceUpdate(BaseModel):
    name: Optional[str] = Field(..., max_length=100)
    url: Optional[str] = Field(..., max_length=255)
    is_active: Optional[bool] = None

class NewsSourceRespose(NewsSourceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)    