from sqlalchemy import select
from typing import List
from uuid import UUID

from . import PGStorage, db_connection
from ub_backend.database.postgres.sqlalchemy_models.good import DBGood

class PGGoodStorage(PGStorage):

    def __init__(self, db: db_connection):
        super().__init__(db, DBGood)

    async def get_list_by_ids(self, ids: List[UUID]) -> List[DBGood]:
        result = await self._db.execute(
            select(self._model_cls).where(self._model_cls.id.in_(ids))
        )

        return result.scalars().all()
        