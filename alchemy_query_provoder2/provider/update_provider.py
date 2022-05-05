from abc import ABC
from typing import Any, Optional, List, Mapping, Sequence
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty
from sqlalchemy.sql import update, Update
from ..query.update_query import UpdateQuery
from .base import BaseProvider
from .join_provider import JoinProvider


class UpdateProvider(ABC, JoinProvider, BaseProvider):
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
        if returning:
            update_stmt = update_stmt.returning(mapper)

        return update_stmt

    def make_bulk_update_stmt(self):
        pass

    def __make_updatable_values(self):
        pass
