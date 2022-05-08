from abc import abstractmethod
from typing import Any, Optional, List, Mapping, Sequence, Type, Union, Dict
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty
from sqlalchemy.sql import insert, Insert
from ..query import CRUDQuery
from .base import BaseProvider


class InsertProvider(BaseProvider):
    @abstractmethod
    async def insert(self, *args, **kwargs):
        pass

    @abstractmethod
    async def bulk_insert(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_insert_stmt(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_bulk_insert_stmt(self, *args, **kwargs):
        pass

    def _make_insert_stmt(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Insert:
        insert_stmt = insert(mapper)

        insertable_values = self.__make_insertable_values(
            mapper=mapper,
            values=query.dict,
        )

        insert_stmt = insert_stmt.values(**insertable_values)

        if returning:
            insert_stmt = insert_stmt.returning(mapper)

        return insert_stmt

    def _make_bulk_insert_stmt(
        self,
        values_seq: Sequence[Dict[str, Any]],
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Insert:
        """
        """
        insertable_values_seq: List[Mapping[str, Any]] = []

        for values in values_seq:
            insertable_values = self.__make_insertable_values(
                mapper=mapper,
                values=values
            )
            insertable_values_seq.append(insertable_values)

        insert_stmt = insert(mapper)
        insert_stmt = insert_stmt.values(insertable_values_seq)

        if returning:
            insert_stmt = insert_stmt.returning(mapper)

        return insert_stmt

    async def _insert(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[CRUDQuery]:
        """
        if returning is True, returns instance of passed query
        """
        insert_stmt = self._make_insert_stmt(
            query=query,
            mapper=mapper,
            returning=returning
        )

        scalar_result = await self._session.execute(insert_stmt)

        if returning:
            return query.from_returning_mapper(scalar_result.first())

    async def _bulk_insert(
        self,
        query: Union[CRUDQuery, Type[CRUDQuery]],
        values_seq: Sequence[Dict[str, Any]],
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[CRUDQuery]]:
        """
        If returning is True, returns iterable object that contains
        CRUDQuery
        """
        if not values_seq:
            return

        insert_stmt = self.make_bulk_insert_stmt(
            query=query,
            values_seq=values_seq,
            mapper=mapper,
            returning=returning
        )

        scalar_result = await self._session.execute(insert_stmt)

        if returning:
            return query.from_returning_mappers(scalar_result.all())

    @staticmethod
    def __make_insertable_values(
        mapper: DeclarativeMeta,
        values: Dict[str, Any],
    ) -> Mapping[str, Any]:
        insertable_values = dict()

        for field_name, value in values.items():
            mapper_field = getattr(mapper, field_name, None)

            if mapper_field is None:
                continue

            if not isinstance(mapper_field.property, ColumnProperty):
                continue

            insertable_values[field_name] = value

        return insertable_values
