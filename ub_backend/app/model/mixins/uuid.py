from uuid import UUID
from ub_backend.core.base.model import BaseModel


class UUIDMixin(BaseModel):
    id: UUID
    