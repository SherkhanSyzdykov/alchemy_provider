from abc import ABC
from dataclasses import dataclass, make_dataclass
from typing import Optional, Tuple, Type, Callable, Literal, Union
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import outerjoin, join, Join, ClauseElement
from sqlalchemy.sql.expression import FromClause
import json
from .models import *


@dataclass
class JoinStrategy:
    full: bool = False


class BaseQuery(ABC):
    class Meta(ABC):
        mapper: DeclarativeMeta

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # @staticmethod
    # @property
    # def get_meta(): -> Type[Meta]:
    #     return self._meta

    @classmethod
    def get_mapper(cls) -> DeclarativeMeta:
        return cls.Meta.mapper

    def set_certain_attr_feature(self, field_name, value):
        pass  # TODO


class MeterTypeQuery(BaseQuery):
    name: str
    description: str

    class Meta(BaseQuery.Meta):
        mapper = MeterTypeModel


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
    meter_type: Optional[MeterTypeQuery] = JoinStrategy(
        full=False
    )


class MeterInlineMeterTypeResourcesQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeResourcesQuery] = None