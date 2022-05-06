from abc import abstractmethod
from typing import Dict, Any, Optional, Union, Sequence
from sqlalchemy import and_, or_
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, Insert, Update, Delete
from sqlalchemy.sql.expression import BinaryExpression
from utils import is_relationship, get_column, get_related_mapper


class BaseClauseBinder:
    LOOKUP_STRING = '__'
    OR_OPERATOR = '_or_'
    AND_OPERATOR = '_and_'

    @abstractmethod
    def bind(self, *args, **kwargs):
        pass

    @abstractmethod
    def _is_self_method(
        self,
        lookup: str
    ):
        pass

    @abstractmethod
    def _bind_self_method(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete],
    ) -> Select:
        pass

    @abstractmethod
    def _bind_string_expression_method(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete],
    ) -> Select:
        pass

    @abstractmethod
    def _get_expression(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
    ):
        pass

    def _bind(
        self,
        clause: Dict[str, Any],
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete]
    ) -> Select:
        for lookup, value in clause.items():
            stmt = self._bind_expressions(
                lookup=lookup,
                value=value,
                mapper=mapper,
                stmt=stmt
            )

        return stmt

    def _bind_expressions(
        self,
        lookup: str,
        value: Any,
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete],
    ) -> Select:
        if self._is_self_method(lookup=lookup):
            return self._bind_self_method(
                lookup=lookup,
                value=value,
                mapper=mapper,
                stmt=stmt
            )

        if type(value) is dict:
            stmt = self._bind_dict_value(
                lookup=lookup,
                value=value,
                mapper=mapper,
                stmt=stmt
            )

        return self._bind_string_expression_method(
            lookup=lookup,
            value=value,
            mapper=mapper,
            stmt=stmt
        )

    def _bind_dict_value(
        self,
        lookup: str,
        value: Dict[str, Any],
        mapper: DeclarativeMeta,
        stmt: Union[Select, Insert, Update, Delete]
    ) -> Select:
        expression = self._get_dict_expression(
            lookup=lookup,
            value=value,
            mapper=mapper
        )
        if expression is None:
            return stmt

        if isinstance(expression, Sequence):
            return stmt.where(*expression)

        return stmt.where(expression)

    def _get_dict_expression(
        self,
        lookup: str,
        value: Dict[str, Any],
        mapper: DeclarativeMeta,
    ) -> Optional[Union[BinaryExpression, Sequence[BinaryExpression]]]:
        if lookup in (self.AND_OPERATOR, self.OR_OPERATOR) \
                and type(value) is not dict:
            raise ValueError(
                f'If lookup in {(self.AND_OPERATOR, self.OR_OPERATOR)}, so'
                f'value have to be dict'
            )

        if lookup == self.OR_OPERATOR:
            return self._get_or_expression(
                clause=value,
                mapper=mapper,
            )

        if lookup == self.AND_OPERATOR:
            return self._get_and_expression(
                clause=value,
                mapper=mapper,
            )

        column = get_column(mapper=mapper, field_name=lookup)
        if column is not None:
            if is_relationship(mapper_field=column):
                return self._get_expressions(
                    clause=value,
                    mapper=get_related_mapper(mapper=mapper, field_name=lookup),
                )

    def _get_or_expression(
        self,
        clause: Dict[str, Any],
        mapper: DeclarativeMeta,
    ) -> BinaryExpression:
        expressions = self._get_expressions(
            clause=clause,
            mapper=mapper,
        )
        return or_(*expressions)

    def _get_and_expression(
        self,
        clause: Dict[str, Any],
        mapper: DeclarativeMeta,
    ) -> BinaryExpression:
        expressions = self._get_expressions(
            clause=clause,
            mapper=mapper,
        )
        return and_(*expressions)

    def _get_expressions(
        self,
        clause: Dict[str, Any],
        mapper: DeclarativeMeta,
    ) -> Sequence[BinaryExpression]:
        expressions = []
        for lookup, value in clause.items():
            if type(value) is dict:
                expressions.append(self._get_dict_expression(
                    value=clause,
                    mapper=mapper
                ))
                continue

            expressions.append(self._get_expression(
                lookup=lookup,
                value=value,
                mapper=mapper
            ))

        return expressions
