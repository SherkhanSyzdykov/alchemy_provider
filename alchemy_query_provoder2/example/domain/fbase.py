from datetime import datetime
from typing import Mapping
from pydantic import Extra, root_validator
from .base import BaseDomain


class FBase(BaseDomain, Mapping):
    """
    """
    class Config:
        extra = Extra.allow

    def __iter__(self):
        for k, _ in BaseDomain._iter(self, exclude_unset=True):
            yield k

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, item):
        return getattr(self, item)

    @root_validator(pre=True)
    def convert_isoformat_to_datetime(cls, values):
        for key, value in values.items():
            try:
                values[key] = datetime.fromisoformat(value)
            except:
                pass

        return values
