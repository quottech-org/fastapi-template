from ub_backend.database.postgres.db import Base
from .user import DBUser
from .good import DBGood
from .order import DBOrder
from .order_good import DBOrderGood
from .refresh_token import DBRefreshToken


metadata = Base.metadata

__all__ = [
    "metadata",
    "DBUser",
    "DBGood",
    "DBOrder",
    "DBOrderGood",
    "DBRefreshToken",
]
