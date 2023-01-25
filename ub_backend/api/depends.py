from fastapi import Depends, Header
from ub_backend.app.exception.common import UnauthorizedException

from ub_backend.app.model.token import AccessToken
from ub_backend.app.service.jwt_service import jwt_service
from ub_backend.database.postgres.db import get_db
from ub_backend.database.postgres.storage.good_storage import PGGoodStorage
from ub_backend.database.postgres.storage.order_storage import PGOrderStorage
from ub_backend.database.postgres.storage.token_storage import PGTokenStorage
from ub_backend.database.postgres.storage.user_storage import PGUserStorage


async def access_token(authorization=Header(...)) -> AccessToken:
    token = jwt_service.decode_access_token(authorization)
    if token.is_expired():
        raise UnauthorizedException(detail="Token is expired")
    return token


async def get_user_storage_pg(db=Depends(get_db)) -> PGUserStorage:
    return PGUserStorage(db=db)


async def get_token_storage_pg(db=Depends(get_db)) -> PGTokenStorage:
    return PGTokenStorage(db=db)
    

async def get_good_storage_pg(db=Depends(get_db)) -> PGGoodStorage:
    return PGGoodStorage(db=db)


async def get_order_storage_pg(db=Depends(get_db)) -> PGOrderStorage:
    return PGOrderStorage(db=db)
