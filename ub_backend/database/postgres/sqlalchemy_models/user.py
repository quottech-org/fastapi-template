from sqlalchemy import Column, DateTime, String

from ub_backend.database.postgres.db import Base

from .mixin import CreateUpdateMixin, UUIDMixin


class DBUser(UUIDMixin, CreateUpdateMixin, Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"eager_defaults": True}

    nick_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    description = Column(String)
    birthday = Column(DateTime)
    email = Column(String, nullable=False)
    phone_number = Column(String)
    avatar = Column(String, nullable=True)  # HTTP url
    salt = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
