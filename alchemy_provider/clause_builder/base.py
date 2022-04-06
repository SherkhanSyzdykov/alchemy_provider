from abc import ABC
from types import MappingProxyType
from typing import Type, Union, Iterable, Optional, Any, List, Callable
from sqlalchemy import Table, Column
from sqlalchemy.sql import Select, select
from sqlalchemy.sql.expression import BinaryExpression
from sqlalchemy.orm import (
    DeclarativeMeta,
    InstrumentedAttribute,
    RelationshipProperty
)


class BaseClauseBuilder(ABC):
    """
    Build clause select statement
    """

    LOOKUP_STRING = '__'
    EQUAL_OPERATOR = 'e'
    NOT_EQUAL_OPERATOR = 'ne'
    LESS_THAN_OPERATOR = 'l'
    LESS_THAN_OR_EQUAL_TO_OPERATOR = 'le'
    GREATER_THAN_OPERATOR = 'g'
    GREATER_THAN_OR_EQUAL_TO_OPERATOR = 'ge'
    LIKE_OPERATOR = 'like'
    ILIKE_OPERATOR = 'ilike'
    IN_OPERATOR = 'in'
    NOT_IN_OPERATOR = 'not_in'
    ALL_OBJECTS_FILTER = '__all__'
    AND_LOOKUP = '__and__'
    OR_LOOKUP = '__or__'

    LOOKUP_OPERATORS = MappingProxyType({
        EQUAL_OPERATOR:
            lambda _column, _value: _column == _value,
        NOT_EQUAL_OPERATOR:
            lambda _column, _value: _column != _value,
        LESS_THAN_OPERATOR:
            lambda _column, _value: _column < _value,
        LESS_THAN_OR_EQUAL_TO_OPERATOR:
            lambda _column, _value: _column <= _value,
        GREATER_THAN_OPERATOR:
            lambda _column, _value: _column > _value,
        GREATER_THAN_OR_EQUAL_TO_OPERATOR:
            lambda _column, _value: _column >= _value,
        LIKE_OPERATOR:
            lambda _column, _value: _column.like(_value),
        ILIKE_OPERATOR:
            lambda _column, _value: _column.ilike(_value),
        IN_OPERATOR:
            lambda _column, _value: _column.in_(_value),
        NOT_IN_OPERATOR:
            lambda _column, _value: _column.not_in(_value),
    })

    _table: Type[Table]

    def __init__(
        self,
        table: Type[Table]
    ):
        self.table = table

    @property
    def table(self) -> Type[Table]:
        return self._table

    @table.setter
    def table(self, value: Type[Table]):
        if type(value) is not Table:
            raise  # TODO

        self._table = value

    @property
    def select_stmt(self) -> Select:
        return select(self.table)

    @staticmethod
    def get_related_table(
        table: Type[Table],
        relationship_name: str,
    ) -> Table:
        relationship = getattr(table, relationship_name, None)
        if relationship is None:
            raise  # TODO

        if not isinstance(relationship.property, RelationshipProperty):
            raise  # TODO

        return relationship.property.mapper.class_.__table__

    def _get_column(
        self,
        lookup: str
    ) -> Union[Column, InstrumentedAttribute]:
        pass

    def _remove_lookup_key(
        self,
        lookup: str
    ) -> str:
        """
        lookup: user__id__in
        return: user__id
        """
        *_, lookup_key = lookup.split(self.LOOKUP_STRING)
        if lookup_key in self.LOOKUP_OPERATORS:
            return self.LOOKUP_STRING.join(_)

        return lookup

    def _get_lookup_function(
        self,
        lookup: str
    ) -> Callable[[InstrumentedAttribute, Any], BinaryExpression]:
        *_, lookup_key = lookup.split(self.LOOKUP_STRING)
        return self.LOOKUP_OPERATORS.get(
            lookup_key,
            self.LOOKUP_OPERATORS.get(self.EQUAL_OPERATOR)
        )

    def _get_self_method(
        self,
        lookup: str
    ) -> Optional[Callable[[str, Any, Select], BinaryExpression]]:
        lookup_without_key = self._remove_lookup_key(lookup=lookup)


        self_method = getattr(self, lookup_without_key, None)
        if self_method is not None:
            return self_method

        column_name, *_ = lookup_without_key.split(self.LOOKUP_STRING)

    def _bind_expression(
        self,
        lookup: str,
        value: Any,
        select_method: Select
    ) -> Select:
        """
        lookup:
            user__id__in: [1, 2, 3]
            or
            user: {id__in: [1, 2, 3]}
        """
        self_method = self._get_self_method(lookup=lookup)
        select_method.join()







    def _build(
        self,
        select_stmt: Optional[Select] = None,
        **filters
    ) -> Select:
        if select_stmt is None:
            select_stmt = self.select_stmt



    def build(
        self,
        select_stmt: Optional[Select] = None,
        **filters
    ) -> Select:

        for key, value in filters.items():
            pass


    def _build_and_clause(
        self,
        **filters
    ) -> BinaryExpression:
        pass

    def _build_or_clause(
        self,
        **filters
    ) -> BinaryExpression:
        pass

    def _build_order_by(
        self,
        order_by: Union[str, Iterable[str]]
    ):
        pass

    def _build_group_by(
        self,
        group_by: Union[str, Iterable[str]]
    ):
        pass

    def _build_limit(
        self,
        limit: int
    ):
        pass

    def _build_offset(
        self,
        offset: int
    ):
        pass


class BaseMapperClauseBuilder(BaseClauseBuilder, ABC):
    _mapper: DeclarativeMeta

    def __init__(
        self,
        mapper: DeclarativeMeta
    ):
        super().__init__(table=mapper.__table__)
        self.mapper = mapper
        self.table = mapper.__table__

    @property
    def mapper(self) -> DeclarativeMeta:
        return self._mapper

    @mapper.setter
    def mapper(self, value: DeclarativeMeta):
        if not isinstance(value, DeclarativeMeta):
            raise  # TODO

        self._mapper = value


class BaseTableClauseBuilder(BaseClauseBuilder, ABC):
    _table: Type[Table]

    @property
    def table(self) -> Type[Table]:
        return self._table

    @table.setter
    def table(self, value: Type[Table]):
        if type(value) is not Table:
            raise  # TODO

        self._table = value
