from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)

from sqlalchemy.orm import Session

import stripe

from app.database import get_db
from app.models.payment import Payment
from app.models.lease import Lease
from app.models.user import User

from app.auth import get_current_user
from app.utils.stripe import create_payment_intent
from app.utils.email import send_email

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/webhook",
    include_in_schema=False
)
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    payload = await request.body()

    sig_header = request.headers.get(
        "stripe-signature"
    )

    endpoint_secret = "whsec_6b5352d5414f5993c5a5a80d3dd29f1d06df9096193b59534a68a73498f191e4"

    try:

        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )

    except Exception as e:

        print("WEBHOOK ERROR:", str(e))

        raise HTTPException(
            status_code=400,
            detail="Webhook verification failed"
        )

    if event["type"] == "payment_intent.succeeded":

        payment_intent = event["data"]["object"]

        stripe_payment_intent_id = payment_intent["id"]

        payment = db.query(Payment).filter(
            Payment.stripe_payment_intent_id
            == stripe_payment_intent_id
        ).first()

        if payment:

            payment.payment_status = "paid"

            db.commit()

            lease = db.query(Lease).filter(
                Lease.id == payment.lease_id
            ).first()

            if lease:

                tenant = db.query(User).filter(
                    User.id == lease.tenant_id
                ).first()

                if tenant:

                    send_email(
                        to_email=tenant.email,
                        subject="Rent Payment Successful",
                        body="""
Your rent payment was successful.

Thank you for your payment.
"""
                    )

            print("Payment success")

    return {
        "status": "success"
    }


@router.post("/{lease_id}")
def pay_rent(
    lease_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    lease = db.query(Lease).filter(
        Lease.id == lease_id
    ).first()

    if not lease:
        raise HTTPException(
            status_code=404,
            detail="Lease not found"
        )

    if lease.tenant_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not your lease"
        )

    if lease.status != "active":
        raise HTTPException(
            status_code=400,
            detail="Lease not active"
        )

    intent = create_payment_intent(
        lease.monthly_rent
    )

    payment = Payment(
        lease_id=lease.id,
        amount=lease.monthly_rent,
        payment_status="pending",
        stripe_payment_intent_id=intent.id
    )

    db.add(payment)
    db.commit()

    return {
        "message": "Payment initiated",
        "client_secret": intent.client_secret
    }


@router.get("/")
def payment_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    payments = db.query(Payment).join(
        Lease,
        Lease.id == Payment.lease_id
    ).filter(
        Lease.tenant_id == current_user.id
    ).all()

    return payments