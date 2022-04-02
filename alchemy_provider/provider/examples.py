from __future__ import annotations
from abc import ABC
from dataclasses import dataclass, make_dataclass
from typing import Optional, Tuple, Type, Callable, Literal, Union, Dict, Any, get_type_hints
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import outerjoin, join, Join, ClauseElement
from sqlalchemy.sql.expression import FromClause
import json
from .models import *


@dataclass
class JoinStrategy:
    full: bool = False


class BaseQuery(ABC):
    __full_annotations = None

    class Meta(ABC):
        mapper: DeclarativeMeta

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def _from_row(
        cls,
        row: Tuple[Any],
    ) -> BaseQuery:
        full_annotations = cls.get_full_annotations()
        query_instance = cls()

        i = 0
        while i < len(row):
            for field in full_annotations.keys():
                if not cls.is_query_field(field=field):
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
    def get_fields_count(cls) -> int:
        return len(cls.get_full_annotations())

    @classmethod
    def from_row(cls, row: Tuple[Any]) -> BaseQuery:
        return cls._from_row(row=row)

    @classmethod
    def is_query_field(cls, field: str) -> bool:
        field_types = cls.get_field_types(field=field)
        for type_ in field_types:
            if issubclass(type_, BaseQuery):
                return True

        return False

    @classmethod
    def get_mapper(cls) -> DeclarativeMeta:
        return cls.Meta.mapper

    @classmethod
    def get_full_annotations(cls) -> Dict[str, Type]:
        if cls.__full_annotations is None:
            cls.__full_annotations = get_type_hints(cls)

        return cls.__full_annotations

    @classmethod
    def is_available_type(cls, field: str, type_: Type) -> bool:
        return type_ in cls.get_field_types(field=field)

    @classmethod
    def get_field_type(cls, field: str) -> Type:
        full_annotations = cls.get_full_annotations()
        if field in full_annotations:
            return full_annotations[field]

        return type(getattr(cls, field, Any))

    @classmethod
    def get_field_types(cls, field: str) -> Tuple[Type]:
        field_type = cls.get_field_type(field=field)
        return getattr(field_type, '__args__', (field_type, ))

    @classmethod
    def is_optional(cls, field: str) -> bool:
        return type(None) in cls.get_field_types(field=field)

    @classmethod
    def get_field_query(cls, field: str) -> Type[BaseQuery]:
        field_types = cls.get_field_types(field=field)
        for type_ in field_types:
            if issubclass(type_, BaseQuery):
                return type_

        raise  # TODO

    def set_certain_attr_feature(self, field_name, value):
        pass  # TODO


class MeterTypeQuery(BaseQuery):
    name: str
    description: str

    class Meta(BaseQuery.Meta):
        mapper = MeterTypeModel

    @property
    def name(self) -> int:
        try:
            return int(self.__name)
        except:
            return 0

    @name.setter
    def name(self, value: Any):
        self.__name = value


class ResourceQuery(BaseQuery):
    name: str

    class Meta(BaseQuery.Meta):
        mapper = ResourceModel


class MeterTypeResourcesQuery(MeterTypeQuery):
    resources: Tuple[ResourceQuery] = tuple()


class ResourceMeterTypesQuery(ResourceQuery):
    meter_types: Tuple[MeterTypeQuery] = tuple()


class MeterInlineQuery(BaseQuery):
    serial_number: str
    is_active: bool

    class Meta(BaseQuery.Meta):
        mapper = MeterInlineModel


class MeterInlineMeterTypeQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeQuery]


class MeterInlineMeterTypeResourcesQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeResourcesQuery] = None
