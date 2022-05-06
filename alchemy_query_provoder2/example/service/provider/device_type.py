from clause_binder import AbstractClauseBinder
from provider import AbstractQueryProvider
from ... import domain
from .mapper import DeviceType


class DeviceTypeClauseBinder(AbstractClauseBinder):
    pass


class DeviceTypeProvider(AbstractQueryProvider):
    _mapper = DeviceType
    _clause_binder = DeviceTypeClauseBinder()
    _query_type = domain.DeviceType
