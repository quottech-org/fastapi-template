

from decimal import Decimal
from typing import List, Optional

from pydantic import validator

from ub_backend.app.model.good import Good
from ub_backend.app.model.order import Order
from ub_backend.app.model.user import User
from ub_backend.core.base.model import BaseModel


class FullOrder(BaseModel):
    order: Order
    client: User
    goods: List[Good]
    total_price_usd: Optional[Decimal]

    @validator("total_price_usd", pre=True, always=True)
    def total_price_count(cls, v, values, **kwargs):
        val: Decimal = Decimal("0")
        prices: List[Decimal] = [i.price_usd for i in values.get("goods")] 
        for price in prices:
            val += price
        
        return val
        