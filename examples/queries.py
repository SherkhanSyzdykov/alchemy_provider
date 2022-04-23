from __future__ import annotations

from typing import Optional, Tuple, Any, List
from sqlalchemy.sql import Join
from alchemy_provider.query import BaseQuery
from .mappers import *


class SecretStr(str):
    pass


class MeterTypeQuery(BaseQuery):
    name: str
    description: str

    class Meta:
        mapper = MeterTypeMapper


class ResourceQuery(BaseQuery):
    name: str

    class Meta:
        mapper = ResourceMapper


class MeterTypeResourcesQuery(MeterTypeQuery):
    resources: Optional[Tuple[ResourceQuery]]


class ResourceMeterTypesQuery(ResourceQuery):
    meter_types: Tuple[MeterTypeQuery] = tuple()


class MeterInlineQuery(BaseQuery):
    serial_number: str
    is_active: bool

    class Meta:
        mapper = MeterInlineMapper


class MeterInlineMeterTypeQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeQuery] = Join(
        MeterInlineMapper,
        MeterTypeMapper,
        MeterInlineMapper.meter_type_id == MeterTypeMapper.id,
        isouter=True,
        full=False
    )
    # stmt = stmt.join_from(
    #   meter_type.left,
    #   meter_type.right,
    #   meter_type.onclause,
    #   meter_type.isouter,
    #   meter_type.full
    # )


class MeterInlineMeterTypeResourcesQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeResourcesQuery]


# class MeterInlinesQuery(BaseQuery):
#     items: List[MeterInlineQuery] = []


class MeterInlineCustomerQuery(MeterInlineQuery):
    created_by: CustomerQuery
    updated_by: Optional[CustomerQuery]


class CustomerQuery(BaseQuery):
    username: str
    phone_number: str
    password: SecretStr
    first_name: Optional[str]
    last_name: Optional[str]
    description: Optional[str]

    class Meta:
        mapper = CustomerMapper
