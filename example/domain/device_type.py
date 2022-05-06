from typing import Optional, List
from uuid import UUID
from .base import BaseDomain
from .fbase import FBase


class DeviceType(BaseDomain):
    id: int
    uuid: UUID
    name: str
    description: Optional[str]
    capability: Optional[dict]


class DeviceTypeList(BaseDomain):
    items: List[DeviceType] = []


class FDeviceType(FBase):
    pass
