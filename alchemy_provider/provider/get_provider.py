from abc import abstractmethod
from typing import Union, Type
from sqlalchemy.orm import DeclarativeMeta
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery
from .base import BaseProvider
from .select_provider import SelectProvider


class GetProvider(SelectProvider, BaseProvider):
    _does_not_exist_exception = None

    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    async def _get(
        self,
        query: Union[Type[CRUDQuery], CRUDQuery],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder
    ) -> CRUDQuery:
        query.limit = 1
        query.offset = None
        queries = await self._select(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder
        )
        if queries:
            return queries[0]

        if self._does_not_exist_exception is None:
            raise ValueError(
                f'Record with passed query does not exist'
            )

        raise self._does_not_exist_exception
