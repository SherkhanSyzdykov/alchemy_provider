from __future__ import annotations
from abc import ABC
from typing import Any, Dict
from .base import BaseQuery
from .from_row import FromRowQuery
from .join_query import JoinQuery


class UpdateQuery(ABC, FromRowQuery, JoinQuery, BaseQuery):
    filters: Dict[str, Any] = dict()
    values: Dict[str, Any] = dict()

    def set_filters(
        self,
        **kwargs
    ) -> UpdateQuery:
        self.filters = dict()

        for item, value in kwargs.items():
            self.filters[item] = value

        return self

    def set_values(
        self,
        **kwargs,
    ) -> UpdateQuery:
        self.values = dict()
        for item, value in kwargs.items():
            self.values[item] = value

        return self
