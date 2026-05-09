from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.property import Property
from app.models.lease import Lease
from app.models.payment import Payment
from app.models.maintenance import MaintenanceRequest

from app.auth import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/owner")
def owner_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    total_properties = db.query(Property).filter(
        Property.owner_id == current_user.id
    ).count()

    owner_property_ids = db.query(Property.id).filter(
        Property.owner_id == current_user.id
    ).subquery()

    active_leases = db.query(Lease).filter(
        Lease.property_id.in_(owner_property_ids),
        Lease.status == "active"
    ).count()

    monthly_revenue = db.query(
        func.sum(Payment.amount)
    ).join(
        Lease,
        Lease.id == Payment.lease_id
    ).filter(
        Lease.property_id.in_(owner_property_ids),
        Payment.payment_status == "paid"
    ).scalar() or 0

    open_maintenance = db.query(
        MaintenanceRequest
    ).filter(
        MaintenanceRequest.property_id.in_(owner_property_ids),
        MaintenanceRequest.status.in_(["open", "pending"])
    ).count()

    return {
        "total_properties": total_properties,
        "active_leases": active_leases,
        "monthly_revenue": monthly_revenue,
        "open_maintenance": open_maintenance
    }


@router.get("/tenant")
def tenant_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    active_lease = db.query(Lease).filter(
        Lease.tenant_id == current_user.id,
        Lease.status == "active"
    ).count()

    payment_count = db.query(Payment).join(
        Lease,
        Lease.id == Payment.lease_id
    ).filter(
        Lease.tenant_id == current_user.id,
        Payment.payment_status == "paid"
    ).count()

    maintenance_count = db.query(
        MaintenanceRequest
    ).filter(
        MaintenanceRequest.tenant_id == current_user.id
    ).count()

    return {
        "active_lease": active_lease,
        "payment_count": payment_count,
        "maintenance_count": maintenance_count
    }