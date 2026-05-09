from pydantic import BaseModel
from datetime import date

class LeaseRequestSchema(BaseModel):
    property_id: int

class LeaseApproveSchema(BaseModel):
    request_id: int
    start_date: date
    end_date: date