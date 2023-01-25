from typing import List
from uuid import UUID
from ub_backend.app.model.full_order import FullOrder
from ub_backend.app.model.order import Order
from ub_backend.database.postgres.storage.order_good_storage import PGOrderGoodStorage
from . import PGStorage, db_connection
from ub_backend.database.postgres.sqlalchemy_models.order import DBOrder
from ub_backend.database.postgres.sqlalchemy_models.order_good import DBOrderGood


class PGOrderStorage(PGStorage):

    def __init__(self, db: db_connection):
        super().__init__(db, DBOrder)
        self._order_good_cls = DBOrderGood
        self._order_good_storage = PGOrderGoodStorage(db=db)

    async def create_order(self, order: DBOrder, goods_ids: List[UUID]) -> DBOrder:
        db_order: DBOrder = await super().insert_one(order)
        await self._order_good_storage.insert_many([DBOrderGood(order_id=db_order.id, good_id=i) for i in goods_ids])

        return db_order
