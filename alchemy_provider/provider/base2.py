from abc import ABC, abstractmethod
from typing import Union, Tuple, Any, List, Optional
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession
from alchemy_provider.clause_builder import BaseClauseBuilder


class BaseProvider(ABC):
    _session: Union[AsyncSession, async_scoped_session]

    class ClauseBuilder(BaseClauseBuilder):
        pass

    def __init__(
        self,
        session: Union[AsyncSession, async_scoped_session]
    ):
        self._session = session

    @abstractmethod
    async def get_row(self, *args, **kwargs) -> Tuple[Any]:
        pass

    @abstractmethod
    async def get(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def select_row(self, *args, **kwargs) -> List[Tuple[Any]]:
        pass

    @abstractmethod
    async def select(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def update(self, *args, **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    async def bulk_update(self, *args, **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    async def conditional_bulk_update(self, *args, **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    async def insert(self, *args, **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    async def bulk_insert(self, *args, **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    async def bulk_delete(self, *args, **kwargs):
        pass

    @abstractmethod
    async def get_or_insert(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def update_or_insert(self, *args, **kwargs) -> Optional[Any]:
        pass

    @abstractmethod
    async def bulk_update_or_insert(self, *args, **kwargs) -> Optional[Any]:
        pass
