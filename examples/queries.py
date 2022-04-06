from __future__ import annotations

from typing import Optional, Tuple, Any, List
from sqlalchemy.sql import Join
from alchemy_provider.query import BaseQuery
from .mappers import *


class MeterTypeQuery(BaseQuery):
    name: str
    description: str

    class Meta:
        mapper = MeterTypeModel

    # @property
    # def name(self) -> int:
    #     try:
    #         return int(self.__name)
    #     except:
    #         return 0
    #
    # @name.setter
    # def name(self, value: Any):
    #     self.__name = value


class ResourceQuery(BaseQuery):
    name: str

    class Meta:
        mapper = ResourceModel


class MeterTypeResourcesQuery(MeterTypeQuery):
    resources: Optional[Tuple[ResourceQuery]]


class ResourceMeterTypesQuery(ResourceQuery):
    meter_types: Tuple[MeterTypeQuery] = tuple()


class MeterInlineQuery(BaseQuery):
    serial_number: str
    is_active: bool

    class Meta:
        mapper = MeterInlineModel


class MeterInlineMeterTypeQuery(MeterInlineQuery):
    meter_type: Optional[MeterTypeQuery] = Join(
        MeterInlineModel,
        MeterTypeModel,
        MeterInlineModel.meter_type_id == MeterTypeModel.id,
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


class CustomerQuery(BaseQuery):
    username: str
    phone_number: str
    password: str


class MeterInlineCustomerQuery(MeterInlineQuery):
    created_by: CustomerQuery
    updated_by: Optional[CustomerQuery]
