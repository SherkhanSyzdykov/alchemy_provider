from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Union, Any, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete


class BaseProvider(ABC):
    _session: Optional[Union[AsyncSession, async_scoped_session]] = None

    def set_session(
        self,
        session: Union[AsyncSession, async_scoped_session]
    ):
        self._session = session

    @abstractmethod
    def _bind_clause(
        self,
        clause: Dict[str, Any],
        stmt: Union[Select, Insert, Update, Delete],
        mapper: DeclarativeMeta
    ) -> Union[Select, Insert, Update, Delete]:
        pass
