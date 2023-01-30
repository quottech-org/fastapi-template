from decimal import Decimal
from typing import Optional

from ub_backend.core.base.model import BaseModel


class PricesMixin(BaseModel):
    price_usd: Decimal
    price_gel: Optional[Decimal]
    price_rub: Optional[Decimal]
    price_eur: Optional[Decimal]
