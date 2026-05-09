from pydantic import BaseModel
from datetime import datetime


class MaintenanceCreate(BaseModel):
    property_id: int
    issue: str


class MaintenanceUpdate(BaseModel):
    status: str


class MaintenanceResponse(BaseModel):
    id: int
    property_id: int
    tenant_id: int
    issue: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True