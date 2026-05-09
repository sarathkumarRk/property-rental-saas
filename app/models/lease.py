from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DateTime
)

from datetime import datetime

from app.database import Base


class LeaseRequest(Base):

    __tablename__ = "lease_requests"

    id = Column(Integer, primary_key=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id")
    )

    tenant_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    status = Column(
        String,
        default="pending"
    )

    requested_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Lease(Base):

    __tablename__ = "leases"

    id = Column(Integer, primary_key=True)

    property_id = Column(
        Integer,
        ForeignKey("properties.id")
    )

    tenant_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    start_date = Column(Date)

    end_date = Column(Date)

    monthly_rent = Column(Integer)

    status = Column(
        String,
        default="active"
    )