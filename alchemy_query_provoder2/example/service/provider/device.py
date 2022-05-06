from clause_binder import AbstractClauseBinder
from provider import AbstractQueryProvider
from ... import domain
from .mapper import Device


class DeviceClauseBinder(AbstractClauseBinder):
    pass


class DeviceProvider(AbstractQueryProvider):
    _mapper = Device
    _clause_binder = DeviceClauseBinder()
    _query_type = domain.Device
