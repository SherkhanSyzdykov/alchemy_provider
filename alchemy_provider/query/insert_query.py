from .base import BaseQuery
from .from_row import FromRowQuery
from .join_query import JoinQuery


class InsertQuery(FromRowQuery, JoinQuery, BaseQuery):
    pass
