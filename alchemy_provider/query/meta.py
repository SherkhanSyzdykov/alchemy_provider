from abc import ABCMeta


class BaseQueryMeta(ABCMeta):
    """
    Here should be released functions that checks each class which
    inherit from BaseQuery to coincidence annotations and mapper fields
    like:

    class CustomerMapper(BaseMapper):
        name = Column(String, nullable=False)
        first_name = Column(String, nullable=True)


    class CustomerQuery(BaseQuery):
        name: str
        first_name: Optional[str]

        class Meta:
            mapper = CustomerMapper
    """
    pass
