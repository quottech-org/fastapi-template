from abc import ABC
from ast import Dict
from ctypes import Union
from typing import Any, Generic, Type, TypeVar, List

from click import UUID


ModelT = TypeVar("ModelT")
DBconnectionT = TypeVar("DBconnectionT")


class BaseStorage(ABC):
    model_cls: Type[ModelT] = ModelT

    def __init__(self, db: DBconnectionT):
        self._db: DBconnectionT = db

    async def insert_many(self, obj: List[ModelT]) -> None:
        ...

    async def insert_one(self, obj: ModelT) -> ModelT:
        ...

    async def get_by_id(self, obj_id: Union[UUID, int]) -> ModelT:
        ...

    async def get_one(self, filters: Dict[str, Any] = None) -> ModelT:
        ...

    async def update(self, instance, update_data) -> ModelT:
        ...

    async def update_one(
            self, obj_id: Union[int, UUID], update_fields: Dict[str, Any]
    ) -> ModelT:
        ...

    async def get_many(
            self,
            filters: Dict[str, Any] = None,
            limit: int = 100,
            offset: int = 0,
    ) -> List[ModelT]:
        ...

    async def get_count(self, filters: dict = None) -> int:
        ...

    async def delete_one(self, obj_id: Union[int, UUID]) -> None:
        ...
