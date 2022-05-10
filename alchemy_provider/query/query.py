from __future__ import annotations
from abc import ABC
from .base import BaseQuery
from .select_query import SelectQuery
from .insert_query import InsertQuery
from .update_query import UpdateQuery
from .delete_query import DeleteQuery


class AbstractQuery(
    ABC,
    SelectQuery,
    InsertQuery,
    UpdateQuery,
    DeleteQuery,
    BaseQuery
):
    pass
