from typing import Optional, Tuple, TypedDict
from sqlalchemy.orm import DeclarativeMeta
from .models import *


class BaseQuery(TypedDict):
    class Meta:
        mapper: DeclarativeMeta

    def __init__(self):
        super().__init__()


class MeterTypeQuery(BaseQuery):
    name: str

    class Meta:
        mapper = MeterTypeModel


class ResourceQuery(BaseQuery):
    name: str

    class Meta:
        mapper = ResourceModel


class MeterTypeResourcesQuery(MeterTypeQuery):
    resources: Tuple[ResourceQuery]


class ResourceMeterTypesQuery(ResourceQuery):
    meter_types: Tuple[MeterTypeQuery]


class MeterInlineQuery(BaseQuery):
    serial_number: str
    is_active: bool

    class Meta:
        mapper = MeterInlineModel


class MeterInlineMeterTypeQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeQuery]


class MeterInlineMeterTypeResourcesQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeResourcesQuery]


"""
Think about full join
"""
