from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.maintenance import MaintenanceRequest
from app.models.lease import Lease
from app.models.user import User

from app.auth import get_current_user

from app.dependencies import owner_required

from app.utils.email import send_email

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.post("/")
def create_issue(
    property_id: int,
    issue: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    lease = db.query(Lease).filter(
        Lease.property_id == property_id,
        Lease.tenant_id == current_user.id,
        Lease.status == "active"
    ).first()

    if not lease:

        raise HTTPException(
            status_code=403,
            detail="Not your property"
        )

    req = MaintenanceRequest(
        property_id=property_id,
        tenant_id=current_user.id,
        issue=issue,
        status="open"
    )

    db.add(req)

    db.commit()

    return {
        "message": "Created"
    }


@router.put("/{request_id}")
def update_status(
    request_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user = Depends(owner_required)
):

    req = db.query(MaintenanceRequest).filter(
        MaintenanceRequest.id == request_id
    ).first()

    if not req:

        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    req.status = status

    db.commit()

    tenant = db.query(User).filter(
        User.id == req.tenant_id
    ).first()

    send_email(
        to_email=tenant.email,
        subject="Maintenance Status Updated",
        body=f"""
Your maintenance request status has been updated.

Issue:
{req.issue}

New Status:
{status}
"""
    )

    return {
        "message": "Updated"
    }