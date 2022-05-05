from abc import ABC
from typing import Any, Callable, Optional
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import BinaryExpression
from .base import BaseClauseBinder


class SelfMethodBinder(ABC, BaseClauseBinder):
    def _is_self_method(
        self,
        lookup: str,
    ) -> bool:
        return self._get_self_method(lookup=lookup) is not None

    def _get_self_method(
        self,
        lookup: str
    ) -> Optional[Callable[
        [str, Any, DeclarativeMeta, Select], BinaryExpression]
    ]:
        lookup_parts = lookup.split(self.LOOKUP_STRING)

        for i in range(len(lookup_parts)-1, -1, -1):
            self_method = getattr(
                self,
                self.LOOKUP_STRING.join(lookup_parts[:i]),
                None
            )
            if self_method is not None:
                return self_method

    def _bind_self_method(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Select:
        self_method = self._get_self_method(lookup=lookup)
        if self_method is None:
            return select_stmt

        expression = self_method(lookup, value, mapper, select_stmt)

        return select_stmt.where(expression)
