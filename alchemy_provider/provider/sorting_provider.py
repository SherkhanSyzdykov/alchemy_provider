from typing import Sequence, Union
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty, InstrumentedAttribute
from sqlalchemy.sql import Select, nullsfirst, nullslast
from ..query import CRUDQuery, SortingField
from .base import BaseProvider


class SortingProvider(BaseProvider):
    _sorting_fields: Sequence[str] = None

    def bind_sorting(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Select:
        if query.sort_by is None:
            return select_stmt

        return self._bind_sorting(
            sorting_field=query.sort_by,
            mapper=mapper,
            select_stmt=select_stmt
        )

    def _bind_sorting(
        self,
        sorting_field: Union[SortingField, Sequence[SortingField]],
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Select:
        if isinstance(sorting_field, Sequence):
            for sort_by in sorting_field:
                select_stmt = self._bind_sorting(
                    sorting_field=sort_by,
                    mapper=mapper,
                    select_stmt=select_stmt
                )
            return select_stmt

        if self._sorting_fields is not None:
            if sorting_field.order_by not in self._sorting_fields:
                raise KeyError(
                    f'Order by field {sorting_field.order_by} '
                    f'not in {self._sorting_fields}'
                )

        sorting_column = sorting_field.make_sorting_column(mapper=mapper)
        return select_stmt.order_by(sorting_column)
