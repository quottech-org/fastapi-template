from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import NUMERIC
from ub_backend.database.postgres.db import Base

from .mixin import CreateUpdateMixin, UUIDMixin


class DBGood(UUIDMixin, CreateUpdateMixin, Base):
    __tablename__ = "good"
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}

    title = Column(String, nullable=False)
    description = Column(String)
    # TODO: type + specs
    price_usd = Column(NUMERIC, nullable=False)
    price_gel = Column(NUMERIC)
    price_rub = Column(NUMERIC)
    price_eur = Column(NUMERIC)
    # TODO: add qty
    