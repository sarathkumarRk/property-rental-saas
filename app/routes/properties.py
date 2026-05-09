from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

import os

from app.database import get_db
from app.schemas.property import PropertyCreate

from app.models.property import (
    Property,
    PropertyImage
)

from app.auth import get_current_user

router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


# CREATE PROPERTY (OWNER ONLY)
@router.post("/")
def create_property(
    data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can create properties"
        )

    property_obj = Property(
        owner_id=current_user.id,
        title=data.title,
        description=data.description,
        address=data.address,
        rent_amount=data.rent_amount
    )

    db.add(property_obj)
    db.commit()
    db.refresh(property_obj)

    return property_obj


# GET ALL PROPERTIES
@router.get("/")
def get_properties(
    db: Session = Depends(get_db)
):

    properties = db.query(Property).all()

    result = []

    for property_obj in properties:

        first_image = db.query(PropertyImage).filter(
            PropertyImage.property_id == property_obj.id
        ).first()

        result.append({
            "id": property_obj.id,
            "owner_id": property_obj.owner_id,
            "title": property_obj.title,
            "description": property_obj.description,
            "address": property_obj.address,
            "rent_amount": property_obj.rent_amount,
            "is_available": property_obj.is_available,
            "image_url": (
                f"http://127.0.0.1:8000/{first_image.image_url}"
                if first_image else None
            )
        })

    return result


# GET SINGLE PROPERTY
@router.get("/{property_id}")
def get_single_property(
    property_id: int,
    db: Session = Depends(get_db)
):

    property_obj = db.query(Property).filter(
        Property.id == property_id
    ).first()

    if not property_obj:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    first_image = db.query(PropertyImage).filter(
        PropertyImage.property_id == property_obj.id
    ).first()

    return {
        "id": property_obj.id,
        "owner_id": property_obj.owner_id,
        "title": property_obj.title,
        "description": property_obj.description,
        "address": property_obj.address,
        "rent_amount": property_obj.rent_amount,
        "is_available": property_obj.is_available,
        "image_url": (
            f"http://127.0.0.1:8000/{first_image.image_url}"
            if first_image else None
        )
    }


# UPDATE PROPERTY (OWNER ONLY)
@router.put("/{property_id}")
def update_property(
    property_id: int,
    data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can update properties"
        )

    property_obj = db.query(Property).filter(
        Property.id == property_id
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

    property_obj.title = data.title
    property_obj.description = data.description
    property_obj.address = data.address
    property_obj.rent_amount = data.rent_amount

    db.commit()

    return {
        "message": "Property updated"
    }


# DELETE PROPERTY (OWNER ONLY)
@router.delete("/{property_id}")
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can delete properties"
        )

    property_obj = db.query(Property).filter(
        Property.id == property_id
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

    db.delete(property_obj)
    db.commit()

    return {
        "message": "Property deleted"
    }


# UPLOAD PROPERTY IMAGE (OWNER ONLY)
@router.post("/{property_id}/upload")
def upload_image(
    property_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    if current_user.role != "owner":
        raise HTTPException(
            status_code=403,
            detail="Only owners can upload images"
        )

    property_obj = db.query(Property).filter(
        Property.id == property_id
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

    os.makedirs("uploads", exist_ok=True)

    filename = f"uploads/{file.filename}"

    with open(filename, "wb") as buffer:
        buffer.write(file.file.read())

    image = PropertyImage(
        property_id=property_id,
        image_url=filename
    )

    db.add(image)
    db.commit()

    return {
        "message": "Image uploaded",
        "image_url": f"http://127.0.0.1:8000/{filename}"
    }