from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends

from ub_backend.api.depends import get_good_storage_pg, get_order_storage_pg, get_user_storage_pg, access_token
from ub_backend.api.v1.order.schema import FullOrderResp, AddOrderReq
from ub_backend.app.model.good import Good
from ub_backend.app.model.order import Order
from ub_backend.app.model.token import AccessToken
from ub_backend.app.model.user import User
from ub_backend.database.postgres.sqlalchemy_models.order import DBOrder
from ub_backend.database.postgres.storage.good_storage import PGGoodStorage
from ub_backend.database.postgres.storage.order_storage import PGOrderStorage
from ub_backend.database.postgres.storage.user_storage import PGUserStorage
from ub_backend.database.postgres.transactional import Transactional

from ub_backend.app.service.telegram_service import telegram_service

router = APIRouter(prefix="/order")


@router.post(
    "/",
    tags=["order"],
    summary="Create order",
    description="",
    response_model=FullOrderResp,
)
@Transactional()
async def add_order(
    req: AddOrderReq,
    user_storage: PGUserStorage = Depends(get_user_storage_pg),
    order_storage: PGOrderStorage = Depends(get_order_storage_pg),
    good_storage: PGGoodStorage = Depends(get_good_storage_pg),
    token: AccessToken = Depends(access_token),
):
    user_db = await user_storage.get_by_id(UUID(token.user_id))
    
    order_db = await order_storage.create_order(DBOrder(**req.order.dict()), req.cart)
    good_db_list = await good_storage.get_list_by_ids(req.cart)


    full_order = FullOrderResp(
        order=Order.from_orm(order_db),
        client=User.from_orm(user_db),
        goods=[Good.from_orm(i) for i in good_db_list],
    )
    
    await telegram_service.send_order_alert(full_order=full_order)

    return full_order
