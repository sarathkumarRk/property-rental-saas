from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    lease_id = Column(Integer, ForeignKey("leases.id"))
    amount = Column(Integer)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_status = Column(String)
    stripe_payment_intent_id = Column(String)