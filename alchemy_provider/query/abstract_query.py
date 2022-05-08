from abc import ABC
from .crud_query import CRUDQuery


class AbstractQuery(
    ABC,
    CRUDQuery
):
    pass
