from abc import ABC
from typing import Optional
from .base import BaseQuery


class PaginationQuery(ABC, BaseQuery):
    limit: Optional[int] = None
    offset: Optional[int] = None
