from __future__ import annotations
from abc import ABC
from typing import Any, Tuple
from .base import BaseQuery


class FromRowQuery(ABC, BaseQuery):
    @classmethod
    def _from_row(
        cls,
        row: Tuple[Any],
    ) -> BaseQuery:
        type_hints = cls.get_type_hints()
        query_instance = cls()

        i = 0
        while i < len(row):
            for field in type_hints.keys():
                if not cls._is_query_field(field=field):
                    setattr(query_instance, field, row[i])
                    i += 1
                    continue

                nested_query = cls.get_field_query(field=field)
                nested_query_fields_count = cls.get_fields_count()
                nested_query_instance = nested_query._from_row(
                    row[i: i + nested_query_fields_count]
                )
                setattr(query_instance, field, nested_query_instance)
                i += nested_query_fields_count

        return query_instance

    @classmethod
    def from_row(
        cls,
        row: Tuple[Any]
    ) -> BaseQuery:
        class_ = cls
        if isinstance(cls, BaseQuery):
            class_ = cls.__class__

        return class_._from_row(row=row)
