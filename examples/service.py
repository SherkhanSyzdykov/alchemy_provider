import random
from uuid import uuid4
from typing import List
from .queries import CustomerQuery, SecretStr
from .provider import CustomerProvider


class BaseService:
    pass


def id_serial() -> int:
    i = 0
    while True:
        yield i
        i += 1


def _generate_customers(count: int = 10) -> List[CustomerQuery]:
    id_generator = id_serial()
    customers = []
    for i in range(count):
        customers.append(CustomerQuery(
            username=str(uuid4()),
            phone_number=str(uuid4()),
            password=SecretStr(str(uuid4())),
            first_name=random.choice((str(uuid4()), None)),
            last_name=random.choice((str(uuid4()), None)),
            description=random.choice((str(uuid4()), None)),

        ))
    return customers


class CustomerFamily(BaseService):
    _customers = _generate_customers(10)
    _provider: CustomerProvider

    def __init__(self):
        super().__init__()
        _provider = CustomerProvider()

    async def descendants(
        self,
        parent_query: CustomerQuery,
        descendant_query: CustomerQuery,
        with_parent: bool = True,
    ) -> List[CustomerQuery]:
        pass

    async def ancestors(
        self,
        leaf_query: CustomerQuery,
        ancestor_query: CustomerQuery,
        with_leaf: bool = True
    ) -> List[CustomerQuery]:
        pass


class CustomerService(BaseService):
    _provider: CustomerProvider

    def __init__(self):
        super().__init__()
        _provider = CustomerProvider()

    async def get_one(
        self,
        query: CustomerQuery
    ) -> CustomerQuery:
        pass

    async def get_multi(
        self,
        query: CustomerQuery
    ) -> List[CustomerQuery]:
        pass

