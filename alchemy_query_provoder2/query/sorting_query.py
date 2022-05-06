from typing import Optional, Literal
from .base import BaseQuery


class SortingQuery(BaseQuery):
    order_by: Optional[str] = None
    reversed: bool = False
    nulls_place: Literal['first', 'last', None] = None
