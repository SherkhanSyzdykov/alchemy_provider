from sqlalchemy.sql import Select
from query.pagination_query import PaginationQuery
from .base import BaseProvider


class PaginationProvider(BaseProvider):
    def bind_pagination(
        self,
        query: PaginationQuery,
        select_stmt: Select
    ) -> Select:
        return select_stmt.limit(query.limit).offset(query.offset)
