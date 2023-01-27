from datetime import datetime
from ub_backend.core.base.model import BaseModel


class CreatedAtMixin(BaseModel):
    created_at: datetime


class UpdatedAtMixin(BaseModel):
    updated_at: datetime


class TimestampMixin(CreatedAtMixin, UpdatedAtMixin):
    pass
    