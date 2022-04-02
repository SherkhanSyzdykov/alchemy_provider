from typing import Type, Union, TypedDict, is_typeddict, Dict, Any
from types import UnionType
from sqlalchemy import *
from sqlalchemy.sql import Select
from sqlalchemy.orm import DeclarativeMeta, RelationshipProperty, ColumnProperty
from alchemy_provider.provider.examples import *
from alchemy_provider.provider.provider_on_class import *



class ModelAttributeException(BaseException):
    ...


{
    'serial_number__in': ['dfsdf', 'asdfsdf'],
    'is_active': '__all__',
    'meter_type': {
        '__or__': {
            'name__ilike': '%dsf%',
            'description': 'dfsdf'
        }
    }
}


class BaseQueryTypeProvider:
    _query: Type[BaseQuery]

    def __init__(self,query: Type[BaseQuery]):
        self._query = query

    @property
    def get_query(self) -> Type[BaseQuery]:
        return self._query

    def _get_available_types_of_field(
        self,
        query: Type[BaseQuery],
        field: str
    ) -> Tuple[Any]:
        annotation = query.__annotations__[field]
        return getattr(annotation, '__args__', (annotation,))

    def _join_base_query_type(
        self,
        select_stmt: Select,
        query: Type[BaseQuery],
        field: str,
    ) -> Select:
        join_strategy = getattr(query, field, JoinStrategy)
        model_field = getattr(query.get_model(), field)

        is_outer = False

        available_types = self._get_available_types_of_field(
            query=query,
            field=field,
        )
        if type(None) in available_types:
            is_outer = True

        stmt = select_stmt.join(
            model_field,
            is_outer=is_outer,
            full=join_strategy.full
        )
        return stmt

    def _get_base_query_subtype(
        self,
        query: Type[BaseQuery],
        field: str
    ) -> Type[BaseQuery]:
        available_types = self._get_available_types_of_field(
            query=query,
            field=field,
        )
        for type_ in available_types:
            if issubclass(type_, BaseQuery):
                return type_

    def _make_select_stmt_from_base_query_type(
        self,
        query: Optional[Type[TypedDict]] = None,
        select_stmt: Optional[Select] = None
    ) -> Select:
        """
        query: subclass of typing.TypedDict
        example:
        class Test(typing.TypedDict):
            name: str
            test: bool
        """
        if query is None:
            query = self.get_query

        model = query.get_model()

        stmt = select_stmt
        if select_stmt is None:
            stmt = select()

        for field in self.get_query.__annotations__:
            model_field = getattr(model, field, None)
            if isinstance(model_field.property, ColumnProperty):
                stmt = stmt.add_columns(model_field)
                continue

            if isinstance(model_field.property, RelationshipProperty):
                stmt = self._join_base_query_type(
                    select_stmt=stmt,
                    query=query,
                    field=field,
                )
                stmt = self._make_select_stmt_from_base_query_type(
                    query=self._get_base_query_subtype(
                        query=query,
                        field=field
                    ),
                    select_stmt=stmt,
                )
                continue

            raise  # TODO

        return stmt


class QueryInstanceProvider:
    _query: BaseQuery

    def __init__(
        self,
        query: BaseQuery
    ):
        self._query = query

    @property
    def get_query(self) -> BaseQuery:
        return self._query

    def _make_select_stmt_by_query_instance(
        self,
        query: Optional[BaseQuery] = None,
        select_stmt: Optional[Select] = None
    ) -> Select:
        if query is None:
            query = self.get_query

        model = query.get_model()

        stmt = select_stmt
        if select_stmt is None:
            stmt = select()


class DictProvider:
    _query: Dict[str, Any]

    def __init__(
        self,
        query: Dict[str, Any]
    ):
        self._query = query

    @property
    def get_query(self) -> Dict[str, Any]:
        return self._query

    def _make_select_stmt_by_query_instance(
        self,
        query: Optional[Dict[str, Any]] = None,
        select_stmt: Optional[Select] = None,
    ) -> Select:
        if query is None:
            query = self.get_query

        model = query.get_model()

        stmt = select_stmt
        if select_stmt is None:
            stmt = select()


