"""
Example:
{
    "user": {
        "id__in": [1, 2, 3],
        "name__ilike": "%some_name%",
        "group": {
            "name__in": ["readers", "writers"]
        }
    }
}
or
{
    "user__id__in": [1, 2, 3],
    "user__name__ilike": "%some_name%",
    "user__group__name__in": ["readers", "writers"]
}
"""
from typing import Optional, Any, Union
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute
from sqlalchemy.sql import Select, select
from sqlalchemy.sql.expression import BinaryExpression
from .base import BaseClauseBuilder


class WhereClauseBuilder(BaseClauseBuilder):
    @staticmethod
    def get_column(
        lookup: str,
        mapper: DeclarativeMeta,
    ) -> Optional[InstrumentedAttribute]:
        pass

    def _get_where_clause_result(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Optional[Select]:
        pass

