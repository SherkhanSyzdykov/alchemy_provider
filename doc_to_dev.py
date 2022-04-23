"""
Direction of development should be from the highest abstraction to
the lowest abstraction, example:

develop first
class Service:
    provider: Provider

develop second
class Provider:
    db: Database

develop third
class Database:
    pass


FEATURES TO DEVELOP
1. PROVIDER THAT MANAGES CONNECTION TO DB
2. CACHEABLE PROVIDER THAT CACHES RECORDS FROM DB IF TYPE OF QUERY IS THE SAME
3. ADD VALIDATION ABILITY BY PYDANTIC

# classes to Join, Where, GroupBy, OrderBy



class CustomerMapper(BaseMapper):
    name = Column(String)
    phone_number = Column(String)
    password = Column(String)
    description = Column(String, nullable=True)


class CustomerQuery(BaseQuery):
    name: str
    phone_number: str
    password: SecretStr
    description: Optional[str]


class CustomerListQuery(BaseQuery):
    items: List[CustomerQuery]



example of usage:

SOMEWHERE ENDPOINTS LIKE:
async def get_customers() -> Customers:
    pass




"""


