from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    name: str


class UserDM(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
