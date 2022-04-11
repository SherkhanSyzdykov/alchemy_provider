from typing import Optional, Union
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import BinaryExpression
from .base import BaseClauseBuilder


class LimitClauseBuilder(BaseClauseBuilder):
    def _get_limit_clause_result(
        self,
        lookup: str,
        value: Union[str, int],
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Optional[Select]:
        pass
