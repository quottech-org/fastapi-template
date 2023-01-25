from ub_backend.database.postgres.sqlalchemy_models.order_good import DBOrderGood
from . import PGStorage, db_connection


class PGOrderGoodStorage(PGStorage):
    def __init__(self, db: db_connection):
        super().__init__(db, DBOrderGood)

        