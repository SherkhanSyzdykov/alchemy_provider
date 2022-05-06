from typing import List, Dict, Any, Union, Optional, Sequence
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from clause_binder.clause_binder import ClauseBinder
from query.query import AbstractQuery
from .select_provider import SelectProvider
from .insert_provider import InsertProvider
from .update_provider import UpdateProvider
from .delete_provider import DeleteProvider


class Provider(
    SelectProvider,
    InsertProvider,
    UpdateProvider,
    DeleteProvider
):
    def _bind_clause(
        self,
        clause: Dict[str, Any],
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete],
    ) -> Union[Select, Insert, Update, Delete]:
        stmt = ClauseBinder().bind(
            clause=clause,
            mapper=mapper,
            stmt=stmt,
        )
        return stmt

    async def select(
        self,
        query: AbstractQuery,
        mapper: DeclarativeMeta
    ) -> List[AbstractQuery]:
        return await self._select(
            query=query,
            mapper=mapper
        )

    async def insert(
        self,
        query: AbstractQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[AbstractQuery]:
        return await self._insert(
            query=query,
            mapper=mapper,
            returning=returning
        )

    async def bulk_insert(
        self,
        queries: Sequence[AbstractQuery],
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[AbstractQuery]]:
        return await self._bulk_insert(
            queries=queries,
            mapper=mapper,
            returning=returning
        )

    async def update(
        self,
        query: AbstractQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[AbstractQuery]]:
        return await self._update(
            query=query,
            mapper=mapper,
            returning=returning
        )

    async def delete(
        self,
        query: AbstractQuery,
        mapper: DeclarativeMeta
    ):
        await self._delete(
            query=query,
            mapper=mapper
        )
