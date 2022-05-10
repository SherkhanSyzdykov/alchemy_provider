import asyncio
from typing import Awaitable, Union, List, Sequence, Tuple


async def run_concurrently(
    *aws: Awaitable
) -> Union[Sequence, List, Tuple]:
    """
    To avoid transaction exception that can be raised with running
    request to db concurrently
    """
    result = await asyncio.gather(*aws, return_exceptions=False)
    for item in result:
        if isinstance(item, BaseException):
            raise item

    return result
