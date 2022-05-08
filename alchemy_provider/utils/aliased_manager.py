from typing import Dict
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.util import AliasedClass
from .alchemy_orm import make_aliased_mapper


class AliasedManager:
    __aliased_map: Dict[int, Dict[str, AliasedClass]] = dict()

    @classmethod
    def get_or_create(
        cls,
        stmt_id: int,
        mapper: DeclarativeMeta,
        field_name: str
    ) -> AliasedClass:
        if cls.is_exist(stmt_id=stmt_id, field_name=field_name):
            return cls.__aliased_map[stmt_id][field_name]

        aliased_mapper = make_aliased_mapper(
            mapper=mapper,
            field_name=field_name
        )
        cls.__aliased_map[stmt_id] = cls.__aliased_map.get(stmt_id, {})
        cls.__aliased_map[stmt_id][field_name] = aliased_mapper

        return aliased_mapper

    @classmethod
    def delete(
        cls,
        stmt_id: int,
    ):
        cls.__aliased_map.pop(stmt_id, None)

    @classmethod
    def is_exist(
        cls,
        stmt_id: int,
        field_name: str,
    ) -> bool:
        return bool(cls.__aliased_map.get(stmt_id, {}).get(field_name, False))
