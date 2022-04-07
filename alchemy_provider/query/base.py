from __future__ import annotations
from abc import ABC, ABCMeta
from typing import Tuple, Type, Dict, Any, get_type_hints
from sqlalchemy.orm import DeclarativeMeta
import orjson


class BaseQueryMeta(ABCMeta):
    pass


class BaseQuery(metaclass=BaseQueryMeta):
    __full_annotations = None

    class Meta(ABC):
        mapper: DeclarativeMeta

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_class(cls) -> Type[BaseQuery]:
        if isinstance(cls, BaseQuery):
            return cls.__class__

        return cls

    def dict(self) -> Dict[str, Any]:
        result_dict: Dict[str, Any] = {}
        full_annotations = self.get_full_annotations()
        for field in full_annotations.keys():
            if not self.is_query_field(field=field):
                result_dict[field] = getattr(self, field)
                continue

            nested_query_instance = getattr(self, field)
            result_dict[field] = nested_query_instance.dict()

        return result_dict

    def json(self) -> str:
        return orjson.dumps(self.dict()).decode('utf-8')

    def jsonb(self) -> bytes:
        return orjson.dumps(self.dict())

    @classmethod
    def _from_row(
        cls,
        row: Tuple[Any],
    ) -> BaseQuery:
        full_annotations = cls.get_full_annotations()
        query_instance = cls()

        i = 0
        while i < len(row):
            for field in full_annotations.keys():
                if not cls.is_query_field(field=field):
                    setattr(query_instance, field, row[i])
                    i += 1
                    continue

                nested_query = cls.get_field_query(field=field)
                nested_query_fields_count = cls.get_fields_count()
                nested_query_instance = nested_query._from_row(
                    row[i: i + nested_query_fields_count]
                )
                setattr(query_instance, field, nested_query_instance)
                i += nested_query_fields_count

        return query_instance

    @classmethod
    def from_row(cls, row: Tuple[Any]) -> BaseQuery:
        return cls.get_class()._from_row(row=row)

    @classmethod
    def get_fields_count(cls) -> int:
        return len(cls.get_full_annotations())

    @classmethod
    def is_query_field(cls, field: str) -> bool:
        field_types = cls.get_field_types(field=field)
        for type_ in field_types:
            if issubclass(type_, BaseQuery):
                return True

        return False

    @classmethod
    def get_mapper(cls) -> DeclarativeMeta:
        return cls.Meta.mapper

    @classmethod
    def get_full_annotations(cls) -> Dict[str, Type]:
        # if cls.__full_annotations is None:
        #     cls.__full_annotations = get_type_hints(cls)
        #
        # return cls.__full_annotations
        return get_type_hints(cls)

    @classmethod
    def is_available_type(cls, field: str, type_: Type) -> bool:
        return type_ in cls.get_field_types(field=field)

    @classmethod
    def get_field_type(cls, field: str) -> Type:
        full_annotations = cls.get_full_annotations()
        if field in full_annotations:
            return full_annotations[field]

        return type(getattr(cls, field, Any))

    @classmethod
    def get_field_types(cls, field: str) -> Tuple[Type]:
        field_type = cls.get_field_type(field=field)
        return getattr(field_type, '__args__', (field_type, ))

    @classmethod
    def is_optional(cls, field: str) -> bool:
        return type(None) in cls.get_field_types(field=field)

    @classmethod
    def _get_query_from_field_type(cls, field_type: Any) -> Type[BaseQuery]:
        try:
            if type(field_type) is BaseQueryMeta:
                return field_type
            types_ = field_type.__args__
            for type_ in types_:
                return cls._get_query_from_field_type(field_type=type_)
        except:
            raise  # TODO

    @classmethod
    def get_field_query(cls, field: str) -> Type[BaseQuery]:
        field_type = cls.get_field_type(field=field)
        return cls._get_query_from_field_type(field_type=field_type)

    @property
    def get_fields(self) -> Dict[str, Any]:
        return self.__dict__