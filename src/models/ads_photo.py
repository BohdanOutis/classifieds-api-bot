from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class AdvertisementPhoto(Base):
    __tablename__ = "advertisement_photo"

    id: Mapped[int] = mapped_column(primary_key=True)
    advert_id: Mapped[int] = mapped_column(ForeignKey("advertisements.id", ondelete="CASCADE"), nullable=False)
    file_id: Mapped[str] = mapped_column(String(255), nullable=False)

    advertisement: Mapped['Advertisement'] = relationship(back_populates="advertisement_photo")