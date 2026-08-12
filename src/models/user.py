from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional
from enum import Enum

from sqlalchemy import func, Enum as SQLEnum
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, timezone

from .base import Base

if TYPE_CHECKING:
    from .advertisement import Advertisement

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(SQLEnum(UserRole, native_enum=False), default=UserRole.USER)
    is_vip: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    vip_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )

    advertisement: Mapped[List['Advertisement']] = relationship(back_populates="user")

    @property
    def has_active_vip(self) -> bool:
        if not self.vip_expires_at:
            return False
        return self.vip_expires_at > datetime.now(timezone.utc)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r})"