from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, func
from sqlalchemy import BigInteger, String, DECIMAL, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from .base import Base

class PaymentType(str, Enum):
    VIP_SUBSCRIPTION = "vip_subscription"
    PRODUCT_PURCHASE = "product_purchase"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentServiceType(str, Enum):
    BOOST_TOP = "BOOST_TOP"
    VIP_HIGHLIGHT = "VIP_HIGHLIGHT"

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    ad_id: Mapped[int] = mapped_column(ForeignKey("advertisements.id", ondelete="SET NULL"), nullable=True)

    shop_order_number: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    amount: Mapped[DECIMAL] = mapped_column(DECIMAL, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="UAH")

    service_type: Mapped[PaymentType] = mapped_column(SQLEnum(PaymentType), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus), 
        default=PaymentStatus.PENDING, 
        server_default=PaymentStatus.PENDING.value,
        index=True
    )

    provider: Mapped[str] = mapped_column(String(32), default="portmone")
    external_payment_id: Mapped[Optional[str]] = mapped_column(String(128), unique=True, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        onupdate=func.now(), 
        nullable=True
    )