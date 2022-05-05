from __future__ import annotations
from abc import ABC
from .select_query import SelectQuery
from .insert_query import InsertQuery
from .update_query import UpdateQuery
from .delete_query import DeleteQuery


class AbstractQuery(ABC, SelectQuery, InsertQuery, UpdateQuery, DeleteQuery):
    pass


# class CustomerQuery(BaseQuery):
#     uuid: uuid.UUID
#     name: str
#     email: str
#     description: Optional[str]
#     type: int = 0
#     team: int = 0
#     first_name: Optional[str]
#     last_name: Optional[str]
#     password: SecretStr
#     is_active: bool = True
#     is_superuser: bool = False
#     last_activity: Optional[datetime]
#     date_joined: datetime
#
#     parent_id: Optional[int]
#
#     # devices: List[DeviceQuery] = JoinStrategy(is_outer=True, is_full=True)
#
#
# class DeviceTypeQuery(BaseQuery):
#     uuid: uuid.UUID
#     name: str
#     description: str
#     capability: dict
#
#     # devices: List[DeviceQuery] = JoinStrategy(is_outer=True, is_full=False)
#
#
# class DeviceQuery(BaseQuery):
#     uuid: uuid.UUID
#     eui: str
#     dev_addr: Optional[str]
#     description: Optional[str]
#     active: bool = True
#     new_fw_timestamp: bool = True
#
#     device_type: Optional[DeviceTypeQuery] = JoinStrategy(is_outer=True, is_full=False)
#     customers: List[CustomerQuery] = JoinStrategy(is_outer=False, is_full=True)
