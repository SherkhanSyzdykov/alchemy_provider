import asyncio
from typing import Union, Optional
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
import mapper
import domain
from alchemy_provider.provider import AbstractProvider
from alchemy_provider.clause_binder import ClauseBinder
from alchemy_provider.query import AbstractQuery, JoinStrategy
from alchemy_provider.utils.aliased_manager import AliasedManager


class BaseQuery(AbstractQuery):
    limit: int = 25
    offset: int = 0

class DeviceTypeQuery(BaseQuery, domain.DeviceType):
    __query_mapper__ = mapper.DeviceType

class ResourceQuery(BaseQuery, domain.Resource):
    __query_mapper__ = mapper.Resource

class FieldQuery(BaseQuery, domain.Field):
    __query_mapper__ = mapper.Field

class MeterTypeQuery(BaseQuery, domain.MeterType):
    __query_mapper__ = mapper.MeterType

class CustomerQuery(BaseQuery, domain.Customer):
    __query_mapper__ = mapper.Customer

class MountEventQuery(BaseQuery, domain.MountEvent):
    __query_mapper__ = mapper.MountEvent

    device_type: Optional[DeviceTypeQuery] = JoinStrategy(is_outer=True)
    resource: Optional[ResourceQuery] = JoinStrategy(is_outer=True)
    field: Optional[FieldQuery] = JoinStrategy(is_outer=True)
    meter_type: Optional[MeterTypeQuery] = JoinStrategy(is_outer=True)
    mounted_by: Optional[CustomerQuery]
    updated_by: Optional[CustomerQuery] = JoinStrategy(is_outer=True)

class MountEventClauseBinder(ClauseBinder):
    pass

class MountEventProvider(AbstractProvider):
    _mapper = mapper.MountEvent
    _query_type = MountEventQuery
    _clause_binder = MountEventClauseBinder()

    session = AsyncSession(engine)

    @property
    def _session(self) -> Union[AsyncSession, async_scoped_session]:
        if self.session is None:
            self.session = AsyncSession(engine)

        return self.session


select_kwargs = dict(
    id__g=1,
    # status__in=[0, 1, 2],
    # device_type__name__ilike='%a%',
    # device_type={
    #     'id__l': 100,
        # 'description__ilike': '%a%'
    # },
    # meter_type={
    #     'id__lt': 10,
        # 'name__like': '%a%'
    # },
    # meter_type__description__ilike='%a%',
    # mounted_by__is_active=True,
    # mounted_by__team__in=[0, 1, 2],
    limit=100,
    offset=0
)


async def main():
    provider = MountEventProvider()

    stmt = select(
        mapper.MountEvent, mapper.DeviceType
    ).join(mapper.MountEvent.device_type).limit(5)

    result = await provider.session.execute(stmt)

    query = await MountEventQuery.from_mappers_tuple_list(result.all())

    await provider.session.rollback()
    await provider.session.close()

    return query


res = asyncio.run(main())

provider = MountEventProvider()

insert_stmt = provider.make_insert_stmt(
        status=0,
        event_type=0,
        device_type_id=1,
        field_id=2,
    )

bulk_insert_stmt = provider.make_bulk_insert_stmt(
    values_seq=[
        dict(status=0, event_type=0, device_type_id=1, field_id=0),
        dict(status=1, event_type=2, device_type_id=1, field_id=1)
    ]
)


select_count_stmt = provider.make_count_stmt(
    id__g=1,
    status__in=[1, 2],
    device_type__name__ilike='%some_name%',
    device_type={
        'id__l': 100,
        'description__ilike': '%desc%'
    },
    meter_type={
        'id__lt': 2,
        'name__like': '%sdfsdf%'
    },
    meter_type__description__ilike='%asdfsdf%',
    mounted_by__is_active=True,
    mounted_by__team__in=[1, 2],
    limit=1,
    offset=2
)


select_stmt = provider.make_select_stmt(
    id__g=1,
    status__in=[1, 2],
    device_type__name__ilike='%some_name%',
    device_type={
        'id__l': 100,
        'description__ilike': '%desc%'
    },
    meter_type={
        'id__lt': 2,
        'name__like': '%sdfsdf%'
    },
    meter_type__description__ilike='%asdfsdf%',
    mounted_by__name__ilike='%sdfsdf%',
    mounted_by__name__in=['some_name'],
    mounted_by__type__in=[1, 2],
    limit=1,
    offset=2
)

update_stmt = provider.make_update_stmt_from_kwargs(
    id__g=1,
    status__in=[1, 2],
    # device_type__name__ilike='%some_name%',
    # device_type={
    #     'id__l': 100,
    #     'description__ilike': '%desc%'
    # },
    # meter_type={
    #     'id__lt': 2,
    #     'name__like': '%sdfsdf%'
    # },
    # meter_type__description__ilike='%asdfsdf%',
    event_type=1,
    directory={'city_name': 'asdfsdf'}
)

delete_stmt = provider.make_delete_stmt(
    id__g=1,
    status__in=[1, 2],
    # device_type__name__ilike='%some_name%',
    # device_type={
    #     'id__l': 100,
    #     'description__ilike': '%desc%'
    # },
    # meter_type={
    #     'id__lt': 2,
    #     'name__like': '%sdfsdf%'
    # },
    # meter_type__description__ilike='%asdfsdf%',
)
