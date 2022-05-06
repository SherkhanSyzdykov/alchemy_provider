from __future__ import annotations
from abc import abstractmethod
from typing import Optional, Any, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete


class BaseProvider:
    @property
    @abstractmethod
    def _session(self) -> Union[AsyncSession, async_scoped_session]:
        pass

    @abstractmethod
    def _bind_clause(
        self,
        clause: Dict[str, Any],
        stmt: Union[Select, Insert, Update, Delete],
        mapper: DeclarativeMeta
    ) -> Union[Select, Insert, Update, Delete]:
        pass
