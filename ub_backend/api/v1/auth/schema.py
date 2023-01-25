from uuid import UUID

from pydantic import EmailStr, Field
from ub_backend.core.base.model import BaseModel
from ub_backend.core.config import app_config


class TokensResp(BaseModel):
    access_token: str = Field(
        ...,
        description=(
            f"Necessary to add header"
            f"'Authorization: {app_config.jwt.prefix} ...'"
        ),
    )
    refresh_token: str = Field(
        ...,
        description="Need to refresh ur pair",
    )


class LoginByEmailReq(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        example="Pa$$w0rd",
        title="Пароль",
    )


class RefreshTokenReq(BaseModel):
    token: str
    