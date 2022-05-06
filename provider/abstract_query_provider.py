from abc import ABC
from typing import List, Dict, Any, Union, Optional, Sequence, Type
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from clause_binder.abstract_clause_binder import AbstractClauseBinder
from query.base import BaseQuery
from query.query import AbstractQuery
from .select_provider import SelectProvider
from .insert_provider import InsertProvider
from .update_provider import UpdateProvider
from .delete_provider import DeleteProvider


class AbstractQueryProvider(
    ABC,
    SelectProvider,
    InsertProvider,
    UpdateProvider,
    DeleteProvider
):
    _mapper: DeclarativeMeta
    _clause_binder: AbstractClauseBinder
    _query_type: Type[AbstractQuery]

    def make_select_stmt(
        self,
        **kwargs
    ) -> Select:
        return super().make_select_stmt(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper
        )

    async def select(
        self,
        **kwargs
    ) -> List[BaseQuery]:
        return await self._select(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper
        )

    async def insert(
        self,
        returning: bool = True,
        **kwargs
    ) -> Optional[AbstractQuery]:
        return await self._insert(
            query=self._query_type(**kwargs),
            mapper=self._mapper,
            returning=returning
        )

    async def bulk_insert(
        self,
        values_seq: Sequence[Dict[str, Any]],
        returning: bool = True,
    ) -> Optional[Sequence[AbstractQuery]]:
        return await self._bulk_insert(
            query=self._query_type,
            values_seq=values_seq,
            mapper=self._mapper,
            returning=returning
        )

    async def update(
        self,
        filters: Dict[str, Any],
        values: Dict[str, Any],
        returning: bool = True,
    ) -> Optional[Sequence[AbstractQuery]]:
        return await self._update(
            query=self._query_type().set_filters(**filters).set_values(**values),
            mapper=self._mapper,
            returning=returning
        )

    async def delete(
        self,
        **kwargs
    ):
        await self._delete(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper
        )

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
