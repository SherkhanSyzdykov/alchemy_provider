from typing import Any, Optional, Union
from sqlalchemy import alias
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql import Select
from sqlalchemy.sql.expression import BinaryExpression
from .base import BaseClauseBuilder


class AliasedClauseBuilder(BaseClauseBuilder):
    def get_aliased(
        self,
        lookup: str
    ) -> Optional[AliasedClass]:
        pass

    def _get_aliased_clause_result(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Optional[Select]:
        pass
