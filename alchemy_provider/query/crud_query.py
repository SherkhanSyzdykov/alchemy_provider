from __future__ import annotations
from typing import Type, List
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import DeclarativeMeta
from .base import BaseQuery
from .select_query import SelectQuery
from .insert_query import InsertQuery
from .update_query import UpdateQuery
from .delete_query import DeleteQuery


class CRUDQuery(
    InsertQuery,
    SelectQuery,
    UpdateQuery,
    DeleteQuery,
    BaseQuery
):
    pass

    @classmethod
    def get_field_query(cls, field_name: str) -> Type[CRUDQuery]:
        return super().get_field_query(field_name=field_name)

    @classmethod
    def from_returning_mapper(
        cls,
        mapper: DeclarativeMeta
    ) -> CRUDQuery:
        return super().from_returning_mapper(mapper=mapper)

    @classmethod
    def from_returning_mappers(
        cls,
        mappers: List[DeclarativeMeta]
    ) -> List[CRUDQuery]:
        return super().from_returning_mappers(mappers=mappers)

    @classmethod
    def from_selected_row(
        cls,
        row: Row
    ) -> CRUDQuery:
        return super().from_selected_row(row=row)

    @classmethod
    def from_selected_rows(
        cls,
        rows: List[Row]
    ) -> List[CRUDQuery]:
        return super().from_selected_rows(rows=rows)
