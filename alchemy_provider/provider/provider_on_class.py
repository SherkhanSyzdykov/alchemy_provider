from typing import Type, Optional, Dict, Union, List, Tuple, Any
from sqlalchemy.sql import Select, select
from sqlalchemy.orm import ColumnProperty, RelationshipProperty
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession
from .examples import BaseQuery


class BaseProvider:
    _session: Union[async_scoped_session, AsyncSession]

    def __init__(
        self,
        session: Union[async_scoped_session, AsyncSession]
    ):
        self._session = session

    @staticmethod
    def join(
        select_stmt: Select,
        query: Type[BaseQuery],
        query_field: str,
    ) -> Select:
        mapper = query.get_mapper()
        mapper_field = getattr(mapper, query_field)

        select_stmt = select_stmt.join(
            mapper_field,
            isouter=query.is_optional(field=query_field),
            full=False  # TODO
        )
        return select_stmt


class Provider(BaseProvider):
    _query: Type[BaseQuery]

    def __init__(
        self,
        session: Union[async_scoped_session, AsyncSession],
        query: Type[BaseQuery]
    ):
        super().__init__(session=session)
        self._query = query

    @classmethod
    def get_query(cls) -> Type[BaseQuery]:
        return cls._query

    @classmethod
    def _build_select(
        cls,
        query: Optional[Type[BaseQuery]] = None,
        select_stmt: Optional[Select] = None
    ) -> Select:
        if query is None:
            query = cls.get_query()

        if select_stmt is None:
            select_stmt = select()

        mapper = query.get_mapper()
        annotations = query.get_full_annotations()

        for query_field in annotations:
            mapper_field = getattr(mapper, query_field, None)
            if mapper_field is None:
                raise  # TODO

            if isinstance(mapper_field.property, ColumnProperty):
                select_stmt = select_stmt.add_columns(mapper_field)

            if isinstance(mapper_field.property, RelationshipProperty):
                select_stmt = cls.join(
                    select_stmt=select_stmt,
                    query=query,
                    query_field=query_field,
                )
                select_stmt = cls._build_select(
                    select_stmt=select_stmt,
                    query=query.get_field_query(field=query_field)
                )

        return select_stmt

    @classmethod
    def get_select_stmt(
        cls,
        query: Type[BaseQuery]
    ) -> Select:
        return cls._build_select(query=query)

    @classmethod
    async def select(
        cls,
        query: Type[BaseQuery],
        session: Optional[Union[async_scoped_session, AsyncSession]] = None,
    ) -> List[BaseQuery]:
        if session is None:
            session = cls._session

        select_stmt = cls.get_select_stmt(query=query)
        rows: List[Tuple[Any]] = await session.execute(select_stmt)

        queries: List[BaseQuery] = []
        for row in rows:
            queries.append(
                query.from_row(row=row)
            )

        return queries


