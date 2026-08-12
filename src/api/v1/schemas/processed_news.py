from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class ProcessedNewsBase(BaseModel):
    source_id: int
    news_hash: str = Field(..., max_length=64, description="SHA-256 хеш новини")
    title: str = Field(..., max_length=255)
    link: str = Field(..., max_length=550)

class ProcessedNewsCreate(ProcessedNewsBase):
    pass

class ProcessedNewsUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    link: Optional[str] = Field(None, max_length=550)

class ProcessedNewsResponse(ProcessedNewsBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)