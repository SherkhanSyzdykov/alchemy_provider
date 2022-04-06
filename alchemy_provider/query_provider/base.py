from abc import ABC, abstractmethod
from typing import Union, Type, Optional, List, Any, Tuple
from sqlalchemy.sql import Select, select
from sqlalchemy.orm import ColumnProperty, RelationshipProperty
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from alchemy_provider.provider import BaseProvider
from alchemy_provider.query import BaseQuery


class BaseQueryProvider(ABC, BaseProvider):
    _query: Optional[Union[Type[BaseQuery], BaseQuery]] = None

    def __init__(
        self,
        session: Union[AsyncSession, async_scoped_session],
        query: Optional[Union[Type[BaseQuery], BaseQuery]] = None,
    ):
        super().__init__(session=session)
        self._query = query

    @property
    def query(self) -> Union[Type[BaseQuery], BaseQuery]:
        if self._query is None:
            raise  # TODO
        return self._query

    @query.setter
    def query(
        self,
        value: Union[Type[BaseQuery], BaseQuery]
    ):
        self._query = value

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

    @staticmethod
    def build_select_stmt(
        query: Union[Type[BaseQuery], BaseQuery],
        select_stmt: Optional[Select] = None,
    ) -> Select:
        query = query.get_class()

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
                select_stmt = BaseQueryProvider.join(
                    select_stmt=select_stmt,
                    query=query,
                    query_field=query_field,
                )
                select_stmt = BaseQueryProvider.build_select_stmt(
                    query=query.get_field_query(field=query_field),
                    select_stmt=select_stmt,
                )

        return select_stmt

    @property
    def select_stmt(self) -> Select:
        return self.build_select_stmt(query=self.query)

    # @abstractmethod
    # async def get_row(self, *args, **kwargs) -> Tuple[Any]:
    #     pass
    #
    # @abstractmethod
    # async def select_row(self, *args, **kwargs) -> List[Tuple[Any]]:
    #     pass
    #
    # @property
    # async def get(self) -> BaseQuery:
    #     row = await self.get_row
    #     return self.query.from_row(row=row)
    #
    # @property
    # async def select(self) -> List[BaseQuery]:
    #     select_stmt = self.select_stmt
    #     scalar_result = await self._session.execute(select_stmt)
    #
    #     queries: List[BaseQuery] = []
    #     for row in scalar_result:
    #         queries.append(
    #             self.query.from_row(row=row)
    #         )
    #
    #     return queries


class BaseQueryTypeProvider(ABC, BaseQueryProvider):
    _query: Type[BaseQuery]

    @BaseQueryProvider.query.setter
    def query(self, value: Type[BaseQuery]):
        if not issubclass(value, BaseQuery):
            raise  # TODO

        self._query = value


class BaseQueryInstanceProvider(ABC, BaseQueryProvider):
    _query: BaseQuery

    @BaseQueryProvider.query.setter
    def query(self, value: BaseQuery):
        if not isinstance(value, BaseQuery):
            raise  # TODO

        self._query = value
