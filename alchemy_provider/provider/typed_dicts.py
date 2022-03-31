from typing import Optional, Tuple, TypedDict
from .models import *


class BaseQuery(TypedDict):
    class Meta:
        pass

    _meta = Meta


class MeterTypeQuery(TypedDict):
    name: str

    class Meta:
        model = MeterTypeModel


class ResourceQuery(TypedDict):
    name: str

    class Meta:
        model = ResourceModel


class MeterTypeResourcesQuery(MeterTypeQuery):
    resources: Tuple[ResourceQuery]


class ResourceMeterTypesQuery(ResourceQuery):
    meter_types: Tuple[MeterTypeQuery]


class MeterInlineQuery(TypedDict):
    serial_number: str
    is_active: bool

    class Meta:
        model = MeterInlineModel


class MeterInlineMeterTypeQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeQuery]


class MeterInlineMeterTypeResourcesQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeResourcesQuery]
