from typing import Optional, Any
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from .base import BaseClauseBuilder


class OrClauseBuilder(BaseClauseBuilder):
    def _get_or_clause_result(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Optional[Select]:
        pass
