from sqlalchemy import func, ForeignKey
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from .base import Base

class ProcessedNews(Base):
    __tablename__ = "processed_news"

    id: Mapped[int] = mapped_column(primary_key=True)

    source_id: Mapped[int] = mapped_column(ForeignKey("news_sources.id"))
    news_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(550))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"ProcessedNews(id={self.id!r}, source_url={self.source_id!r}, hash={self.news_hash!r})"