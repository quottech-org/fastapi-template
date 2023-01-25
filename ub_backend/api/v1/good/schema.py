from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from ub_backend.app.model import AllOptional
from ub_backend.app.model.good import Good


class GoodResp(Good):
    pass


class AddGoodReq(BaseModel):
    title: str
    description: str
    # TODO: type + specs
    price_usd: Decimal
    price_gel: Optional[Decimal]
    price_rub: Optional[Decimal]
    price_eur: Optional[Decimal]


class PatchGoodReq(AddGoodReq, metaclass=AllOptional):
    pass
