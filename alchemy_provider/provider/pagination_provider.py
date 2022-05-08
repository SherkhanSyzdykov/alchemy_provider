from sqlalchemy.sql import Select
from ..query import CRUDQuery
from .base import BaseProvider


class PaginationProvider(BaseProvider):
    def bind_pagination(
        self,
        query: CRUDQuery,
        select_stmt: Select
    ) -> Select:
        return select_stmt.limit(query.limit).offset(query.offset)
