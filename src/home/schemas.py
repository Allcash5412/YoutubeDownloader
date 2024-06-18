from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserProfileInfo(BaseModel):
    username: str
    email: EmailStr
    register_at: datetime | None
    last_login: datetime | None
    model_config = ConfigDict(from_attributes=True)