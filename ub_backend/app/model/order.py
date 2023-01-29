from decimal import Decimal
from typing import Optional
from uuid import UUID
from ub_backend.app.model.enum.order_type import OrderType
from ub_backend.app.model.mixins.timestamp import CreatedAtMixin
from ub_backend.app.model.mixins.uuid import UUIDMixin
from ub_backend.core.base.model import BaseModel


class OrderInfo(BaseModel):
    client_id: UUID
    comment: Optional[str]
    type: OrderType
    delivery_lon: Optional[float]
    delivery_lat: Optional[float]

    
class Order(UUIDMixin, OrderInfo, CreatedAtMixin):
    pass
