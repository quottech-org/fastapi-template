from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from ub_backend.core.base.model import BaseModel


class UserInfo(BaseModel):
    nick_name: str
    first_name: str
    last_name: str
    description: str
    birthday: datetime
    email: EmailStr
    phone_number: str
    avatar: Optional[str]  # TODO: http-url


class User(UserInfo):
    id: UUID
    
    