from typing import Type, Union, TypedDict, is_typeddict, Dict
from sqlalchemy import *
from sqlalchemy.sql import Select
from sqlalchemy.orm import DeclarativeMeta, RelationshipProperty, ColumnProperty
from alchemy_provider.provider.examples import *



class ModelAttributeException(BaseException):
    ...



class Provider:
    _query: Union[Type[BaseQuery], BaseQuery]

    def __init__(self,query: Union[Type[BaseQuery], BaseQuery]):
        self._query = query

    @property
    def get_query(self) -> Union[Type[BaseQuery], BaseQuery]:
        return self._query

    def _inner_join(
        self,
        select_stmt: Select,
        query: Union[Type[BaseQuery], BaseQuery],
    ) -> Select:
        """
        select_stmt: select(test_model1.id, test_model1.name)
        query:
        class Test2(BaseQuery):
            start_time: datetime

            class Meta:
                model = test_model2

        return: select(
        test_model1.id, test_model1.name, test_model2.start_time
        ).innerjoin(test_model2, test_model1.related_field_pk = test_model2.pk)
        """
        model = query.get_model

        for field in self.get_query.__annotations__:
            model_field = getattr(model, field, None)
            if isinstance(model_field.property, ColumnProperty):
                select_stmt.add_columns(model_field)


    def _outer_join(
        self,
        select_stmt: Select,
        query: TypedDict,
    ):
        """
        select_stmt: select(test_model1.id, test_model1.name)
        query:
        class Test2(BaseQuery):
            start_time: datetime

            class Meta:
                model = test_model2

        return: select(
        test_model1.id, test_model1.name, test_model2.start_time
        ).outerjoin(test_model2, test_model1.related_field_pk = test_model2.pk)
        """
        pass

    def _make_select_stmt_from_base_query_type(
        self,
    ) -> Select:
        """
        query: subclass of typing.TypedDict
        example:
        class Test(typing.TypedDict):
            name: str
            test: bool
        """
        model = self.get_query.get_model
        stmt = select()
        for field in self.get_query.__annotations__:
            model_field = getattr(model, field, None)
            if isinstance(model_field.property, ColumnProperty):
                stmt.add_columns(model_field)

            if isinstance(model_field.property, RelationshipProperty):
                related_model: DeclarativeMeta = model_field.property.mapper.class_

            stmt = stmt.add_columns()


    def _make_select_stmt(
        self,
        query: Union[Type[TypedDict], Dict]
    ) -> Select:
        """
        query: Dataclass
        example:
        @dataclass
        class Test:
            name: str

            class Meta:
                model = TestModel

        return: select(TestModel)
        """
        self._query = query
        model = self._get_model(query=query)

        stmt = select()
        for field in query.__dataclass_fields__:
            model_field = getattr(model, field)
            if isinstance(model_field.property, ColumnProperty):
                stmt.add_columns(model_field)

            if isinstance(model_field.property, RelationshipProperty):
                pass

