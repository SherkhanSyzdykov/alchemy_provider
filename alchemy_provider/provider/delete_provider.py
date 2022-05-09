from abc import abstractmethod
from uuid import uuid4
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import delete, Delete
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery
from ..utils import AliasedManager
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

        uuid = uuid4()
        delete_stmt = self._bind_clause(
            clause=query.get_filters(),
            mapper=mapper,
            stmt=delete_stmt,
            clause_binder=clause_binder,
            uuid=uuid,
        )
        AliasedManager.delete(uuid=uuid)

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
