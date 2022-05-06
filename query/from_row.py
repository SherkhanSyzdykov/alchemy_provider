from __future__ import annotations
from typing import List, Any, Dict
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import DeclarativeMeta
from .base import BaseQuery


FIELD_NAME_SEPARATOR = '__'


class FromRowQuery(BaseQuery):
    @classmethod
    def from_returning_mapper(
        cls,
        mapper: DeclarativeMeta
    ) -> BaseQuery:
        type_hints = cls.get_type_hints()
        query = cls()
        for field_name in type_hints.keys():
            setattr(query, field_name, getattr(mapper, field_name, None))

        return query

    @classmethod
    def from_returning_mappers(
        cls,
        mappers: List[DeclarativeMeta]
    ) -> List[BaseQuery]:
        queries = list()
        for mapper in mappers:
            query = cls.from_returning_mapper(mapper=mapper)
            queries.append(query)

        return queries

    @classmethod
    def _from_mapping(
        cls,
        mapping: Dict[str, Any]
    ) -> BaseQuery:
        query = cls()

        nested_mappings: Dict[str, Dict[str, Any]] = dict()

        for field, value in mapping.items():
            field_name, *deeper = field.split(FIELD_NAME_SEPARATOR)
            if not deeper:
                setattr(query, field_name, value)
                continue

            if field_name in nested_mappings:
                nested_mappings[field_name].update({
                    FIELD_NAME_SEPARATOR.join(deeper): value
                })
            else:
                nested_mappings[field_name] = {
                    FIELD_NAME_SEPARATOR.join(deeper): value
                }

        if not nested_mappings:
            return query

        for field_name, mapping in nested_mappings.items():
            nested_query = cls.get_field_query(field_name=field_name)
            nested_query = nested_query._from_mapping(mapping=mapping)
            setattr(query, field_name, nested_query)

        return query

    @classmethod
    def from_selected_row(
        cls,
        row: Row
    ) -> BaseQuery:
        return cls._from_mapping(mapping=dict(row))

    @classmethod
    def from_selected_rows(
        cls,
        rows: List[Row]
    ) -> List[BaseQuery]:
        queries = list()
        for row in rows:
            queries.append(cls.from_selected_row(row=row))

        return queries


a = {
    'id': 1,
    'name': 'some_name',
    'device_type__id': 'some_id',
    'device_type__name': 'some_name',
    'device_type__meter_inline__id': 3,
}

