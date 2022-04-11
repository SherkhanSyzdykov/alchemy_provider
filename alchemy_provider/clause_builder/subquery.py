"""
RY PASSING LIKE
{
    'user': {
        'id__in': select(
            MeterType.user_id
        ).where(MeterType.name.ilike('%some_name%')).subquery()
    }
}
"""
from typing import Optional, Union, Any
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Subquery
from sqlalchemy.sql.expression import BinaryExpression
from sqlalchemy.sql.selectable import ScalarSelect
from .base import BaseClauseBuilder


class SubqueryClauseBuilder(BaseClauseBuilder):
    """
    """

    @staticmethod
    def is_subquery_value(
        value: Any
    ) -> bool:
        if isinstance(value, Select):
            return True

        if isinstance(value, Subquery):
            return True

        if isinstance(value, ScalarSelect):
            return True

        return False

    def _get_subquery_clause_result(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Optional[Select]:
        pass

    def _bind_subquery(
        self,
        lookup: str,
        subquery: Union[Select, Subquery, ScalarSelect],
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Select:
        pass