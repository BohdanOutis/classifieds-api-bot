from enum import Enum
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class PaymentType(str, Enum):
    VIP_SUBSCRIPTION = "vip_subscription"
    PRODUCT_PURCHASE = "product_purchase"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentsBase(BaseModel):
    user_id: int
    shop_order_number: str
    amount: Decimal = Field(..., gt=0, description="Сума оплати")
    currency: str = "UAH"
    service_type: PaymentType
    status: PaymentStatus = PaymentStatus.PENDING
    ad_id: Optional[int] = None
    provider: str = "portmone"

class PaymentCreate(PaymentsBase):
    external_payment_id: Optional[str] = None

class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    external_payment_id: Optional[str] = None

class PaymentResponse(PaymentsBase):
    id: int
    external_payment_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)