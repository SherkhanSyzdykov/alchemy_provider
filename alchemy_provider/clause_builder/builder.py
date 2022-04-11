"""
"""
from typing import Any, Optional, Tuple, Callable, Union, Iterable
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import BinaryExpression

from .base import BaseClauseBuilder
from .where import WhereClauseBuilder
from .subquery import SubqueryClauseBuilder
from .order_by import OrderByClauseBuilder
from .group_by import GroupByClauseBuilder
from .limit import LimitClauseBuilder
from .offset import OffsetClauseBuilder
from .self_method import SelfMethodClauseBuilder
from .aliased import AliasedClauseBuilder


class ClauseBuilder(
    WhereClauseBuilder,
    SubqueryClauseBuilder,
    SelfMethodClauseBuilder,
    OrderByClauseBuilder,
    GroupByClauseBuilder,
    LimitClauseBuilder,
    OffsetClauseBuilder,
    AliasedClauseBuilder
):
    @property
    def clause_result_priority(self) -> Iterable[
        Callable[
            [str, Any, DeclarativeMeta, Select],
            Optional[Select]
        ]
    ]:
        return (
            self._get_self_method_clause_result,
            self._get_aliased_clause_result,
            self._get_where_clause_result,
            self._get_subquery_clause_result,
            self._get_group_by_clause_result,
            self._get_order_by_clause_result,
            self._get_limit_clause_result,
            self._get_offset_clause_result
        )

    def _get_expression(
        self,
        lookup: str,
        mapper: DeclarativeMeta
    ) -> InstrumentedAttribute:
        pass

    def _bind_expression(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Select:
        pass

    def build(
        self,
        mapper: Optional[DeclarativeMeta] = None,
        select_stmt: Optional[Select] = None,
        **filters,
    ) -> Select:
        if select_stmt is None:
            select_stmt = self.select_stmt

        if mapper is None:
            mapper = self.mapper

        for lookup, value in filters.items():
            select_stmt = self._bind_expression(
                lookup=lookup,
                value=value,
                mapper=mapper,
                select_stmt=select_stmt,
            )

        return select_stmt
