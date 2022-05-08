from datetime import datetime
from uuid import UUID
from typing import Optional, List


class MountEventDirectory:
    city_name: str
    district_name: str
    street_name: str
    house_number: str
    entrance: Optional[str]
    apartment: Optional[str]


class MountEventMeterInline:
    serial_number: str
    coefficient: float
    unit_of_measurement: str
    initial_value: float
    initial_device_value: int
    point: str


class Geom:
    latitude: Optional[float]
    longitude: Optional[float]


class MountEventDevice:
    eui: str

    geo_data: Optional[Geom]


class DeviceType:
    id: int
    uuid: UUID
    name: str
    description: Optional[str]
    capability: Optional[dict]


class Device:
    id: Optional[int]
    uuid: Optional[UUID]
    dev_addr: Optional[str]
    eui: Optional[str]
    description: Optional[str]
    parameters: Optional[dict]
    active: Optional[bool]
    activated_time: Optional[datetime]
    deactivated_time: Optional[datetime]
    last_message_time: Optional[datetime]
    last_message: Optional[dict]
    new_fw_timestamp: Optional[bool]
    battery: Optional[float]

    geo_data: Optional[Geom]
    device_type: Optional[DeviceType]


class Resource:
    id: int
    uuid: UUID
    name: str
    category: Optional[int]
    has_rate: bool
    parameters: Optional[dict]
    icon: Optional[str]


class Field:
    id: int
    uuid: UUID
    name: str
    value_type: int


class MeterType:
    id: int
    uuid: UUID
    name: str
    description: Optional[str]
    coefficient: Optional[float]
    unit_of_measurement: Optional[str]
    multiplier: Optional[float]
    parameters: Optional[dict]
    mine: bool = False
    resources: List[Resource] = []


class Customer:
    id: int
    uuid: UUID
    name: str
    email: str
    password: Optional[str]
    description: Optional[str]
    type: Optional[int] = 0
    team: Optional[int] = 0
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    is_superuser: bool
    last_activity: Optional[datetime]
    date_joined: datetime
    parent_id: Optional[int]


class MountEvent:
    id: int
    uuid: UUID
    status: int
    event_type: int
    mounted_datetime: datetime
    updated_datetime: Optional[datetime]

    directory: MountEventDirectory
    meter_inline: MountEventMeterInline
    device: MountEventDevice

    device_type: Optional[DeviceType]
    resource: Optional[Resource]
    field: Optional[Field]
    meter_type: Optional[MeterType]
    mounted_by: Optional[Customer]
    updated_by: Optional[Customer]
