from __future__ import annotations
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .ads_photo import AdvertisementPhoto

class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False, default="other", server_default="other")
    status: Mapped[str] = mapped_column(String(20), default="pending", server_default="pending")
    wp_post_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    advertisement_photo: Mapped[List["AdvertisementPhoto"]] = relationship(back_populates="advertisement")

    user: Mapped['User'] = relationship(back_populates="advertisement")

    def __repr__(self):
        return f"Advertisement(id={self.id!r}, name={self.name!r}, description={self.description!r}, price={self.price!r})"
    