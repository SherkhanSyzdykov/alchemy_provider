from __future__ import annotations
from abc import abstractmethod
from typing import Union, Type, List, Optional
from sqlalchemy import select
from sqlalchemy.sql import Select, Insert
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty, \
    RelationshipProperty, InstrumentedAttribute
from query.base import BaseQuery
from query.from_row import FIELD_NAME_SEPARATOR
from query.select_query import SelectQuery
from utils import get_related_mapper
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

    def make_select_stmt(
        self,
        query: Union[Type[SelectQuery], SelectQuery],
        mapper: DeclarativeMeta
    ) -> Select:
        select_stmt = select()

        select_stmt = self._make_select_stmt(
            select_stmt=select_stmt,
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
                stmt=select_stmt
            )

        return select_stmt

    def make_select_from_insert(
        self,
        query: SelectQuery,
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

    def _make_column_label(
        self,
        mapper_field: InstrumentedAttribute,
        label_prefix: Optional[str] = None,
    ) -> str:
        if label_prefix is None:
            return mapper_field.name

        return label_prefix + FIELD_NAME_SEPARATOR + mapper_field.name

    def _make_select_stmt(
        self,
        select_stmt: Select,
        query: Union[Type[SelectQuery], SelectQuery],
        mapper: DeclarativeMeta,
        label_prefix: Optional[str] = None,
    ) -> Select:
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
                select_stmt = self._join(
                    field_name=field_name,
                    query=query,
                    stmt=select_stmt,
                    mapper=mapper,
                )
                select_stmt = self._make_select_stmt(
                    select_stmt=select_stmt,
                    query=query.get_field_query(field_name),
                    mapper=get_related_mapper(
                        mapper=mapper,
                        field_name=field_name,
                    ),
                    label_prefix=field_name
                )

        return select_stmt

    async def _select(
        self,
        query: Union[Type[SelectQuery], SelectQuery],
        mapper: DeclarativeMeta
    ) -> List[BaseQuery]:
        select_stmt = self.make_select_stmt(
            query=query,
            mapper=mapper
        )

        scalar_result = await self._session.execute(select_stmt)

        return query.from_selected_rows(rows=scalar_result.all())
