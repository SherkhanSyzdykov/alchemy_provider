"""
"""
from typing import Optional, Callable, Any, Union
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import BinaryExpression
from .base import BaseClauseBuilder


class SelfMethodClauseBuilder(BaseClauseBuilder):
    """
    """
    def _is_self_method(
        self,
        lookup: str
    ) -> bool:
        """
        param lookup: user__id__in or user
        """
        return self._get_self_method(lookup=lookup) is not None

    def _get_self_method(
        self,
        lookup: str
    ) -> Optional[
        Callable[
            [str, Any, DeclarativeMeta, Select],
            Union[BinaryExpression, Select]
        ]
    ]:
        """
        param lookup: user__id__in or user
        """
        lookup_parts = lookup.split(self.LOOKUP_STRING)

        for i in range(len(lookup_parts), 0, -1):
            self_method = getattr(
                self,
                self.LOOKUP_STRING.join(lookup_parts[:i]),
                None
            )
            if self_method is not None:
                return self_method

    def _get_self_method_clause_result(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Optional[Select]:
        pass

    def _bind_self_method_result(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Select:
        """
        param lookup: user__id__in or user
        param value: [1, 2, 3] or {'id__in': [1, 2, 3]}
        """
        self_method = self._get_self_method(lookup=lookup)
        if self_method is None:
            return select_stmt

        self_method_result = self_method(
            lookup,
            value,
            mapper,
            select_stmt
        )

        if self_method_result is None:
            return select_stmt

        if isinstance(self_method_result, BinaryExpression):
            return select_stmt.where(self_method_result)

        if isinstance(self_method_result, Select):
            return self_method_result

        raise  # TODO
