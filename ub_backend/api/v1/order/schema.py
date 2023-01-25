from typing import List
from uuid import UUID
from ub_backend.app.model.full_order import FullOrder

from ub_backend.app.model.good import Good
from ub_backend.app.model.order import OrderInfo
from ub_backend.core.base.model import BaseModel


class AddOrderReq(BaseModel):
    order: OrderInfo
    cart: List[UUID]


class FullOrderResp(FullOrder):
    pass
