from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from ub_backend.database.postgres.db import Base

from .mixin import IDMixin


class DBOrderGood(IDMixin, Base):
    __tablename__ = "order_good"
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}

    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("order.id", ondelete="CASCADE"),
        nullable=False,
    )
    good_id = Column(
        UUID(as_uuid=True),
        ForeignKey("good.id", ondelete="CASCADE"),
        nullable=False,
    )
    # TODO: add qty
    # qty = Column(Integer)
