from __future__ import annotations
from abc import abstractmethod
from typing import Union, Type, List, Optional
from sqlalchemy import select
from sqlalchemy.sql import Select, Insert
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty, \
    RelationshipProperty, InstrumentedAttribute
from sqlalchemy.orm.util import AliasedClass
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery, FIELD_NAME_SEPARATOR
from ..utils import AliasedManager
from .base import BaseProvider
from .join_provider import JoinProvider
from .pagination_provider import PaginationProvider
from .sorting_provider import SortingProvider


class SelectProvider(
    JoinProvider,
    PaginationProvider,
    SortingProvider,
    BaseProvider
):
    @abstractmethod
    async def select(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_select_stmt(self, *args, **kwargs):
        pass

    def _make_select_stmt(
        self,
        query: Union[Type[CRUDQuery], CRUDQuery],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder
    ) -> Select:
        select_stmt = self._make_simple_select_stmt(
            query=query,
            mapper=mapper
        )

        select_stmt = self.bind_pagination(
            query=query,
            select_stmt=select_stmt
        )

        select_stmt = self.bind_sorting(
            query=query,
            mapper=mapper,
            select_stmt=select_stmt,
        )

        if query.is_instance():
            select_stmt = self._bind_clause(
                clause=query.get_filters(),
                mapper=mapper,
                stmt=select_stmt,
                clause_binder=clause_binder
            )

        AliasedManager.delete(id(select_stmt))

        return select_stmt

    def __make_select_from_insert(
        self,
        query: CRUDQuery,
        insert_stmt: Insert
    ) -> Select:
        """
        Will be added in future version

        with inserted as (
            insert intoROW_MAP_FORMAT.format(
                        query.get_name(), field_name
                    ) test2(name, description, test_id) values
            ('test2_name1', 'test2_description1', 1)
            returning *
        )
        select inserted.*, test.*
        from inserted left outer join test on inserted.test_id = test.id
        """
        raise NotImplementedError

    def _make_simple_select_stmt(
        self,
        query: Type[CRUDQuery],
        mapper: Union[DeclarativeMeta, AliasedClass],
        label_prefix: Optional[str] = None,
        select_stmt: Optional[Select] = None,
    ) -> Select:

        if select_stmt is None:
            select_stmt = select()

        type_hints = query.get_type_hints()

        for field_name, type_hint in type_hints.items():
            mapper_field = getattr(mapper, field_name, None)
            if mapper_field is None:
                continue

            if isinstance(mapper_field.property, ColumnProperty):
                select_stmt = select_stmt.add_columns(
                    mapper_field.label(
                        self._make_column_label(
                            mapper_field=mapper_field,
                            label_prefix=label_prefix
                        )
                    )
                )
                continue

            if isinstance(mapper_field.property, RelationshipProperty):
                aliased_mapper = AliasedManager.get_or_create(
                    stmt_id=id(select_stmt),
                    mapper=mapper,
                    field_name=field_name
                )

                select_stmt = self._join(
                    field_name=field_name,
                    query=query,
                    stmt=select_stmt,
                    mapper=mapper,
                    aliased_mapper=aliased_mapper,
                )

                select_stmt = self._make_simple_select_stmt(
                    select_stmt=select_stmt,
                    query=query.get_field_query(field_name),
                    mapper=aliased_mapper,
                    label_prefix=field_name
                )

        return select_stmt

    @staticmethod
    def _make_column_label(
        mapper_field: InstrumentedAttribute,
        label_prefix: Optional[str] = None,
    ) -> str:
        if label_prefix is None:
            return mapper_field.name

        return label_prefix + FIELD_NAME_SEPARATOR + mapper_field.name

    async def _select(
        self,
        query: Union[Type[CRUDQuery], CRUDQuery],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder
    ) -> List[CRUDQuery]:
        select_stmt = self._make_select_stmt(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder
        )

        scalar_result = await self._session.execute(select_stmt)

        return query.from_selected_rows(rows=scalar_result.all())
