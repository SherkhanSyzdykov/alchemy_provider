class BaseService:
    pass


class CustomerService(BaseService):
    async def get_one(
        self,
        query: BaseService
    ):
        pass

    async def get_multi(self):
        pass

