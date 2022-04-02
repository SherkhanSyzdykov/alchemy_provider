from __future__ import annotations
from typing import get_type_hints, Dict, Type, Tuple, Any
from abc import ABC, ABCMeta


class BaseTestMeta(ABCMeta):
    PREFIX = '__'

    def __new__(
        mcls,
        name: str,
        bases: Tuple[Type],
        namespace: Dict[str, Any],
        **kwargs
    ) -> BaseTestMeta:
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        cls.get_full_annotations = classmethod(
            lambda cls_: cls_.__annotations__
        )
        full_annotations = cls.get_full_annotations()

        for attr, annotation in full_annotations.items():
            def attr_property(self):
                print('property in meta base')
                return getattr(self, mcls.PREFIX + attr)

            setattr(
                cls,
                attr,
                property(attr_property)
            )

            def attr_setter(self: cls, value: Any):
                print('setter in meta base')
                setattr(self, mcls.PREFIX + attr, value)

            setattr(
                cls,
                attr,
                getattr(getattr(cls, attr), 'setter')(attr_setter)
            )

        return cls


class BaseTest(metaclass=BaseTestMeta):
    __full_annotations = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_full_annotations(cls) -> Dict[str, Type]:
        if cls.__full_annotations is None:
            cls.__full_annotations = get_type_hints(cls)

        return cls.__full_annotations


class Test(BaseTest):
    name: str
    test: str


class Test2(Test):
    test2: int

    @property
    def test2(self) -> int:
        print('test2 property')
        return self.__test2

    @test2.setter
    def test2(self, value: Any):
        print('test2 setter')
        self.__test2 = value
