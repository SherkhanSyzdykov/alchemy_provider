from pydantic import BaseModel
from query import AbstractQuery


class BaseDomain(BaseModel, AbstractQuery):
    pass
