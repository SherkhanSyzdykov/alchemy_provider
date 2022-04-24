from abc import ABC, ABCMeta
from dataclasses import dataclass
from typing import Optional, Iterable, Sequence, \
    List, Tuple, get_type_hints, get_args, get_origin, Literal, final, Final
from types import NoneType
from pydantic import BaseModel


LOOKUP_STRING = '__'
OR_LOOKUP = '__or__'

EQUAL_OPERATOR = 'e'
NOT_EQUAL_OPERATOR = 'ne'
LESS_THAN_OPERATOR = 'l'
LESS_THAN_OR_EQUAL_TO_OPERATOR = 'le'
GREATER_THAN_OPERATOR = 'g'
GREATER_THAN_OR_EQUAL_TO_OPERATOR = 'ge'
LIKE_OPERATOR = 'like'
ILIKE_OPERATOR = 'ilike'
IN_OPERATOR = 'in'
NOT_IN_OPERATOR = 'not_in'
ALL_OBJECTS_FILTER = '__all__'


ANNOTATION_SETTERS = {
    EQUAL_OPERATOR: lambda type_: Optional[type_],
    NOT_EQUAL_OPERATOR: lambda type_: Optional[type_],
    LESS_THAN_OPERATOR: lambda type_: Optional[type_],
    LESS_THAN_OR_EQUAL_TO_OPERATOR: lambda type_: Optional[type_],
    GREATER_THAN_OPERATOR: lambda type_: Optional[type_],
    GREATER_THAN_OR_EQUAL_TO_OPERATOR: lambda type_: Optional[type_],
    LIKE_OPERATOR: lambda type_: Optional[type_],
    ILIKE_OPERATOR: lambda type_: Optional[type_],
    IN_OPERATOR: lambda type_: Optional[Iterable[type_]],
    NOT_IN_OPERATOR: lambda type_: Optional[Iterable[type_]],
}


AVAILABLE_LOOKUPS_PER_TYPE = {
    str: (
        EQUAL_OPERATOR,
        NOT_EQUAL_OPERATOR,
        LESS_THAN_OPERATOR,
        LESS_THAN_OR_EQUAL_TO_OPERATOR,
        GREATER_THAN_OPERATOR,
        GREATER_THAN_OR_EQUAL_TO_OPERATOR,
        LIKE_OPERATOR,
        ILIKE_OPERATOR,
        IN_OPERATOR,
        NOT_IN_OPERATOR,
    ),
    int: (
        EQUAL_OPERATOR,
        NOT_EQUAL_OPERATOR,
        LESS_THAN_OPERATOR,
        LESS_THAN_OR_EQUAL_TO_OPERATOR,
        GREATER_THAN_OPERATOR,
        GREATER_THAN_OR_EQUAL_TO_OPERATOR,
        IN_OPERATOR,
        NOT_IN_OPERATOR,
    ),
    float: (
        EQUAL_OPERATOR,
        NOT_EQUAL_OPERATOR,
        LESS_THAN_OPERATOR,
        LESS_THAN_OR_EQUAL_TO_OPERATOR,
        GREATER_THAN_OPERATOR,
        GREATER_THAN_OR_EQUAL_TO_OPERATOR,
        IN_OPERATOR,
        NOT_IN_OPERATOR,
    )
}


def is_primitive(type_: type):
    return type_ in AVAILABLE_LOOKUPS_PER_TYPE


class BaseQueryMeta(type):
    def __new__(cls, *args, **kwargs):
        declared_class = super().__new__(cls, *args, **kwargs)

        if declared_class.__name__ == 'CustomerQuery':
            import pdb
            pdb.set_trace()


        origin_annotations = get_type_hints(declared_class)
        declared_class.__origin_annotations__ = origin_annotations
        declared_class.get_origin_annotations = classmethod(
            lambda cls: cls.__origin_annotations__
        )



        if declared_class.__name__ == 'CustomerQuery':
            import pdb
            pdb.set_trace()

        for name, type_ in origin_annotations.items():
            if lookup_operators := AVAILABLE_LOOKUPS_PER_TYPE.get(type_):
                for lookup_operator in lookup_operators:
                    declared_class.__annotations__[
                        name + LOOKUP_STRING + lookup_operator
                    ] = ANNOTATION_SETTERS.get(lookup_operator)(type_)

        return declared_class


class BaseQuery(metaclass=BaseQueryMeta):
    def __init__(self, *args, **kwargs):
        pass



class BaseCustomerQuery(BaseQuery):
    name: str
    phone_number: str
    first_name: Optional[str]


class CustomerQuery(BaseCustomerQuery):
    phone_number: Optional[str]
    last_name: Optional[str]


#
# class Customer(ABC):
#     name: str
#     phone_number: str
#     password: SecretStr
#     description: Optional[str]
#
#
# class CustomerList(ABC):
#     items: List[Customer] = list
#
#
