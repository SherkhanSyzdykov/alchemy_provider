from uuid import UUID
from datetime import datetime
from example import domain
from .base import BaseService
from .device_type import DeviceTypeService
from .provider.device import DeviceProvider


def ll2geom(
    latitude: float = ...,
    longitude: float = ...,
) -> str:
    geom = ...
    if latitude is ...:
        latitude = 0
    if longitude is ...:
        longitude = 0
    if any((latitude, longitude)):
        geom = f'POINT({latitude} {longitude})'
    return geom



class DeviceService(BaseService):
    _provider: DeviceProvider
    _s_device_type: DeviceTypeService

    def __init__(self):
        self._provider = DeviceProvider()
        self._s_device_type = DeviceTypeService()

    async def create(
        self,
        eui: str,
        device_type_id: int = ...,
        device_type_uuid: UUID = ...,
        dev_addr: str = ...,
        description: str = ...,
        parameters: dict = ...,
        new_fw_timestamp: bool = ...,
        latitude: float = ...,
        longitude: float = ...,
        battery: float = ...,
    ) -> domain.Device:
        device_type = await self._s_device_type.get(
            id=device_type_id,
            uuid=device_type_uuid
        )

        device = await self._provider.insert(
            query=domain.Device(
                device_type_id=device_type.id,
                eui=eui,
                dev_addr=dev_addr,
                description=description,
                parameters=parameters,
                new_fw_timestamp=new_fw_timestamp,
                activated_time=datetime.utcnow(),
                active=True,
                deactivated_time=None,
                geo_data=ll2geom(latitude, longitude),
                battery=battery
            )
        )

        return device

