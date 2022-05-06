from typing import Optional
from .base import BaseQuery


class PaginationQuery(BaseQuery):
    limit: Optional[int] = None
    offset: Optional[int] = None
