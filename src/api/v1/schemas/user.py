from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    tg_id: int
    name: str = Field(..., max_length=64)

class UserCreate(UserBase):
    pass 

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=64)
    status: Optional[UserRole] = None
    is_vip: Optional[bool] = None 
    vip_expires_at: Optional[datetime] = None

class UserResponse(UserBase):
    id: int
    status: str
    is_vip: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class VIPActivationRequest(BaseModel):
    days: int = Field(default=30, ge=1, description="Amount of days for VIP activation")