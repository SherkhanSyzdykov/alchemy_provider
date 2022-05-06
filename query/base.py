from __future__ import annotations
from copy import deepcopy
from typing import Any, get_type_hints, Type, get_args, Tuple, Dict
from utils import cls_or_ins
from .field import Field


class BaseQuery:
    _filters: Dict[str, Any] = dict()

    def __init__(self, **kwargs):
        self._set_attrs(**kwargs)

    @staticmethod
    def _set_values(mapping: Dict[str, Any], **kwargs):
        for field, value in kwargs.items():
            if value is ...:
                continue

            mapping[field] = value

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

    @cls_or_ins
    def is_class(cls_or_ins) -> bool:
        return not isinstance(cls_or_ins, BaseQuery) \
               and issubclass(cls_or_ins, BaseQuery)

    @cls_or_ins
    def is_instance(cls_or_ins) -> bool:
        return isinstance(cls_or_ins, BaseQuery)

    @cls_or_ins
    def get_filters(cls_or_ins) -> Dict[str, Any]:
        return deepcopy(cls_or_ins._filters)

    @cls_or_ins
    def set_filters(cls_or_ins, **kwargs) -> BaseQuery:
        self = cls_or_ins
        if cls_or_ins.is_class():
            self = cls_or_ins()

        self._set_values(self._filters, **kwargs)

        return self

    @cls_or_ins
    def get_class(cls_or_ins) -> Type[BaseQuery]:
        if cls_or_ins.is_instance:
            return cls_or_ins.__class__

        return cls_or_ins

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

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

        field = cls._get_query_type(field_type_hint)

        if field is None or not issubclass(field, BaseQuery):
            raise KeyError(
                f'Attribute {field_name}, '
                f'in {cls.__name__ or cls.__class__.__name__} is not Query type'
            )

        return field

    @classmethod
    def get_fields_count(cls) -> int:
        return len(cls.get_type_hints())

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

    @property
    def dict(self) -> Dict[str, Any]:
        mapping = dict()
        for field, value in self.__dict__.items():
            if field.startswith('_'):
                continue

            if isinstance(value, BaseQuery):
                mapping[field] = value.dict

            mapping[field] = value

        return mapping

    def _set_attrs(self, **kwargs):
        for field, value in kwargs.items():
            if value is ...:
                value = None

            if field not in self.get_type_hints():
                continue

            attr_default = getattr(self, field, None)
            if isinstance(attr_default, Field):
                setattr(self, field, attr_default(value))
                continue

            setattr(self, field, value)
