from abc import abstractmethod
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import delete, Delete
from query.delete_query import DeleteQuery
from .base import BaseProvider
from .join_provider import JoinProvider


class DeleteProvider(JoinProvider, BaseProvider):
    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass

    def make_delete_stmt(
        self,
        query: DeleteQuery,
        mapper: DeclarativeMeta,
    ) -> Delete:
        delete_stmt = delete(mapper)
        delete_stmt = self._bind_clause(
            clause=query.get_filters(),
            mapper=mapper,
            stmt=delete_stmt
        )
        return delete_stmt

    async def _delete(
        self,
        query: DeleteQuery,
        mapper: DeclarativeMeta
    ):
        delete_stmt = self.make_delete_stmt(
            query=query,
            mapper=mapper
        )
        await self._session.execute(delete_stmt)
