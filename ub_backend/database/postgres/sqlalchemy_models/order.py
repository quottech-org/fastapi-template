from sqlalchemy import Column, DateTime, String, ForeignKey, Enum, Float
from sqlalchemy.dialects.postgresql import UUID

from ub_backend.database.postgres.db import Base
from ub_backend.app.model.enum import OrderType
from .mixin import CreateUpdateMixin, UUIDMixin


class DBOrder(UUIDMixin, CreateUpdateMixin, Base):
    __tablename__ = "order"
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}

    client_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    comment = Column(String, nullable=True)
    type = Column(Enum(OrderType), nullable=False)
    delivery_lon = Column(Float, nullable=True)
    delivery_lat = Column(Float, nullable=True)
