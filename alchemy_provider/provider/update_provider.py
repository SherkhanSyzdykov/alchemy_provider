from abc import abstractmethod
from typing import Any, Dict, Sequence, Optional
from sqlalchemy.orm import DeclarativeMeta, ColumnProperty
from sqlalchemy.sql import update, Update
from query.update_query import UpdateQuery
from .base import BaseProvider
from .join_provider import JoinProvider


class UpdateProvider(JoinProvider, BaseProvider):
    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    def make_update_stmt(
        self,
        query: UpdateQuery,
        mapper: DeclarativeMeta,
        returning: bool = True
    ) -> Update:
        update_stmt = update(mapper)
        update_stmt = self._bind_clause(
            clause=query.get_filters(),
            mapper=mapper,
            stmt=update_stmt,
        )

        updatable_values = self.__make_updatable_values(
            query=query,
            mapper=mapper,
        )
        if not updatable_values:
            raise ValueError(
                'Attr values not empty'
            )

        update_stmt = update_stmt.values(**updatable_values)

        if returning:
            update_stmt = update_stmt.returning(mapper)

        return update_stmt

    def make_bulk_update_stmt(self):
        """
        Will be released in next version
        Use simple make_update_stmt for simple bulk_updates
        """
        raise NotImplementedError

    async def _update(
        self,
        query: UpdateQuery,
        mapper: DeclarativeMeta,
        returning: bool = True,
    ) -> Optional[Sequence[UpdateQuery]]:
        """
        Returns sequence of query instance if returning is True
        """
        update_stmt = self.make_update_stmt(
            query=query,
            mapper=mapper,
            returning=returning
        )

        # import pdb
        # pdb.set_trace()

        scalar_result = await self._session.execute(update_stmt)

        if not returning:
            return

        return query.from_returning_mappers(scalar_result.all())

    def __make_updatable_values(
        self,
        query: UpdateQuery,
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
