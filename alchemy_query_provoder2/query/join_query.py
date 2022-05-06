from .base import BaseQuery


class JoinStrategy:
    is_outer: bool = False
    is_full: bool = False

    def __init__(self, is_outer: bool = False, is_full: bool = False):
        self.is_outer = is_outer
        self.is_full = is_full


class JoinQuery(BaseQuery):
    @classmethod
    def get_join_strategy(cls, field_name: str):
        class_ = cls
        if isinstance(cls, BaseQuery):
            class_ = cls.__class__

        return getattr(class_, field_name, JoinStrategy())
