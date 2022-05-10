from uuid import UUID
from types import MappingProxyType
from typing import Any, Mapping, Callable, Optional, Union, Sequence, Literal
from sqlalchemy.orm import DeclarativeMeta, InstrumentedAttribute
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql import Select, Insert, Update, Delete
from sqlalchemy.sql.expression import BinaryExpression
from ..utils import is_relationship, get_column, is_column, AliasedManager
from .base import BaseClauseBinder


class StringClauseBuilder(BaseClauseBinder):
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

    _value_type = Union[
        int,
        float,
        str,
        bool,
        Sequence[int, float, str, bool],
    ]

    LOOKUP_OPERATORS: Mapping[
        str,
        Callable[[InstrumentedAttribute, _value_type], BinaryExpression]
    ] = MappingProxyType({
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

    @classmethod
    def get_lookup_operator(
        cls,
        lookup: str
    ) -> Callable[[InstrumentedAttribute, _value_type], BinaryExpression]:
        if lookup not in cls.LOOKUP_OPERATORS:
            raise KeyError(
                f'{lookup=} not in {cls.LOOKUP_OPERATORS.keys()}'
            )
        return cls.LOOKUP_OPERATORS.get(lookup)

    def _get_column(
        self,
        lookup: str,
        mapper: Union[DeclarativeMeta, AliasedClass],
        uuid: UUID,
    ) -> Optional[InstrumentedAttribute]:
        """
        lookup: meter_inline__directory__name__ilike: "%some_directory_name%"
        """
        lookup_parts = lookup.split(self.LOOKUP_STRING)
        for i, lookup_part in enumerate(lookup_parts):
            mapper_field = get_column(mapper=mapper, field_name=lookup_part)
            if mapper_field is None:
                return

            if is_column(mapper_field=mapper_field):
                return mapper_field

            if is_relationship(mapper_field=mapper_field):
                return self._get_column(
                    lookup=self.LOOKUP_STRING.join(lookup_parts[i+1:]),
                    mapper=AliasedManager.get_or_create(
                        mapper=mapper,
                        field_name=lookup_part,
                        uuid=uuid,
                    ),
                    uuid=uuid,
                )

    def _get_expression(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        uuid: UUID,
    ) -> Optional[BinaryExpression]:
        """
        """
        column = self._get_column(
            lookup=lookup,
            mapper=mapper,
            uuid=uuid,
        )
        if column is None:
            return

        operator_names = lookup.split(self.LOOKUP_STRING)
        if not operator_names:
            return

        operator_name = operator_names[-1]
        if operator_name not in self.LOOKUP_OPERATORS:
            operator_name = self.EQUAL_OPERATOR

        lookup_operator = self.get_lookup_operator(operator_name)

        if lookup_operator is None:
            return

        return lookup_operator(column, value)

    def _bind_string_expression_method(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete],
        uuid: UUID,
    ) -> Select:
        expression = self._get_expression(
            lookup=lookup,
            value=value,
            mapper=mapper,
            uuid=uuid,
        )
        if expression is None:
            return stmt

        return stmt.where(expression)
