from __future__ import annotations
from abc import ABC
from typing import Any, get_type_hints, Type, get_args, Tuple


class BaseQuery(ABC):
    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    @classmethod
    def get_class(cls) -> Type[BaseQuery]:
        if isinstance(cls, BaseQuery):
            return cls.__class__

        return cls

    @classmethod
    def is_instance(cls) -> bool:
        return isinstance(cls, BaseQuery)

    @classmethod
    def get_type_hints(cls):
        class_ = cls
        if isinstance(cls, BaseQuery):
            class_ = cls.__class__

        return get_type_hints(class_)

    @classmethod
    def get_field_query(cls, field_name: str) -> Type[BaseQuery]:
        field_type_hint = cls.get_type_hints().get(field_name)
        if field_type_hint is None:
            raise AttributeError

        return cls._get_query_type(field_type_hint)

    @classmethod
    def _get_field_type(cls, field_name: str) -> Type:
        type_hints = cls.get_type_hints()
        if field_name in type_hints:
            return type_hints[field_name]

        return type(getattr(cls, field_name, Any))

    @classmethod
    def _get_field_types(cls, field_name: str) -> Tuple[Type]:
        field_type = cls._get_field_type(field_name=field_name)
        return getattr(field_type, '__args__', (field_type, ))

    @classmethod
    def _is_query_field(cls, field_name: str) -> bool:
        field_types = cls._get_field_types(field_name=field_name)
        for type_ in field_types:
            if issubclass(type_, BaseQuery):
                return True

        return False

    @staticmethod
    def _get_query_type(type_hint: Any) -> Type[BaseQuery]:
        try:
            if issubclass(type_hint, BaseQuery):
                return type_hint
        except:
            pass

        args = get_args(type_hint)
        answers = []
        for item in args:
            answers.append(BaseQuery._get_query_type(item))

        for answer in answers:
            try:
                if issubclass(answer, BaseQuery):
                    return answer
            except:
                pass

    def to_dict(self) -> dict:
        kwargs = self.__dict__
        for field, value in kwargs.items():
            if isinstance(value, BaseQuery):
                kwargs[field] = value.to_dict()

        return kwargs