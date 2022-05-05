from abc import ABC
from .base import BaseQuery
from .from_row import FromRowQuery
from .join_query import JoinQuery


class InsertQuery(ABC, FromRowQuery, JoinQuery, BaseQuery):
    pass
