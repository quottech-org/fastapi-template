from typing import Any, Union, Type, List, Dict, Tuple
from uuid import UUID

import sqlalchemy
from sqlalchemy import select

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.orm import Session
from ub_backend.app.exception.common import BadRequestExcetion, NotFoundException

from ub_backend.core.base.storage import BaseStorage, ModelT

db_connection = Union[Session, async_scoped_session]

class PGStorage(BaseStorage):

    def __init__(self, db: db_connection, model_cls: ModelT):
        self._db: Union[Session, async_scoped_session] = db
        self._model_cls: ModelT = model_cls

    async def insert_many(self, obj: List[ModelT]) -> None:
        self._db.add_all(obj)

    async def insert_one(self, obj: ModelT) -> ModelT:
        try:
            self._db.add(obj)
            await self._db.flush()
            await self._db.refresh(obj)
            self._db.expunge(obj)
        except sqlalchemy.exc.IntegrityError as e:
            raise BadRequestExcetion(detail=str(e))
        return obj

    async def get_by_id(self, obj_id: Union[UUID, int]) -> ModelT:
        return await self._db.get(self._model_cls, obj_id)

    async def get_one(self, filters: dict = None) -> ModelT:
        query = select(self._model_cls)
        for attr, value in filters.items():
            query = query.filter(getattr(self._model_cls, attr) == value)

        result = (await self._db.execute(query)).scalars().first()
        if not result:
            return None
        self._db.expunge(result)
        return result

    async def update(self, instance, update_data) -> ModelT:
        for k, v in update_data.items():
            setattr(instance, k, v)

        self._db.add(instance)
        await self._db.flush()
        await self._db.refresh(instance)
        self._db.expunge(instance)
        return instance

    async def update_one(
        self, obj_id: Union[int, UUID], update_fields: Dict[str, Any]
    ) -> ModelT:
        instance = await self.get_one({"id": obj_id})
        if instance is None:
            raise NotFoundException()
        return await self.update(instance, update_fields)

    async def get_many(
        self,
        filters: dict = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ModelT]:
        if limit > 100:
            limit = 100
        result = await self._db.execute(
            select(self._model_cls).filter_by(**filters).limit(limit).offset(offset)
        )

        return result.scalars().all()

    async def get_count(self, filters: dict = None) -> int:
        count: int = (
            await self._db.execute(select(self._model_cls)).filter(**filters).count()
        )
        return count

    async def get_list_and_count(
        self,
        filters: dict = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Tuple[List[ModelT], int]:
        docs = await self.get_many(
            filters=filters,
            limit=limit,
            offset=offset,
        )

        count = await self.get_count(filters=filters)
        return docs, count

    async def delete_one(self, obj_id: Union[int, UUID]) -> None:
        model = await self.get_by_id(obj_id)
        if model is None:
            raise NotFoundException
        await self._db.delete(model)

    async def get_or_create(self, obj: ModelT, exclude_fields: list = None) -> ModelT:
        result = await self.get_one(obj.dict(exclude_fields=exclude_fields))
        if result is None:
            result = await self.insert_one(obj)

        return result
