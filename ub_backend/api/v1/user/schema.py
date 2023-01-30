from datetime import datetime
from typing import Optional
from pydantic import EmailStr
from ub_backend.app.model import AllOptional
from ub_backend.app.model.good import Good
from ub_backend.app.model.user import User
from ub_backend.core.base.model import BaseModel


class CreateUserReq(BaseModel):
    password: str
    nick_name: str
    first_name: str
    last_name: str
    description: str
    birthday: datetime
    email: EmailStr
    phone_number: str
    avatar: Optional[str]  # TODO: http-url


class UserResp(User):
    pass
