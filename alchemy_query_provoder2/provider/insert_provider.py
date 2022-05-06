from abc import abstractmethod
from typing import Any, Optional, List, Mapping, Sequence
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty
from sqlalchemy.sql import insert, Insert
from query.insert_query import InsertQuery
from .base import BaseProvider


class InsertProvider(BaseProvider):
    @abstractmethod
    async def insert(self, *args, **kwargs):
        pass

    @abstractmethod
    async def bulk_insert(self, *args, **kwargs):
        pass

    def make_insert_stmt(
        self,
        query: InsertQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Insert:
        insert_stmt = insert(mapper)

        insertable_values = self.__make_insertable_values(
            query=query,
            mapper=mapper,
        )

        insert_stmt = insert_stmt.values(**insertable_values)

        if returning:
            insert_stmt = insert_stmt.returning(mapper)

        return insert_stmt

    def make_bulk_insert_stmt(
        self,
        queries: Sequence[InsertQuery],
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Insert:
        """
        """
        values_list: List[Mapping[str, Any]] = []

        for query in queries:
            insertable_values = self.__make_insertable_values(
                query=query,
                mapper=mapper
            )
            values_list.append(insertable_values)

        insert_stmt = insert(mapper)
        insert_stmt = insert_stmt.values(values_list)

        if returning:
            insert_stmt = insert_stmt.returning(mapper)

        return insert_stmt

    async def _insert(
        self,
        query: InsertQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[InsertQuery]:
        """
        if returning is True, returns instance of passed query
        """
        insert_stmt = self.make_insert_stmt(
            query=query,
            mapper=mapper,
            returning=returning
        )

        scalar_result = await self._session.execute(insert_stmt)

        if returning:
            return query.from_row(scalar_result.first())

    async def _bulk_insert(
        self,
        queries: Sequence[InsertQuery],
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[InsertQuery]]:
        """
        If returning is True, returns iterable object that contains
        InsertQuery
        """
        if not queries:
            return

        insert_stmt = self.make_bulk_insert_stmt(
            queries=queries,
            mapper=mapper,
            returning=returning
        )

        scalar_result = await self._session.execute(insert_stmt)

        if not returning:
            return

        query = queries[0]
        inserted_queries = list()

        for row in scalar_result:
            inserted_query = query.from_row(row)
            inserted_queries.append(inserted_query)

        return inserted_queries

    def __make_insertable_values(
        self,
        query: InsertQuery,
        mapper: DeclarativeMeta,
    ) -> Mapping[str, Any]:
        values = dict()

        for field_name, value in query.to_dict():
            mapper_field = getattr(mapper, field_name, None)

            if mapper_field is None:
                continue

            if mapper_field.property is not ColumnProperty:
                continue

            values[field_name] = value

        return values
