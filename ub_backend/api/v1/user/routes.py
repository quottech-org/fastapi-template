from uuid import UUID
from fastapi import APIRouter, Depends
from ub_backend.api.depends import get_user_storage_pg
from ub_backend.app.exception.common import BadRequestExcetion, NotFoundException
from ub_backend.core.security import generate_salt, get_password_hash
from ub_backend.database.postgres.sqlalchemy_models.user import DBUser
from ub_backend.database.postgres.storage.user_storage import PGUserStorage

from ub_backend.database.postgres.transactional import Transactional

from .schema import CreateUserReq, UserResp
router = APIRouter(prefix="/user")


@router.post(
    "/",
    tags=["user"],
    summary="Create user",
    response_model=UserResp,
)
@Transactional()
async def create_user(
    req: CreateUserReq,
    user_storage: PGUserStorage = Depends(get_user_storage_pg),
):
    user_exists = await user_storage.get_by_email(req.email)
    if user_exists:
        raise BadRequestExcetion(
            detail=("This email ") + req.email + (" already exists")
        )
    
    salt = generate_salt()
    db_user = await user_storage.insert_one(DBUser(**req.dict(exclude={"password"}), salt=salt,
            hashed_password=get_password_hash(f"{salt}{req.password}"),))
        
    return UserResp.from_orm(db_user)



@router.get(
    "/{user_id}",
    tags=["user"],
    summary="Get user by id",
    response_model=UserResp,
)
async def get_user_by_id(
    user_id: UUID,
    user_storage: PGUserStorage = Depends(get_user_storage_pg),
):
    user = await user_storage.get_by_id(user_id)
    if not user:
        raise NotFoundException(detail=f"User with id {user_id} does not exists")
    
    return UserResp.from_orm(user)
    