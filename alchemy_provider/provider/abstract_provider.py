from abc import ABC
from typing import List, Dict, Any, Union, Optional, Sequence
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from clause_binder.abstract_clause_binder import AbstractClauseBinder
from query.base import BaseQuery
from query.query import AbstractQuery
from .select_provider import SelectProvider
from .insert_provider import InsertProvider
from .update_provider import UpdateProvider
from .delete_provider import DeleteProvider


class AbstractProvider(
    ABC,
    SelectProvider,
    InsertProvider,
    UpdateProvider,
    DeleteProvider
):
    _mapper: DeclarativeMeta
    _clause_binder: AbstractClauseBinder

    def _bind_clause(
        self,
        clause: Dict[str, Any],
        stmt: Union[Select, Insert, Update, Delete],
        *args, **kwargs
    ) -> Union[Select, Insert, Update, Delete]:
        stmt = self._clause_binder.bind(
            clause=clause,
            stmt=stmt,
        )

        return stmt

    async def select(
        self,
        query: AbstractQuery
    ) -> List[BaseQuery]:
        return await self._select(
            query=query,
            mapper=self._mapper
        )

    async def insert(
        self,
        query: AbstractQuery,
        returning: bool = True,
    ) -> Optional[AbstractQuery]:
        return await self._insert(
            query=query,
            mapper=self._mapper,
            returning=returning
        )

    async def bulk_insert(
        self,
        queries: Sequence[AbstractQuery],
        returning: bool = True,
    ) -> Optional[Sequence[AbstractQuery]]:
        return await self._bulk_insert(
            queries=queries,
            mapper=self._mapper,
            returning=returning
        )

    async def update(
        self,
        query: AbstractQuery,
        returning: bool = True,
    ) -> Optional[Sequence[AbstractQuery]]:
        return await self._update(
            query=query,
            mapper=self._mapper,
            returning=returning
        )

    async def delete(
        self,
        query: AbstractQuery,
    ):
        await self._delete(
            query=query,
            mapper=self._mapper
        )
