from uuid import UUID
from typing import Dict
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.util import AliasedClass
from .alchemy_orm import make_aliased_mapper


class AliasedManager:
    __aliased_map: Dict[UUID, Dict[str, AliasedClass]] = dict()

    @classmethod
    def get_or_create(
        cls,
        uuid: UUID,
        mapper: DeclarativeMeta,
        field_name: str
    ) -> AliasedClass:
        if cls.is_exist(uuid=uuid, field_name=field_name):
            return cls.__aliased_map[uuid][field_name]

        aliased_mapper = make_aliased_mapper(
            mapper=mapper,
            field_name=field_name
        )
        cls.__aliased_map[uuid] = cls.__aliased_map.get(uuid, {})
        cls.__aliased_map[uuid][field_name] = aliased_mapper

        return aliased_mapper

    @classmethod
    def delete(
        cls,
        uuid: UUID,
    ):
        print('CLS.__ALIASED_MAP')
        print(cls.__aliased_map)
        [print(i) for i in cls.__aliased_map]
        print()
        cls.__aliased_map.pop(uuid, None)

    @classmethod
    def is_exist(
        cls,
        uuid: UUID,
        field_name: str,
    ) -> bool:
        return bool(cls.__aliased_map.get(uuid, {}).get(field_name, False))
