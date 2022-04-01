from abc import ABC
from dataclasses import dataclass
from typing import Tuple, Optional
from sqlalchemy.orm import DeclarativeMeta
from .models import *


@dataclass
class JoinStrategy:
    full: bool = False


@dataclass
class BaseQuery(ABC):
    class Meta(ABC):
        model: DeclarativeMeta

    @classmethod
    def get_model(cls) -> DeclarativeMeta:
        return cls.Meta.model

    def set_certain_attr_feature(self, field_name, value):
        pass  # TODO


class MeterTypeQuery(BaseQuery):
    name: str
    description: str

    class Meta(BaseQuery.Meta):
        model = MeterTypeModel


class ResourceQuery(BaseQuery):
    name: str

    class Meta(BaseQuery.Meta):
        model = ResourceModel


class MeterTypeResourcesQuery(MeterTypeQuery):
    resources: Tuple[ResourceQuery]


class ResourceMeterTypesQuery(ResourceQuery):
    meter_types: Tuple[MeterTypeQuery]


class MeterInlineQuery(BaseQuery):
    serial_number: str
    is_active: bool

    class Meta(BaseQuery.Meta):
        model = MeterInlineModel


class MeterInlineMeterTypeQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeQuery] = JoinStrategy(
        full=False
    )


class MeterInlineMeterTypeResourcesQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeResourcesQuery]
