from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.database import get_db
from app.models.lease import LeaseRequest, Lease
from app.models.property import Property
from app.models.user import User

from app.schemas.lease import (
    LeaseRequestSchema,
    LeaseApproveSchema
)

from app.auth import get_current_user
from app.utils.email import send_email

router = APIRouter(
    prefix="/leases",
    tags=["Leases"]
)


# GET LEASE REQUESTS (OWNER ONLY)
@router.get("/requests")
def get_lease_requests(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can view lease requests"
        )

    requests = db.query(LeaseRequest).join(
        Property,
        Property.id == LeaseRequest.property_id
    ).filter(
        Property.owner_id == current_user.id
    ).all()

    result = []

    for req in requests:

        tenant = db.query(User).filter(
            User.id == req.tenant_id
        ).first()

        property_obj = db.query(Property).filter(
            Property.id == req.property_id
        ).first()

        result.append({
            "id": req.id,
            "property_title": property_obj.title,
            "tenant_email": tenant.email,
            "status": req.status
        })

    return result


# TENANT REQUEST LEASE
@router.post("/request")
def request_lease(
    data: LeaseRequestSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "tenant":
        raise HTTPException(
            status_code=403,
            detail="Only tenants can request leases"
        )

    property_obj = db.query(Property).filter(
        Property.id == data.property_id
    ).first()

    if not property_obj:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    if not property_obj.is_available:
        raise HTTPException(
            status_code=400,
            detail="Property unavailable"
        )

    existing = db.query(Lease).filter(
        Lease.property_id == data.property_id,
        Lease.status == "active"
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already leased"
        )

    req = LeaseRequest(
        property_id=data.property_id,
        tenant_id=current_user.id
    )

    db.add(req)
    db.commit()

    return {
        "message": "Lease requested"
    }


# OWNER APPROVE LEASE
@router.post("/approve")
def approve_lease(
    data: LeaseApproveSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can approve leases"
        )

    req = db.query(LeaseRequest).filter(
        LeaseRequest.id == data.request_id
    ).first()

    if not req:
        raise HTTPException(
            status_code=404,
            detail="Lease request not found"
        )

    property_obj = db.query(Property).filter(
        Property.id == req.property_id
    ).first()

    if not property_obj:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    if property_obj.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not your property"
        )

    if data.start_date >= data.end_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    overlap = db.query(Lease).filter(
        Lease.property_id == req.property_id,
        Lease.status == "active",
        or_(
            and_(
                Lease.start_date <= data.start_date,
                Lease.end_date >= data.start_date
            ),
            and_(
                Lease.start_date <= data.end_date,
                Lease.end_date >= data.end_date
            )
        )
    ).first()

    if overlap:
        raise HTTPException(
            status_code=400,
            detail="Lease dates overlap"
        )

    lease = Lease(
        property_id=req.property_id,
        tenant_id=req.tenant_id,
        start_date=data.start_date,
        end_date=data.end_date,
        monthly_rent=property_obj.rent_amount,
        status="active"
    )

    property_obj.is_available = False
    req.status = "approved"

    db.add(lease)
    db.commit()

    tenant = db.query(User).filter(
        User.id == req.tenant_id
    ).first()

    if tenant:
        send_email(
            tenant.email,
            "Lease Approved",
            "Your lease request has been approved."
        )

    return {
        "message": "Lease approved"
    }


# OWNER REJECT REQUEST
@router.put("/reject/{request_id}")
def reject_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can reject leases"
        )

    req = db.query(LeaseRequest).filter(
        LeaseRequest.id == request_id
    ).first()

    if not req:
        raise HTTPException(
            status_code=404,
            detail="Lease request not found"
        )

    req.status = "rejected"
    db.commit()

    tenant = db.query(User).filter(
        User.id == req.tenant_id
    ).first()

    if tenant:
        send_email(
            tenant.email,
            "Lease Rejected",
            "Your lease request has been rejected."
        )

    return {
        "message": "Lease rejected"
    }


# OWNER TERMINATE LEASE
@router.put("/terminate/{lease_id}")
def terminate_lease(
    lease_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can terminate leases"
        )

    lease = db.query(Lease).filter(
        Lease.id == lease_id
    ).first()

    if not lease:
        raise HTTPException(
            status_code=404,
            detail="Lease not found"
        )

    lease.status = "terminated"

    property_obj = db.query(Property).filter(
        Property.id == lease.property_id
    ).first()

    if property_obj:
        property_obj.is_available = True

    db.commit()

    return {
        "message": "Lease terminated"
    }


# UPDATE LEASE
@router.put("/{lease_id}")
def update_lease(
    lease_id: int,
    db: Session = Depends(get_db)
):

    lease = db.query(Lease).filter(
        Lease.id == lease_id
    ).first()

    if not lease:
        raise HTTPException(
            status_code=404,
            detail="Lease not found"
        )

    if lease.status == "active":
        raise HTTPException(
            status_code=400,
            detail="Cannot edit active lease"
        )

    return {
        "message": "Lease editable"
    }