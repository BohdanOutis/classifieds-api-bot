from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    tg_id: int
    name: str = Field(..., max_length=64)

class UserCreate(UserBase):
    pass 

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=64)
    status: Optional[str] = Field(None, max_length=20)
    is_vip: Optional[bool] = None 
    vip_expires_at: Optional[datetime] = None

class UserResponse(UserBase):
    id: int
    status: str
    is_vip: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    