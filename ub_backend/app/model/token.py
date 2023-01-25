from datetime import datetime, timedelta
from uuid import uuid4

from pydantic import EmailStr, Field
from ub_backend.core.base.model import BaseModel
from ub_backend.core.config import app_config


class BaseToken(BaseModel):
    user_id: str
    email: EmailStr


class AccessToken(BaseToken):
    exp: datetime = Field(
        default_factory=lambda: (
            datetime.utcnow() + timedelta(minutes=app_config.jwt.access_expiration_time)
        )
    )

    def is_expired(self) -> bool:
        return self.exp < datetime.now(self.exp.tzinfo)


class RefreshToken(BaseToken):
    token: str = Field(default_factory=lambda: str(uuid4()))
