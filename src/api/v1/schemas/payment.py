from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"

class PaymentServiceType(str, Enum):
    BOOST_TOP = "BOOST_TOP"
    VIP_HIGHLIGHT = "VIP_HIGHLIGHT"

class PaymentsBase(BaseModel):
    user_id: int
    ad_id: int
    shop_order_number: str
    amount: float
    service_type: PaymentServiceType
    status: PaymentStatus = PaymentStatus.PENDING

class PaymentCreate(PaymentsBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None

class PaymentResponse(PaymentsBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)