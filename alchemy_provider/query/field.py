from typing import Any, Callable, Optional


class Field:
    _adapter: Optional[Callable[[Any], Any]] = None

    def __init__(
        self,
        adapter: Optional[Callable[[Any], Any]] = None,
    ):
        self._adapter = adapter

    def __call__(self, value: Any) -> Any:
        if self._adapter is not None:
            return self._adapter(value)

        return value
