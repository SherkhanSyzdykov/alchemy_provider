from typing import Literal, Union, Sequence, Optional, Dict
from sqlalchemy.orm import InstrumentedAttribute, DeclarativeMeta, \
    ColumnProperty
from sqlalchemy.sql import nullsfirst, nullslast
from sqlalchemy.sql.expression import UnaryExpression
from ..utils import cls_or_ins
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

    @cls_or_ins
    def set_sorters(
        cls_or_ins,
        **kwargs
    ) -> BaseQuery:
        self = cls_or_ins
        if cls_or_ins.is_class():
            self = cls_or_ins()

        sort_by = kwargs.get('sort_by')
        if sort_by is not None:
            self._set_sort_by(sort_by)
            return self

        if order_by := kwargs.get('order_by'):
            self._set_sort_by(
                sort_by=SortingField(
                    order_by=order_by,
                    order_reversed=kwargs.get('order_reversed'),
                    nulls_place=kwargs.get('nulls_place')
                )
            )

        return self

    def _set_sort_by(
        self,
        sort_by: Union[
            SortingField,
            Sequence[SortingField],
            Sequence[Dict[str, Optional[Union[str, bool]]]]
        ]
    ):

        if isinstance(sort_by, SortingField):
            self.sort_by = sort_by
            return

        if not isinstance(sort_by, Sequence):
            return

        sorting_fields = list()
        for sorting_field in sort_by:
            if isinstance(sorting_field, SortingField):
                sorting_fields.append(sorting_field)
            if isinstance(sorting_field, dict):
                sorting_fields.append(SortingField(
                    order_by=sorting_field.get('order_by'),
                    order_reversed=sorting_field.get('order_reversed'),
                    nulls_place=sorting_field.get('nulls_place')
                ))

        if sorting_fields:
            self.sort_by = sorting_fields
