from enum import Enum
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class PaymentType(str, Enum):
    VIP_SUBSCRIPTION = "VIP_SUBSCRIPTION"
    PRODUCT_PURCHASE = "PRODUCT_PURCHASE"

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class PaymentsBase(BaseModel):
    tg_id: int
    telegram_charge_id: str
    amount: Decimal = Field(..., gt=0, description="Сума оплати")
    currency: str = "UAH"
    service_type: PaymentType
    status: PaymentStatus = PaymentStatus.PENDING
    ad_id: Optional[int] = None
    provider: str = "portmone"

class PaymentCreate(PaymentsBase):
    provider_charge_id: Optional[str] = None

class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    provider_charge_id: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    user_id: int
    telegram_charge_id: str
    amount: Decimal = Field(..., gt=0, description="Сума оплати")
    currency: str = "UAH"
    service_type: PaymentType
    status: PaymentStatus = PaymentStatus.PENDING
    ad_id: Optional[int] = None
    provider: str = "portmone"
    provider_charge_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)