from typing import Literal, Union, Sequence
from sqlalchemy.orm import InstrumentedAttribute, DeclarativeMeta, \
    ColumnProperty
from sqlalchemy.sql import nullsfirst, nullslast
from sqlalchemy.sql.expression import UnaryExpression
from .base import BaseQuery


class SortingField:
    order_by: str
    order_reversed: bool = False
    nulls_place: Literal['first', 'last', None] = None

    def __init__(
        self,
        order_by: str,
        order_reversed: bool = False,
        nulls_place: Literal['first', 'last', None] = None
    ):
        self.order_by = order_by
        self.order_reversed = order_reversed
        self.nulls_place = nulls_place

    def make_sorting_column(
        self,
        mapper: DeclarativeMeta
    ) -> Union[InstrumentedAttribute, UnaryExpression]:

        mapper_field = getattr(mapper, self.order_by, None)

        if any((
                mapper_field is None,
                isinstance(mapper_field.property, ColumnProperty)
        )):
            raise AttributeError(
                f'Mapper {mapper} has not attribute {self.order_by}'
            )

        sorting_column = mapper_field.desc() \
            if self.order_reversed else mapper_field.ack()

        if self.nulls_place is None:
            return sorting_column

        if self.nulls_place == 'first':
            return nullsfirst(sorting_column)

        if self.nulls_place == 'last':
            return nullslast(sorting_column)

        return sorting_column


class SortingQuery(BaseQuery):
    sort_by: Union[SortingField, Sequence[SortingField]] = None
