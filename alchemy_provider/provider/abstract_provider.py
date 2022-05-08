from abc import ABC
from typing import List, Dict, Any, Optional, Sequence, Type
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery
from .select_provider import SelectProvider
from .insert_provider import InsertProvider
from .update_provider import UpdateProvider
from .delete_provider import DeleteProvider
from .count_provider import CountProvider


class AbstractProvider(
    ABC,
    CountProvider,
    SelectProvider,
    InsertProvider,
    UpdateProvider,
    DeleteProvider,
):
    _mapper: DeclarativeMeta
    _clause_binder: ClauseBinder
    _query_type: Type[CRUDQuery]

    def make_select_stmt(
        self,
        **kwargs
    ) -> Select:
        return self._make_select_stmt(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper,
            clause_binder=self._clause_binder
        )

    def make_count_stmt(
        self,
        **kwargs
    ) -> Select:
        return self._make_count_stmt(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper,
            clause_binder=self._clause_binder
        )

    def make_insert_stmt(
        self,
        **kwargs,
    ) -> Insert:
        return self._make_insert_stmt(
            query=self._query_type(**kwargs),
            mapper=self._mapper
        )

    def make_bulk_insert_stmt(
        self,
        values_seq: Sequence[Dict[str, Any]],
        returning: bool = True,
    ) -> Insert:
        return self._make_bulk_insert_stmt(
            values_seq=values_seq,
            mapper=self._mapper,
            returning=returning
        )

    def make_update_stmt(
        self,
        filters: Dict[str, Any],
        values: Dict[str, Any],
        returning: bool = True
    ) -> Update:
        return self._make_update_stmt(
            query=self._query_type.set_filters(**filters).set_values(**values),
            mapper=self._mapper,
            clause_binder=self._clause_binder,
            returning=returning
        )

    def make_update_stmt_from_kwargs(
        self,
        returning: bool = True,
        **kwargs
    ) -> Update:
        return self._make_update_stmt_from_kwargs(
            query=self._query_type,
            mapper=self._mapper,
            clause_binder=self._clause_binder,
            returning=returning,
            **kwargs
        )

    def make_delete_stmt(self, **kwargs) -> Delete:
        return self._make_delete_stmt(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper,
            clause_binder=self._clause_binder
        )

    async def select(
        self,
        **kwargs
    ) -> List[CRUDQuery]:
        return await self._select(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper,
            clause_binder=self._clause_binder
        )

    async def insert(
        self,
        returning: bool = True,
        **kwargs
    ) -> Optional[CRUDQuery]:
        return await self._insert(
            query=self._query_type(**kwargs),
            mapper=self._mapper,
            returning=returning
        )

    async def bulk_insert(
        self,
        values_seq: Sequence[Dict[str, Any]],
        returning: bool = True,
    ) -> Optional[Sequence[CRUDQuery]]:
        return await self._bulk_insert(
            query=self._query_type,
            values_seq=values_seq,
            mapper=self._mapper,
            returning=returning
        )

    async def update(
        self,
        returning: bool = True,
        **kwargs,
    ) -> Optional[Sequence[CRUDQuery]]:
        return await self._update(
            query=self._query_type,
            mapper=self._mapper,
            clause_binder=self._clause_binder,
            returning=returning,
            **kwargs
        )

    async def update_from_query(
        self,
        filters: Dict[str, Any],
        values: Dict[str, Any],
        returning: bool = True,
    ) -> Optional[Sequence[CRUDQuery]]:
        return await self._update_from_query(
            query=self._query_type().set_filters(**filters).set_values(**values),
            mapper=self._mapper,
            clause_binder=self._clause_binder,
            returning=returning
        )

    async def delete(
        self,
        **kwargs
    ):
        await self._delete(
            query=self._query_type.set_filters(**kwargs),
            mapper=self._mapper,
            clause_binder=self._clause_binder,
        )
