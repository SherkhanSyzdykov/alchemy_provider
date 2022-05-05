from abc import ABC, abstractmethod
from typing import Any, Dict, Sequence, Optional
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty
from sqlalchemy.sql import update, Update
from ..query.update_query import UpdateQuery
from .base import BaseProvider
from .join_provider import JoinProvider


class UpdateProvider(ABC, JoinProvider, BaseProvider):
    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    def make_update_stmt(
        self,
        query: UpdateQuery,
        mapper: DeclarativeMeta,
        returning: bool = True
    ) -> Update:
        update_stmt = update(mapper)
        update_stmt = self._bind_clause(
            clause=query.filters,
            mapper=mapper,
            stmt=update_stmt,
        )

        updatable_values = self.__make_updatable_values(
            query=query,
            mapper=mapper,
        )
        update_stmt = update_stmt.values(**updatable_values)

        if returning:
            update_stmt = update_stmt.returning(mapper)

        return update_stmt

    def make_bulk_update_stmt(self):
        """
        Will be released in next version
        Use simple make_update_stmt for simple bulk_updates
        """
        raise NotImplementedError

    async def _update(
        self,
        query: UpdateQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[UpdateQuery]]:
        """
        Returns sequence of query instance if returning is True
        """
        update_stmt = self.make_update_stmt(
            query=query,
            mapper=mapper,
            returning=returning
        )

        scalar_result = await self._session.execute(update_stmt)

        if not returning:
            return

        updated_queries = list()
        for row in scalar_result:
            updated_query = query.from_row(row)
            updated_queries.append(updated_query)

        return updated_queries

    def __make_updatable_values(
        self,
        query: UpdateQuery,
        mapper: DeclarativeMeta
    ) -> Dict[str, Any]:
        updatable_values = dict()
        for item, value in query.values.items():
            mapper_field = getattr(mapper, item, None)
            if mapper_field is None:
                continue

            if mapper_field.property is not ColumnProperty:
                continue

            updatable_values[item] = value

        return updatable_values
