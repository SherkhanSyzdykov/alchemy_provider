import asyncio
from alchemy_provider.query_provider import *
from examples.queries import *
from pydantic import BaseModel


async def main():
    pass
    # stmt1 = Provider.get_select_stmt(MeterInlineMeterTypeQuery)
    # stmt2 = Provider.get_select_stmt(MeterInlineMeterTypeResourcesQuery)
    #
    # print()
    # print(stmt1)
    # print()
    # print(stmt2)
    # print()


asyncio.run(main())
