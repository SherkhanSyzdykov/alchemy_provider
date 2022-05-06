from __future__ import annotations
import asyncio
import sys
from datetime import datetime
from uuid import UUID
from typing import Optional, Union
from pydantic import BaseModel
# from geoalchemy2.shape import to_shape
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, \
    create_async_engine
from clause_binder import AbstractClauseBinder
from query import AbstractQuery, JoinStrategy, Field
from provider import AbstractQueryProvider
from mapper import Device as DeviceMapper


class Geom(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]


class DeviceType:
    id: int
    uuid: UUID
    name: str
    description: Optional[str]
    capability: Optional[dict]


class Device:
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


class DeviceDomain(BaseModel, Device):
    pass


def geom_setter(value) -> Geom:
    import pdb
    pdb.set_trace()
    latitude = None
    longitude = None
    if value:
        # point = to_shape(value)
        # latitude = point.x
        # longitude = point.y
        pass

    geom = Geom(
        latitude=latitude,
        longitude=longitude
    )
    return geom


class DeviceTypeQuery(AbstractQuery, DeviceType):
    pass


class DeviceQuery(AbstractQuery, Device):
    device_type: Optional[DeviceTypeQuery] = JoinStrategy()
    geo_data: Optional[Geom] = Field(adapter=geom_setter)


# device_query = DeviceQuery.set_filters(
#     id__g=1,
#     description__ilike='%sfsdf%',
# )

# device_query2 = DeviceQuery(id=1, eui='asdfsdf', geo_data='SOme_geo_data')


class DeviceClauseBinder(AbstractClauseBinder):
    _mapper = DeviceMapper

    def meter_inline(self, *args, **kwargs):
        import pdb
        pdb.set_trace()


class DeviceProvider(AbstractQueryProvider):
    _clause_binder = DeviceClauseBinder()
    _mapper = DeviceMapper
    _query_type = DeviceQuery
    __session: AsyncSession = None

    @property
    def _session(self) -> Union[AsyncSession, async_scoped_session]:
        if self.__session is None:
            self.__session = AsyncSession(engine)

        return self.__session


async def main():
    device_provider = DeviceProvider()
    # result1 = await device_provider.select(id__g=1)
    # result2 = await device_provider.select(
    #     id__g=1,
    #     description__ilike='%sdfsdfe%',
    #     device_type__id__g=1,
    #     device_type={
    #         'name__ilike': '%some_device_type_name%',
    #         # 'uuid': 'device_type_uuid'
    #     },
    #     # uuid='asdfsdf',
    # )
    # result1 = await device_provider.insert(
    #     description='some_description',
    #     eui='asdfa1'
    # )
    #
    # result2 = await device_provider.bulk_insert(
    #     [
    #         dict(
    #             description='some_description',
    #             eui='asdfa2'
    #         ),
    #         dict(
    #             description='some_description',
    #             eui='asdfa2'
    #         )
    #     ]
    # )

    await device_provider.delete(
        id__g=1,
        # description__ilike='%asdfsd%'
    )


    await device_provider._session.rollback()
    await device_provider._session.close()

    return


result = asyncio.run(main())
