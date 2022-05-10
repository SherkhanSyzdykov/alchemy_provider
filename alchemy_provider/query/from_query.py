from __future__ import annotations
from typing import List, Any, Dict, Optional
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import DeclarativeMeta
from ..utils import run_concurrently
from .adapter_field import AdapterField
from .base import BaseQuery


FIELD_NAME_SEPARATOR = '__'


class FromQuery(BaseQuery):
    @staticmethod
    async def _set_attr(
        query: BaseQuery,
        field_name: str,
        value: Any
    ):
        query_class = query.get_class()
        adapter_field: Optional[AdapterField] = getattr(
            query_class, field_name, None
        )
        if adapter_field is None:
            setattr(query, field_name, value)
            return

        setattr(query, field_name, await adapter_field(value))

    @classmethod
    async def from_mapper(
        cls,
        mapper: DeclarativeMeta
    ) -> BaseQuery:
        type_hints = cls.get_type_hints()
        query = cls()
        set_attr_coroutines = list()
        for field_name in type_hints.keys():
            set_attr_coroutines.append(
                cls._set_attr(
                    query=query,
                    field_name=field_name,
                    value=getattr(mapper, field_name, None)
                )
            )

        await run_concurrently(*set_attr_coroutines)

        return query

    @classmethod
    async def from_mappers(
        cls,
        mappers: List[DeclarativeMeta]
    ) -> List[BaseQuery]:
        coroutines = list()
        for mapper in mappers:
            coroutines.append(cls.from_mapper(mapper=mapper))

        queries: List[BaseQuery] = await run_concurrently(*coroutines)

        return queries

    @classmethod
    async def _from_mapping(
        cls,
        mapping: Dict[str, Any]
    ) -> BaseQuery:
        query = cls()

        nested_mappings: Dict[str, Dict[str, Any]] = dict()

        set_attr_coroutines = list()

        for field, value in mapping.items():
            field_name, *deeper = field.split(FIELD_NAME_SEPARATOR)
            if not deeper:
                set_attr_coroutines.append(
                    cls._set_attr(
                        query=query,
                        field_name=field_name,
                        value=value
                    )
                )
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
            nested_query = await nested_query._from_mapping(mapping=mapping)
            setattr(query, field_name, None)
            for value in nested_query.dict.values():
                if value is not None:
                    setattr(query, field_name, nested_query)
                    break

        await run_concurrently(*set_attr_coroutines)

        return query

    @classmethod
    async def from_selected_row(
        cls,
        row: Row
    ) -> BaseQuery:
        return await cls._from_mapping(mapping=dict(row))

    @classmethod
    async def from_selected_rows(
        cls,
        rows: List[Row]
    ) -> List[BaseQuery]:
        coroutines = list()
        for row in rows:
            coroutines.append(cls.from_selected_row(row=row))

        queries = await run_concurrently(*coroutines)

        return queries
