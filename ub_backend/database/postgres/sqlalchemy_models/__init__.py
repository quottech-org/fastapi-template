from ub_backend.database.postgres.db import Base
from .user import DBUser


metadata = Base.metadata

__all__ = [
    "metadata",
    "DBUser",
]
