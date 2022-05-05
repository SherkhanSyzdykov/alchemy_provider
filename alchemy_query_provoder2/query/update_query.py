from __future__ import annotations
from abc import ABC
from typing import Any, Dict, Sequence, Union, Optional
from .from_row import FromRowQuery
from .join_query import JoinQuery


class UpdateQuery(ABC, FromRowQuery, JoinQuery):
    filters: Dict[str, Any] = dict()
    values: Union[Dict[str, Any], Sequence[Dict[str, Any]]] = dict()

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
        values: Optional[Sequence[Dict[str, Any]]] = None,
        **kwargs,
    ) -> UpdateQuery:
        if values is not None:
            self.values = values
            return self

        self.values = dict()
        for item, value in kwargs.items():
            self.values[item] = value

        return self
