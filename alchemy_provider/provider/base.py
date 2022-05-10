from __future__ import annotations
from abc import abstractmethod
from uuid import UUID
from typing import Any, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from ..clause_binder import ClauseBinder


class BaseProvider:
    @property
    @abstractmethod
    def _session(self) -> Union[AsyncSession, async_scoped_session]:
        pass

    @staticmethod
    def _bind_clause(
        clause: Dict[str, Any],
        stmt: Union[Select, Insert, Update, Delete],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
        uuid: UUID,
    ) -> Union[Select, Insert, Update, Delete]:
        return clause_binder.bind(
            clause=clause,
            stmt=stmt,
            mapper=mapper,
            uuid=uuid,
        )

    @staticmethod
    def _bind_simple_clause(
        clause: Dict[str, Any],
        stmt: Union[Select, Insert, Update, Delete],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
    ) -> Union[Select, Insert, Update, Delete]:
        return clause_binder.simple_bind(
            clause=clause,
            stmt=stmt,
            mapper=mapper,
        )
