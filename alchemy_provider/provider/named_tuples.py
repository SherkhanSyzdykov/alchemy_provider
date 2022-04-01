from typing import NamedTuple
from .models import MeterInlineModel


class BaseQuery(NamedTuple):
    class Meta:
        mapper = MeterInlineModel

    name: str
