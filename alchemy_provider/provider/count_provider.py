from abc import abstractmethod
from sqlalchemy import func, distinct
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import Select, select
from ..clause_binder import ClauseBinder
from ..query import CRUDQuery
from .select_provider import SelectProvider


class CountProvider(SelectProvider):
    @abstractmethod
    async def select_count(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_count_stmt(self, *args, **kwargs):
        pass

    def _make_count_stmt(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder
    ) -> Select:
        """
        select count(distinct alias1.id)
        from (
            select test.id as id, test.name as name,
            test2.id as test2_id, test2.test_id as test2_test_id
            from test join test2 on test.id = test2.test_id
            order by test.name, test2.id
        ) as alias1
        """
        select_stmt = self._make_select_stmt(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder
        )
        select_count_stmt = select(func.count()).select_from(select_stmt)

        subquery = select_stmt.subquery()
        for column in subquery.columns:
            if not (column.primary_key or column.unique):
                continue
            if not hasattr(mapper, column.name):
                continue

            select_count_stmt = select(func.count(distinct(column)))
            break

        return select_count_stmt

    async def _select_count(
        self,
        query: CRUDQuery,
        mapper: DeclarativeMeta,
        clause_binder: ClauseBinder,
    ) -> int:
        select_count_stmt = self._make_count_stmt(
            query=query,
            mapper=mapper,
            clause_binder=clause_binder,
        )

        return await self._session.scalar(select_count_stmt)
