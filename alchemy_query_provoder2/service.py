from __future__ import annotations
from typing import List
from query import DeviceQuery, CustomerQuery, DeviceTypeQuery
from provider import DeviceProvider


class BaseService:
    pass


class DeviceService(BaseService):
    _provider: DeviceProvider

    def __init__(self):
        self._provider = DeviceProvider()

    def get_list(
        self,
        query: DeviceQuery = ...,
        limit: int = 25,
        offset: int = 0,
        order_by: str = ...,
        order_reversed: bool = False,
    ) -> List[DeviceQuery]:
        filters = {
            'uuid__ne': 'null',
            'active': 'true',
            'customers__id__ne': 'null',
            'customers': {
                'id__ne': 'null'
            }
        }

        device_query = DeviceQuery(
            uuid__ne=None,
            eui__ilike='%some_eui%',
            dev_addr__ne=None,
            active=False,
            customers=CustomerQuery(
                id__ne=None,
                name__ilike='%some_customer_name%'
            ),
            device_type=DeviceTypeQuery(
                name__ilike='%some_device_type_name%'
            )
        )
        sql_stmt = self._provider.make_select_stmt(query=device_query)
        return sql_stmt


service = DeviceService()
sql_stmt = service.get_list()

