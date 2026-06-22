# backend/app/users/dms.py
from datetime import datetime
from pydantic import BaseModel


class UserDM(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
