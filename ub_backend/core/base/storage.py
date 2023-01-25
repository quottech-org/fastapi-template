from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar, List, Union, Dict

from click import UUID


ModelT = TypeVar("ModelT")
DBconnectionT = TypeVar("DBconnectionT")


class BaseStorage(ABC):

    @abstractmethod
    def __init__(self, db: DBconnectionT, model_cls: ModelT):
        self._db: DBconnectionT = db
        self._model_cls: ModelT = model_cls

    @abstractmethod
    async def insert_many(self, obj: List[ModelT]) -> None:
        ...

    @abstractmethod
    async def insert_one(self, obj: ModelT) -> ModelT:
        ...

    @abstractmethod
    async def get_by_id(self, obj_id: Union[UUID, int]) -> ModelT:
        ...

    @abstractmethod
    async def get_one(self, filters: Dict[str, Any] = None) -> ModelT:
        ...

    @abstractmethod
    async def update(self, instance, update_data) -> ModelT:
        ...

    @abstractmethod
    async def update_one(
            self, obj_id: Union[int, UUID], update_fields: Dict[str, Any]
    ) -> ModelT:
        ...

    @abstractmethod
    async def get_many(
            self,
            filters: Dict[str, Any] = None,
            limit: int = 100,
            offset: int = 0,
    ) -> List[ModelT]:
        ...

    @abstractmethod
    async def get_count(self, filters: dict = None) -> int:
        ...

    @abstractmethod
    async def delete_one(self, obj_id: Union[int, UUID]) -> None:
        ...
