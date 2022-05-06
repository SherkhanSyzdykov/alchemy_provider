from typing import Any, Union, Dict
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from .self_method_binder import SelfMethodBinder
from .string_clause_binder import StringClauseBuilder


class ClauseBinder(SelfMethodBinder, StringClauseBuilder):
    def bind(
        self,
        clause: Dict[str, Any],
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete]
    ) -> Select:
        return self._bind(
            clause=clause,
            mapper=mapper,
            stmt=stmt,
        )
