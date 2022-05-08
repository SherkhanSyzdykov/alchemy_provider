import asyncio
from typing import Union, Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
import mapper
import domain
from alchemy_provider.provider import AbstractProvider
from alchemy_provider.clause_binder import ClauseBinder
from alchemy_provider.query import AbstractQuery


engine = create_async_engine(
    'postgresql+asyncpg://developer:zie7ua6Ohleo9poh8hig3iedooyaem6ielaibi9aitahGhoh7saogeicohkaepheiHaeCh3aingeghahRe2lae4oom4Nee8eidies0Aesae0pe7QuohGheesh0eitheu@35.228.147.44:5432/development',
    echo=True
)


class BaseQuery(AbstractQuery):
    limit: int = 25
    offset: int = 0


class DeviceTypeQuery(BaseQuery, domain.DeviceType):
    pass


class ResourceQuery(BaseQuery, domain.Resource):
    pass


class FieldQuery(BaseQuery, domain.Field):
    pass


class MeterTypeQuery(BaseQuery, domain.MeterType):
    pass


class CustomerQuery(BaseQuery, domain.Customer):
    pass


class MountEventQuery(BaseQuery, domain.MountEvent):

    device_type: Optional[DeviceTypeQuery]
    resource: Optional[ResourceQuery]
    field: Optional[FieldQuery]
    meter_type: Optional[MeterTypeQuery]
    mounted_by: Optional[CustomerQuery]
    updated_by: Optional[CustomerQuery]


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


async def main():
    provider = MountEventProvider()
    customer_descendants = [1, 2, 3]

    insert_stmt = provider.make_insert_stmt(
        status=0,
        event_type=0,
        device_type_id=1,
        field_id=2,
    )

    await provider.session.rollback()
    await provider.session.close()

    return insert_stmt


# res = asyncio.run(main())

provider = MountEventProvider()

insert_stmt = provider.make_insert_stmt(
        status=0,
        event_type=0,
        device_type_id=1,
        field_id=2,
    )

bulk_insert_stmt = provider.make_bulk_insert_stmt(
    values_seq=[
        dict(status=0, event_type=0, device_type_id=1, field_id=0)
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
    mounter_by__is_active=True,
    mounted_by__team__in=[1, 2],
    limit=1,
    offset=2
)

# TODO
# TODO
# TODO
# TODO
# TODO
# Bug with mounted_by__is_active
# Bug with aliased state, so mounted_by__team__in is saved in second select_stmt
# query
# TODO
# TODO
# TODO
# TODO
# TODO

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


