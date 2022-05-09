from typing import List, Optional, Sequence
from sqlalchemy.orm import DeclarativeMeta
from ..clause_binder.clause_binder import ClauseBinder
from ..query import CRUDQuery
from .select_provider import SelectProvider
from .insert_provider import InsertProvider
from .update_provider import UpdateProvider
from .delete_provider import DeleteProvider
from .count_provider import CountProvider


class Provider(
    CountProvider,
    InsertProvider,
    UpdateProvider,
    SelectProvider,
    DeleteProvider,
):
    async def select(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
    ) -> List[CRUDQuery]:
        return await self._select(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder,
        )

    async def insert(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[CRUDQuery]:
        return await self._insert(
            query=query,
            mapper=mapper,
            returning=returning
        )

    async def bulk_insert(
        self,
        queries: Sequence[CRUDQuery],
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[CRUDQuery]]:
        return await self._bulk_insert(
            queries=queries,
            mapper=mapper,
            returning=returning
        )

    async def update(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[CRUDQuery]]:
        return await self._update(
            query=query,
            mapper=mapper,
            returning=returning
        )

    async def delete(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta
    ):
        await self._delete(
            query=query,
            mapper=mapper
        )
