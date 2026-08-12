from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy import BigInteger, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from .base import Base

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"

class PaymentServiceType(str, Enum):
    BOOST_TOP = "BOOST_TOP"
    VIP_HIGHLIGHT = "VIP_HIGHLIGHT"

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    ad_id: Mapped[int] = mapped_column(ForeignKey("advertisements.id", ondelete="CASCADE"), nullable=False)

    shop_order_number: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    service_type: Mapped[PaymentServiceType] = mapped_column(String(50), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        String(20), 
        default=PaymentStatus.PENDING, 
        server_default=PaymentStatus.PENDING.value
    )
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        onupdate=func.now(), 
        nullable=True
    )