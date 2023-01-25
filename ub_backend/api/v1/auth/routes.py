from uuid import UUID
from fastapi import APIRouter, Depends
from ub_backend.api.depends import get_token_storage_pg, get_user_storage_pg
from ub_backend.api.v1.auth.schema import LoginByEmailReq, RefreshTokenReq, TokensResp
from ub_backend.app.exception.common import UnauthorizedException
from ub_backend.app.service.jwt_service import jwt_service
from ub_backend.database.postgres.storage.token_storage import PGTokenStorage
from ub_backend.database.postgres.storage.user_storage import PGUserStorage

from ub_backend.database.postgres.transactional import Transactional


router = APIRouter(prefix="/auth")


@router.post(
    "/login/email",
    tags=["auth"],
    summary="Авторизация через email",
    description="",
    response_model=TokensResp,
)
@Transactional()
async def login_by_email(
    req: LoginByEmailReq,
    user_storage: PGUserStorage = Depends(get_user_storage_pg),
    token_storage: PGTokenStorage = Depends(get_token_storage_pg),
):
    user = await user_storage.get_by_email_and_password(req.email, req.password)
    access_token, refresh_token = await token_storage.gen_new_tokens(user)
    return TokensResp(
        access_token=jwt_service.encode_token(access_token),
        refresh_token=jwt_service.encode_token(refresh_token),
        user_id=user.id,
    )


@router.post(
    "/refresh",
    tags=["auth"],
    summary="Обновить токен",
    description="Вернёт новую пару access & refresh токенов, если refresh валидный",
    response_model=TokensResp,
)
@Transactional()
async def refresh(
    req: RefreshTokenReq,
    token_storage: PGTokenStorage = Depends(get_token_storage_pg),
    user_storage: PGUserStorage = Depends(get_user_storage_pg),
):
    refresh_token = jwt_service.decode_refresh_token(req.token)
    access_token, new_refresh_token = await token_storage.refresh_tokens(refresh_token)
    user = await user_storage.get_by_id(UUID(access_token.user_id))
    if user is None:
        raise UnauthorizedException(detail="Invalid auth token", error="invalid_token")
    return TokensResp(
        access_token=jwt_service.encode_token(access_token),
        refresh_token=jwt_service.encode_token(new_refresh_token),
        user_id=user.id,
    )
