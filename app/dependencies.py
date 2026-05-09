from fastapi import Depends, HTTPException
from app.auth import get_current_user

def owner_required(current_user = Depends(get_current_user)):
    if current_user.role != "owner":
        raise HTTPException(status_code=403, detail="Owner only")

    return current_user

def tenant_required(current_user = Depends(get_current_user)):
    if current_user.role != "tenant":
        raise HTTPException(status_code=403, detail="Tenant only")

    return current_user

def admin_required(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return current_user