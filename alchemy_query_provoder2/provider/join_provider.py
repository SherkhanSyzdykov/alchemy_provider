from typing import Union, Type
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from query.join_query import JoinQuery
from .base import BaseProvider


class JoinProvider(BaseProvider):
    def _join(
        self,
        field_name: str,
        query: Union[JoinQuery, Type[JoinQuery]],
        stmt: Union[Select, Insert, Update, Delete],
        mapper: DeclarativeMeta
    ) -> Union[Select, Insert, Update, Delete]:
        mapper_field = getattr(mapper, field_name)
        join_strategy = query.get_join_strategy(field_name=field_name)

        return stmt.join(
            mapper_field,
            isouter=join_strategy.is_outer,
            full=join_strategy.is_full
        )
