from asyncio import iscoroutine
from typing import Any, Callable, Coroutine, Union


class AdapterField:
    _adapter: Union[
        Callable[[Any], Any],
        Callable[[Any], Coroutine[Any, None, None]]
    ]

    def __init__(
        self,
        adapter: Union[
            Callable[[Any], Any],
            Callable[[Any], Coroutine[Any, None, None]]
        ],
    ):
        self._adapter = adapter

    async def __call__(self, value: Any) -> Any:
        result = self._adapter(value)
        if iscoroutine(result):
            return await result

        return result
