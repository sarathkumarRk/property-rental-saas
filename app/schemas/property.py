from pydantic import BaseModel

class PropertyCreate(BaseModel):
    title: str
    description: str
    address: str
    rent_amount: int