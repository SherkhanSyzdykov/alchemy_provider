from __future__ import annotations

from typing import Optional, Tuple, Any, List
from sqlalchemy.sql import Join
from alchemy_provider.query import BaseQuery
from .mappers import *


class SecretStr(str):
    def __init__(self, value: str):
        super().__init__()
        self.__secret_value = value

    @property
    def secret_value(self) -> str:
        return self.__secret_value

    def __str__(self):
        return '*****'

    def __repr__(self):
        return self.__class__.__name__ + '*****'


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
    id: int
    uuid: UUID
    username: str
    phone_number: str
    password: SecretStr
    first_name: Optional[str]
    last_name: Optional[str]
    description: Optional[str]

    parent_id: Optional[int]
    parent: Optional[CustomerQuery]

    class Meta:
        mapper = CustomerMapper
