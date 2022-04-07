from abc import ABC
from types import MappingProxyType
from typing import Type, Union, Iterable, Optional, Any, List, Callable, Tuple, Mapping
from sqlalchemy import Table, Column
from sqlalchemy.sql import Select, select, or_, and_
from sqlalchemy.sql.expression import BinaryExpression
from sqlalchemy.orm import (
    DeclarativeMeta,
    InstrumentedAttribute,
    RelationshipProperty,
    ColumnProperty
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
    ASC_ORDER = 'asc'
    DESC_ORDER = 'desc'

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

    _table: Optional[Type[Table]] = None
    _mapper: DeclarativeMeta

    def __init__(
        self,
        mapper: DeclarativeMeta
    ):
        self.mapper = mapper
        self.table = mapper.__table__

    @property
    def table(self) -> Type[Table]:
        return self._table

    @table.setter
    def table(self, value: Type[Table]):
        if type(value) is not Table:
            raise  # TODO

        self._table = value

    @property
    def mapper(self) -> DeclarativeMeta:
        return self._mapper

    @mapper.setter
    def mapper(self, value: DeclarativeMeta):
        if not isinstance(value, DeclarativeMeta):
            raise  # TODO
        self._mapper = value

    @property
    def select_stmt(self) -> Select:
        return select(self.mapper)

    @staticmethod
    def get_related_mapper(
        mapper: DeclarativeMeta,
        relationship_name: str,
    ) -> DeclarativeMeta:
        relationship = getattr(mapper, relationship_name, None)
        if relationship is None:
            raise  # TODO

        if not isinstance(relationship.property, RelationshipProperty):
            raise  # TODO

        return relationship.property.mapper.class_

    @staticmethod
    def is_related_field(
        mapper: DeclarativeMeta,
        relationship_name: str
    ) -> bool:
        related_field = getattr(mapper, relationship_name, None)
        if related_field is None:
            return False

        return isinstance(related_field.property, RelationshipProperty)

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

    def _get_lookup_key(
        self,
        lookup: str,
    ) -> str:
        *_, lookup_key = lookup.split(self.LOOKUP_STRING)
        if lookup_key in self.LOOKUP_OPERATORS:
            return lookup_key

        return self.EQUAL_OPERATOR

    def _get_lookup_function(
        self,
        lookup: str
    ) -> Callable[[InstrumentedAttribute, Any], BinaryExpression]:
        lookup_key = self._get_lookup_key(lookup=lookup)
        return self.LOOKUP_OPERATORS.get(
            lookup_key,
            self.LOOKUP_OPERATORS.get(self.EQUAL_OPERATOR)
        )

    def _is_self_method(
        self,
        method_name: str
    ) -> bool:
        return bool(getattr(self, method_name, False))

    def _get_self_method(
        self,
        lookup: str
    ) -> Optional[
        Callable[[str, Any, Select, DeclarativeMeta], BinaryExpression]
    ]:
        parts_of_lookup = lookup.split(self.LOOKUP_STRING)
        for i in range(len(parts_of_lookup), 0, -1):
            self_method = getattr(
                self,
                self.LOOKUP_STRING.join(parts_of_lookup[:i]),
                None
            )
            if self_method is not None:
                return self_method

    def _get_self_method_expression(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Optional[Union[BinaryExpression, Select]]:
        self_method = self._get_self_method(lookup=lookup)
        if self_method is not None:
            expression = self_method(
                lookup=lookup,
                value=value,
                mapper=mapper,
                select_stmt=select_stmt
            )
            return expression

    def _bind_self_method_expression(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Select:
        self_method_result = self._get_self_method_expression(
            lookup=lookup,
            value=value,
            mapper=mapper,
            select_stmt=select_stmt
        )
        if self_method_result is None:
            return select_stmt

        if isinstance(self_method_result, BinaryExpression):
            return select_stmt.where(self_method_result)

        if isinstance(self_method_result, Select):
            return self_method_result

    def _get_column(
        self,
        lookup: str,
        mapper: DeclarativeMeta
    ) -> Union[Column, InstrumentedAttribute]:
        lookup = self._remove_lookup_key(lookup=lookup)
        lookup_parts = lookup.split(self.LOOKUP_STRING)

        for i in range(len(lookup_parts)):
            field = getattr(mapper, lookup_parts[i], None)
            if field is None:
                raise  # TODO

            if isinstance(field.property, ColumnProperty):
                return field

            if isinstance(field.property, RelationshipProperty):
                related_mapper = self.get_related_mapper(
                    mapper=mapper,
                    relationship_name=field
                )
                return self._get_column(
                    mapper=related_mapper,
                    lookup=self.LOOKUP_STRING.join(lookup_parts[i+1:])
                )

        raise  # TODO

    def _get_expression(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
    ) -> BinaryExpression:
        lookup_function = self._get_lookup_function(lookup=lookup)
        column = self._get_column(lookup=lookup, mapper=mapper)
        return lookup_function(column, value)

    def _get_expressions(
        self,
        mapper: DeclarativeMeta,
        **filters
    ) -> List[BinaryExpression]:
        expressions: List[BinaryExpression] = []
        for key, value in filters.items():
            if isinstance(value, Mapping):
                if key in (self.OR_LOOKUP, self.AND_LOOKUP):
                    nested_expressions = self._get_expressions(
                        mapper=mapper,
                        **value
                    )
                    expressions.extend(nested_expressions)
                    continue

                related_mapper = self.get_related_mapper(
                    mapper=mapper,
                    relationship_name=key
                )
                related_expressions = self._get_expression(
                    mapper=related_mapper,
                    **value
                )
                expressions.extend(related_expressions)
                continue

            expression = self._get_expression(
                mapper=mapper,
                lookup=key,
                value=value
            )
            expressions.append(expression)

        return expressions

    def _bind_expression(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Select:
        """
        lookup:
            user__id__in: [1, 2, 3]
            or
            user: {id__in: [1, 2, 3]}
        """
        if self._is_self_method(method_name=lookup):
            return self._bind_self_method_expression(
                lookup=lookup,
                value=value,
                mapper=mapper,
                select_stmt=select_stmt,
            )
        expression = self._get_expression(
            lookup=lookup,
            value=value,
            mapper=mapper,
        )
        return select_stmt.where(expression)

    def _bind_or_clause(
        self,
        mapper: DeclarativeMeta,
        select_stmt: Select,
        **filters
    ) -> Select:
        expressions = self._get_expressions(
            mapper=mapper,
            **filters
        )
        return select_stmt.where(or_(*expressions))

    def _bind_and_clause(
        self,
        mapper: DeclarativeMeta,
        select_stmt: Select,
        **filters,
    ) -> Select:
        expressions = self._get_expressions(
            mapper=mapper,
            **filters
        )
        return select_stmt.where(and_(*expressions))

    def _handle_mapping_value(
        self,
        key: str,
        value: Mapping,
        mapper: DeclarativeMeta,
        select_stmt: Select
    ) -> Select:
        if self._is_self_method(method_name=key):
            return select_stmt.where(self._get_self_method_expression(
                lookup=key,
                value=value,
                mapper=mapper,
                select_stmt=select_stmt
            ))

        if self.is_related_field(mapper=mapper, relationship_name=key):
            related_mapper = self.get_related_mapper(
                mapper=mapper,
                relationship_name=key
            )
            return self._build(
                mapper=related_mapper,
                select_stmt=select_stmt,
                **value
            )

        if key == self.OR_LOOKUP:
            return self._bind_or_clause(
                mapper=mapper,
                select_stmt=select_stmt,
                **value
            )

        return self._bind_and_clause(
            mapper=mapper,
            select_stmt=select_stmt,
            **value
        )

    def _build(
        self,
        mapper: DeclarativeMeta,
        select_stmt: Optional[Select] = None,
        **filters
    ) -> Select:
        if select_stmt is None:
            select_stmt = self.select_stmt

        for key, value in filters.items():
            if isinstance(value, Mapping):
                select_stmt = self._handle_mapping_value(
                    key=key,
                    value=value,
                    mapper=mapper,
                    select_stmt=select_stmt
                )
                continue
            select_stmt = self._bind_expression(
                lookup=key,
                value=value,
                mapper=mapper,
                select_stmt=select_stmt
            )

        return select_stmt

    def build(
        self,
        mapper: Optional[DeclarativeMeta] = None,
        select_stmt: Optional[Select] = None,
        **filters
    ) -> Select:
        if mapper is None:
            mapper = self.mapper

        if select_stmt is None:
            select_stmt = self.select_stmt

        return self._build(
            mapper=mapper,
            select_stmt=select_stmt,
            **filters,
        )

    def _is_desc_order(
        self,
        order_by: str
    ) -> bool:
        *_, order_type = order_by.split(self.LOOKUP_STRING)
        return order_type == self.DESC_ORDER

    def _remove_order_type(
        self,
        order_by: str,
    ) -> str:
        *_, order_type = order_by.split(self.LOOKUP_STRING)
        return self.LOOKUP_STRING.join(_)

    def _bind_asc_order(
        self,
        order_by: str,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Select:
        pass

    def _bind_desc_order(
        self,
        order_by: str,
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ) -> Select:

    def _bind_order_by(
        self,
        order_by: Union[str, Iterable[str]],
        mapper: DeclarativeMeta,
        select_stmt: Select,
    ):
        if not isinstance(order_by, Iterable):
            if self._is_desc_order(order_by=order_by):
                return self._bind_desc_order(
                    order_by=
                )

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
        super().__init__(mapper=mapper)
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
