from dataclasses import dataclass
from typing import Optional, Iterable, Sequence, List, Tuple, get_type_hints, get_args, get_origin


class SecretStr(str):
    pass


class Base:
    pass


class Customer(Base):
    name: str
    phone_number: str
    password: SecretStr
    description: Optional[str]


class CustomerList(Base):
    items: List[Customer] = list


