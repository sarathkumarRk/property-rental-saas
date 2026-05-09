from pydantic import BaseModel
from datetime import datetime


class PaymentCreate(BaseModel):
    lease_id: int
    amount: int


class PaymentResponse(BaseModel):
    id: int
    lease_id: int
    amount: int
    payment_date: datetime
    payment_status: str
    stripe_payment_intent_id: str

    class Config:
        from_attributes = True