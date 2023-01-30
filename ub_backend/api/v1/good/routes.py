from typing import List, Optional, Union
from uuid import UUID
from fastapi import APIRouter, Depends
from ub_backend.api.depends import get_good_storage_pg
from ub_backend.database.postgres.sqlalchemy_models.good import DBGood

from ub_backend.database.postgres.storage.good_storage import PGGoodStorage
from ub_backend.database.postgres.transactional import Transactional

from .schema import GoodResp, AddGoodReq, PatchGoodReq

router = APIRouter(prefix="/good")


# TODO: role Admin/Manager
@router.post(
    "/",
    tags=["good"],
    summary="Create good",
    response_model=GoodResp,
)
@Transactional()
async def create_good(
    req: AddGoodReq,
    good_storage: PGGoodStorage = Depends(get_good_storage_pg),
):
    db_good = await good_storage.insert_one(DBGood(**req.dict()))
    return GoodResp.from_orm(db_good)


# TODO: fields to search
@router.get(
    "/{good_id}",
    tags=["good"],
    summary="Get good/search",
    response_model=Union[List[GoodResp], GoodResp],
)
async def get_goods(
    good_id: Optional[UUID],
    good_storage: PGGoodStorage = Depends(get_good_storage_pg),
):
    if good_id:
        return GoodResp.from_orm(
            await good_storage.get_by_id(good_id)
        )
    else:
        result = []
        result.extend(GoodResp.from_orm(good) for good in await good_storage.get_many({}))
        return result


# TODO: role Admin/Manager
@router.put(
    "/{good_id}",
    tags=["good"],
    summary="Edit good fields",
    response_model=GoodResp,
)
@Transactional()
async def edit_good(
    good_id: UUID,
    req: PatchGoodReq,
    good_storage: PGGoodStorage = Depends(get_good_storage_pg),
):
    db_good = await good_storage.update_one(good_id, req.dict(exclude_none=True, exclude_unset=True))

    return GoodResp.from_orm(db_good)
