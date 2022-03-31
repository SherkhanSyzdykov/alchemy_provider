from abc import ABC
from dataclasses import dataclass, make_dataclass
from typing import Optional, Tuple, Type
from sqlalchemy.orm import DeclarativeMeta
import json
from .models import *


class BaseQuery(ABC):
    class Meta(ABC):
        model: DeclarativeMeta

    _meta: Type[Meta] = Meta

    def __init__(self, **kwargs):
        self._meta = self.Meta

        for key, value in kwargs.items():
            if key in self.__annotations__:
                assert type(value) in self.__annotations__[key].__args__

            setattr(self, key, value)

    @property
    def get_meta(self) -> Type[Meta]:
        return self._meta

    @property
    def get_model(self) -> DeclarativeMeta:
        return self.get_meta.model

    def set_certain_attr_feature(self, field_name, value):
        pass  # TODO


class MeterTypeQuery(BaseQuery):
    name: str

    class Meta(BaseQuery.Meta):
        model = MeterTypeModel


class ResourceQuery(BaseQuery):
    name: str

    class Meta(BaseQuery.Meta):
        model = ResourceModel


class MeterTypeResourcesQuery(MeterTypeQuery):
    resources: Tuple[ResourceQuery] = tuple()


class ResourceMeterTypesQuery(ResourceQuery):
    meter_types: Tuple[MeterTypeQuery] = tuple()


class MeterInlineQuery(BaseQuery):
    serial_number: str
    is_active: bool

    class Meta(BaseQuery.Meta):
        model = MeterInlineModel


class MeterInlineMeterTypeQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeQuery] = None


class MeterInlineMeterTypeResourcesQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeResourcesQuery] = None
