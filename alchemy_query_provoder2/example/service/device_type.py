from uuid import UUID
from example import domain
from .base import BaseService
from .provider.device_type import DeviceTypeProvider


class DeviceTypeService(BaseService):
    _provider: DeviceTypeProvider

    def __init__(self):
        self._provider = DeviceTypeProvider()

    async def get(
        self,
        id: int = ...,
        uuid: domain.UUID = ...,
    ) -> domain.DeviceType:
        device_types = await self._provider.select(
            query=domain.DeviceType(
                id=id,
                uuid=uuid,
            )
        )
        if not device_types:
            raise

        return device_types[0]
