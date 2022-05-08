from typing import Union, Type
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql import Select, Insert, Update, Delete
from ..query import CRUDQuery
from .base import BaseProvider


class JoinProvider(BaseProvider):
    def _join(
        self,
        field_name: str,
        query: Union[CRUDQuery, Type[CRUDQuery]],
        stmt: Union[Select, Insert, Update, Delete],
        mapper: DeclarativeMeta,
        aliased_mapper: AliasedClass
    ) -> Union[Select, Insert, Update, Delete]:
        mapper_field = getattr(mapper, field_name)
        join_strategy = query.get_join_strategy(field_name=field_name)

        return stmt.join(
            aliased_mapper,
            onclause=mapper_field,
            isouter=join_strategy.is_outer,
            full=join_strategy.is_full
        )
