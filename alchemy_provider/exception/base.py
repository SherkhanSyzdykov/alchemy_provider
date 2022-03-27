"""
Implements base exception for AlchemyProvider
"""
from typing import Union
import orjson


class BaseProviderException(BaseException):
    DEFAULT_DETAIL = 'Something went wrong'
    DEFAULT_CODE = 'Error'

    detail: str = DEFAULT_DETAIL
    code: Union[str, int] = DEFAULT_CODE

    def __init__(
        self,
        detail: str = DEFAULT_DETAIL,
        code: Union[str, int] = DEFAULT_CODE
    ):
        self.detail = detail
        self.code = code

    @property
    def dict(self) -> dict[str, Union[str, int]]:
        return {
            'detail': self.detail,
            'code': self.code
        }

    @property
    def json(self) -> str:
        return orjson.dumps(self.dict).decode('utf-8')

    @property
    def jsonb(self) -> bytes:
        return orjson.dumps(self.dict)
