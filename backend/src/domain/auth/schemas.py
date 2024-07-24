from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Other fields in schemas.BaseUser"""
    id: int | None = None
    username: str
    password: str
    email: EmailStr
    register_at: datetime | None = None
    last_login: datetime | None = None
    model_config = ConfigDict(from_attributes=True)



