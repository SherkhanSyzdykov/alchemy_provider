from abc import ABC
from .join_query import JoinQuery


class DeleteQuery(ABC, JoinQuery):
    pass
