from abc import ABC
from .base import BaseQuery
from .from_row import FromRowQuery
from .join_query import JoinQuery
from .pagination_query import PaginationQuery
from .sorting_query import SortingQuery


class SelectQuery(
    ABC,
    FromRowQuery,
    JoinQuery,
    PaginationQuery,
    SortingQuery,
    BaseQuery
):
    pass
