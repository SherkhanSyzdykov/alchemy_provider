from uuid import UUID
from typing import Optional, List
from datetime import datetime
from .base import BaseDomain
from .device_type import DeviceType
from .fbase import FBase


class Geom(BaseDomain):
    latitude: Optional[float]
    longitude: Optional[float]


class Device(BaseDomain):
    eui: str
    active: bool
    id: Optional[int]
    uuid: Optional[UUID]
    dev_addr: Optional[str]
    description: Optional[str]
    parameters: Optional[dict]
    activated_time: Optional[datetime]
    deactivated_time: Optional[datetime]
    last_message_time: Optional[datetime]
    last_message: Optional[dict]
    new_fw_timestamp: Optional[bool]
    battery: Optional[float]

    geo_data: Optional[Geom]
    device_type: Optional[DeviceType]


class DeviceList(BaseDomain):
    items: List[Device] = []


class FDevice(FBase):
    pass

