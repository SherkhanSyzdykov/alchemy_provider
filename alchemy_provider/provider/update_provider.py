from abc import abstractmethod
from typing import Any, Dict, Sequence, Optional, Union, Type
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty
from sqlalchemy.sql import update, Update
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery
from .base import BaseProvider
from .join_provider import JoinProvider


class UpdateProvider(JoinProvider, BaseProvider):
    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update_from_query(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_update_stmt(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_update_stmt_from_kwargs(self, *args, **kwargs):
        pass

    def _make_update_stmt(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
        returning: bool = True
    ) -> Update:
        update_stmt = update(mapper)
        update_stmt = self._bind_clause(
            clause=query.get_filters(),
            mapper=mapper,
            stmt=update_stmt,
            clause_binder=clause_binder
        )

        updatable_values = self.__make_updatable_values(
            query=query,
            mapper=mapper,
        )
        if not updatable_values:
            raise ValueError(
                'Attr values is empty'
            )

        update_stmt = update_stmt.values(**updatable_values)

        if returning:
            update_stmt = update_stmt.returning(mapper)

        return update_stmt

    @staticmethod
    def _query_from_kwargs(
        query: Union[Type[CRUDQuery], CRUDQuery],
        clause_binder: ClauseBinder,
        **kwargs
    ) -> CRUDQuery:
        result_query = query
        for field, value in kwargs.items():
            if clause_binder.LOOKUP_STRING in field:
                result_query = result_query.set_filters(**{field: value})
            else:
                result_query = result_query.set_values(**{field: value})

        return result_query

    def _make_update_stmt_from_kwargs(
        self,
        query: Union[Type[CRUDQuery], CRUDQuery],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
        returning: bool = True,
        **kwargs
    ) -> Update:
        query = self._query_from_kwargs(
            query=query,
            clause_binder=clause_binder,
            **kwargs
        )
        return self._make_update_stmt(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder,
            returning=returning
        )

    def __make_bulk_update_stmt(self):
        """
        Will be released in next version
        Use simple make_update_stmt for simple bulk_updates
        """
        raise NotImplementedError

    async def _update(
        self,
        query: Union[Type[CRUDQuery], CRUDQuery],
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
        returning: bool = True,
        **kwargs,
    ) -> Optional[Sequence[CRUDQuery]]:
        """
        Returns sequence of query instance if returning is True
        """
        update_stmt = self._make_update_stmt_from_kwargs(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder,
            returning=returning,
            **kwargs
        )

        scalar_result = await self._session.execute(update_stmt)

        if not returning:
            return

        return query.from_returning_mappers(scalar_result.all())

    async def _update_from_query(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
        returning: bool = True,
    ) -> Optional[Sequence[CRUDQuery]]:
        update_stmt = self._make_update_stmt(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder,
            returning=returning,
        )

        scalar_result = await self._session.execute(update_stmt)

        if not returning:
            return

        return query.from_returning_mappers(scalar_result.all())

    @staticmethod
    def __make_updatable_values(
        query: CRUDQuery,
        mapper: DeclarativeMeta
    ) -> Dict[str, Any]:
        updatable_values = dict()

        for field_name, value in query.get_values().items():
            mapper_field = getattr(mapper, field_name, None)
            if mapper_field is None:
                continue

            if not isinstance(mapper_field.property, ColumnProperty):
                continue

            updatable_values[field_name] = value

        return updatable_values
