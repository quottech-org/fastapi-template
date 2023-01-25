from uuid import UUID

from ub_backend.app.model.mixins.price import PricesMixin
from ub_backend.app.model.mixins.uuid import UUIDMixin
from ub_backend.core.base.model import BaseModel


class GoodInfo(BaseModel):
    title: str
    description: str


class Good(UUIDMixin, GoodInfo, PricesMixin):
    # TODO: type + specs
    pass
    
