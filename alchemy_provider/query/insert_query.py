from .base import BaseQuery
from .from_query import FromQuery
from .join_query import JoinQuery


class InsertQuery(FromQuery, JoinQuery, BaseQuery):
    pass
