from abc import ABC
from .from_row import FromRowQuery
from .join_query import JoinQuery


class SelectQuery(ABC, FromRowQuery, JoinQuery):
    pass
