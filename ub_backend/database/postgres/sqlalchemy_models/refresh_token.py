from uuid import uuid4

from sqlalchemy import Column, String

from .mixin import BaseToken
from ub_backend.database.postgres.db import Base


class DBRefreshToken(BaseToken, Base):
    __tablename__ = "refresh_token"
    __mapper_args__ = {"eager_defaults": True}

    token = Column(String, default=str(uuid4()), nullable=False)
