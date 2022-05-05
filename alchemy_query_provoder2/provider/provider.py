from abc import ABC
from typing import List, Dict, Any, Union
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from ..clause_binder.clause_binder import ClauseBinder, AbstractClauseBinder
from ..query.query import AbstractQuery
from .select_provider import SelectProvider


class Provider(SelectProvider):
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


class AbstractProvider(ABC, SelectProvider):
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
    ) -> List[AbstractQuery]:
        return await self._select(
            query=query,
            mapper=self._mapper
        )
