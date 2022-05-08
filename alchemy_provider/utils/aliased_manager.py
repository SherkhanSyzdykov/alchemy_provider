from typing import Dict
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.util import AliasedClass
from .alchemy_orm import make_aliased_mapper


class AliasedManager:
    __aliased_map: Dict[str, AliasedClass] = dict()

    @classmethod
    def get_or_create(
        cls,
        mapper: DeclarativeMeta,
        field_name: str
    ) -> AliasedClass:
        key = cls._make_key(mapper=mapper, field_name=field_name)
        if key in cls.__aliased_map:
            return cls.__aliased_map[key]

        aliased_mapper = make_aliased_mapper(
            mapper=mapper,
            field_name=field_name
        )
        cls.__aliased_map[key] = aliased_mapper

        return aliased_mapper

    @classmethod
    def _make_key(
        cls,
        mapper: DeclarativeMeta,
        field_name: str
    ) -> str:
        return mapper.__name__ + '__' + field_name
