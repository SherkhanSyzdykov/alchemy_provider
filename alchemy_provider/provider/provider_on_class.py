from typing import Type, Optional, Dict
from sqlalchemy.sql import Select, select
from sqlalchemy.orm import ColumnProperty, RelationshipProperty
from .examples import BaseQuery


class BaseProvider:
    @staticmethod
    def get_full_annotations(
        query: Type[BaseQuery]
    ) -> Dict[str, Type]:
        annotations = query.__annotations__
        bases = query.__bases__
        for base in bases:
            if not issubclass(base, BaseQuery):
                continue

            for field, annotation in base.__annotations__.items():
                if field not in annotations:
                    annotations[field] = annotation

        return annotations

    @staticmethod
    def is_optional(field_type: Type) -> bool:
        available_types = getattr(field_type, '__args__', (field_type,))
        return type(None) in available_types

    @staticmethod
    def join(
        select_stmt: Select,
        query: Type[BaseQuery],
        query_field: str,
    ) -> Select:
        field_type = BaseProvider.get_full_annotations(query=query)[query_field]
        mapper = query.get_mapper()
        mapper_field = getattr(mapper, query_field)

        select_stmt = select_stmt.join(
            mapper_field,
            isouter=BaseProvider.is_optional(field_type),
            full=False  # TODO
        )
        return select_stmt

class Provider(BaseProvider):
    _query: Type[BaseQuery]
    _full_annotations: Optional[Dict[str, Type]] = None

    def __init__(
        self,
        query: Type[BaseQuery]
    ):
        self._query = query

    def get_query(self) -> Type[BaseQuery]:
        return self._query

    def _get_full_annotations(
        self,
    ) -> Dict[str, Type]:
        if self._full_annotations is not None:
            return self._full_annotations

        self._full_annotations = self.get_full_annotations(
            query=self.get_query()
        )

        return self._full_annotations

    def _build_select(
        self,
        query: Optional[Type[BaseQuery]] = None,
        select_stmt: Optional[Select] = None
    ) -> Select:
        if query is None:
            query = self.get_query()

        if select_stmt is None:
            select_stmt = select()

        mapper = query.get_mapper()
        annotations = self.get_full_annotations(query=query)

        for query_field in annotations:
            mapper_field = getattr(mapper, query_field, None)
            if mapper_field is None:
                raise  # TODO

            if isinstance(mapper_field.property, ColumnProperty):
                select_stmt = select_stmt.add_columns(mapper_field)

            if isinstance(mapper_field.property, RelationshipProperty):
                select_stmt = self.join(
                    select_stmt=select_stmt,
                    query=query,
                    query_field=query_field,
                )
                select_stmt = ''

        return select_stmt





    @staticmethod
    def select(
        query: Type[BaseQuery]
    ) -> BaseQuery:
        pass
