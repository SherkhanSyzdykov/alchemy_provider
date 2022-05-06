from sqlalchemy.orm import DeclarativeMeta, ColumnProperty
from sqlalchemy.sql import Select, nullsfirst, nullslast
from query.sorting_query import SortingQuery
from .base import BaseProvider


class SortingProvider(BaseProvider):
    def bind_sorting(
        self,
        query: SortingQuery,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Select:
        if query.order_by is None:
            return select_stmt

        mapper_field = getattr(mapper, query.order_by, None)
        if mapper_field is None:
            return select_stmt

        if mapper_field.property is not ColumnProperty:
            return select_stmt

        sorting_column = mapper_field.desc() \
            if query.reversed else mapper_field.ack()

        if query.nulls_place is None:
            return select_stmt.order_by(sorting_column)

        if query.nulls_place == 'first':
            return select_stmt.order_by(nullsfirst(sorting_column))

        if query.nulls_place == 'last':
            return select_stmt.order_by(nullslast(sorting_column))

        return select_stmt
