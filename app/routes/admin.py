from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.property import Property
from app.dependencies import admin_required

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):

    users = db.query(User).count()

    properties = db.query(Property).count()

    return {
        "users": users,
        "properties": properties
    }