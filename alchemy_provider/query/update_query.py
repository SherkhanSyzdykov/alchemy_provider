from __future__ import annotations
from typing import Any, Dict
from copy import deepcopy
from utils import cls_or_ins
from .base import BaseQuery
from .from_row import FromRowQuery
from .join_query import JoinQuery


class UpdateQuery(FromRowQuery, JoinQuery, BaseQuery):
    _values: Dict[str, Any] = dict()

    @classmethod
    def get_values(cls) -> Dict[str, Any]:
        return deepcopy(cls._values)

    @cls_or_ins
    def set_values(cls_or_ins, **kwargs) -> BaseQuery:
        self = cls_or_ins
        if cls_or_ins.is_class():
            self = cls_or_ins()

        self._set_values(self._values, **kwargs)

        return self
