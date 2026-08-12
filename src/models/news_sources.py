from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class NewsSources(Base):
    __tablename__ = "news_sources"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    def __repr__(self):
        return f"NewsSources(id={self.id!r}, url={self.url!r}, is_active={self.is_active!r}, name={self.name!r})"