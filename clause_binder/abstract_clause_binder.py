from abc import ABC
from typing import Any, Union, Dict
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from .self_method_binder import SelfMethodBinder
from .string_clause_binder import StringClauseBuilder


class AbstractClauseBinder(ABC, SelfMethodBinder, StringClauseBuilder):
    _mapper: DeclarativeMeta

    def bind(
        self,
        clause: Dict[str, Any],
        stmt: Union[Select, Insert, Update, Delete]
    ) -> Select:
        return self._bind(
            clause=clause,
            mapper=self._mapper,
            stmt=stmt,
        )
