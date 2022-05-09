from .base import BaseQuery
from .from_query import FromQuery
from .join_query import JoinQuery
from .pagination_query import PaginationQuery
from .sorting_query import SortingQuery


class SelectQuery(
    FromQuery,
    JoinQuery,
    PaginationQuery,
    SortingQuery,
    BaseQuery
):
    pass
