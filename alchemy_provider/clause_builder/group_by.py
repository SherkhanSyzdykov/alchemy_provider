from typing import Optional, Union, Iterable
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import BinaryExpression
from .base import BaseClauseBuilder


class GroupByClauseBuilder(BaseClauseBuilder):
    def _get_group_by_clause_result(
        self,
        lookup: str,
        value: Union[str, Iterable[str]],
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Optional[Select]:
        pass
