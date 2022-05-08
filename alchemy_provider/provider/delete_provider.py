from abc import abstractmethod
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import delete, Delete
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery
from .base import BaseProvider


class DeleteProvider(BaseProvider):
    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_delete_stmt(self, *args, **kwargs):
        pass

    def _make_delete_stmt(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder
    ) -> Delete:
        delete_stmt = delete(mapper)
        delete_stmt = self._bind_clause(
            clause=query.get_filters(),
            mapper=mapper,
            stmt=delete_stmt,
            clause_binder=clause_binder
        )
        return delete_stmt

    async def _delete(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder
    ):
        delete_stmt = self._make_delete_stmt(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder,
        )
        await self._session.execute(delete_stmt)

    def __make_delete_join_stmt(self):
        """
        delete
        from test2
        using test
        where test2.test_id = test.id and
        test.id = 1 and test2.id < 2;
        Will be in next realize
        """
        raise NotImplementedError
