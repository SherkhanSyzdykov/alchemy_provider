from abc import ABC
from .base import BaseQuery
from .join_query import JoinQuery


class DeleteQuery(ABC, JoinQuery, BaseQuery):
    pass
