from __future__ import annotations
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Boolean,
    ForeignKey,
    PrimaryKeyConstraint,
    Table
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class AbstractBaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True)


class CustomerModel(AbstractBaseModel):
    __tablename__ = 'customer'

    username = Column(String(250), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(250), nullable=False)

    created_meter_inlines = relationship(
        'MeterInlineModel', back_populates='created_by',
        foreign_keys='MeterInlineModel.created_by_id'
    )
    updated_meter_inlines = relationship(
        'MeterInlineModel', back_populates='updated_by',
        foreign_keys='MeterInlineModel.updated_by_id'
    )


# class MeterTypeResourceAssocModel(Base):
#     __tablename__ = 'meter_type_resource_assoc'
#
#     meter_type_id = Column(
#         BigInteger,
#         ForeignKey(
#             f'meter_type.id',
#             ondelete='CASCADE',
#         ),
#         nullable=False,
#         index=True
#     )
#     meter_type = relationship('MeterTypeModel', back_populates='resources')
#
#     resource_id = Column(
#         BigInteger,
#         ForeignKey(
#             f'resource.id',
#             ondelete='CASCADE',
#         ),
#         nullable=False,
#         index=True
#     )
#     resource = relationship('ResourceModel', back_populates='meter_types')
#
#     __table_args__ = PrimaryKeyConstraint(
#         'meter_type_id', 'resource_id',
#         name='meter_type_resource_pk_constraint'
#     ),


meter_type_resource_assoc_table = Table(
    'meter_type_resource_assoc',
    Base.metadata,
    Column('resource_id', BigInteger,
           ForeignKey('resource.id', ondelete='CASCADE'),
           index=True, nullable=False),
    Column('meter_type_id', BigInteger,
           ForeignKey('meter_type.id', ondelete='CASCADE'),
           index=True, nullable=False)
)


class ResourceModel(AbstractBaseModel):
    __tablename__ = 'resource'

    name = Column(String(255), nullable=False, unique=True)
    has_rate = Column(Boolean, nullable=False, default=True)

    meter_types = relationship(
        'MeterTypeModel',
        secondary=meter_type_resource_assoc_table,
        back_populates='resources'
    )


class MeterTypeModel(AbstractBaseModel):
    __tablename__ = 'meter_type'

    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)

    meters = relationship('MeterInlineModel', back_populates='meter_type')
    resources = relationship(
        'ResourceModel',
        secondary=meter_type_resource_assoc_table,
        back_populates='meter_types'
    )


class MeterInlineModel(AbstractBaseModel):
    __tablename__ = 'meter_inline'

    serial_number = Column(String(255), nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, default=True)

    parent_id = Column(
        BigInteger,
        ForeignKey(
            f'{__tablename__}.id',
            ondelete='CASCADE'
        ),
    )
    parent = relationship('MeterInlineModel', lazy='joined')

    meter_type_id = Column(
        BigInteger,
        ForeignKey(
            f'{MeterTypeModel.__tablename__}.{MeterTypeModel.id.name}',
            ondelete='CASCADE'
        ),
        nullable=False,
    )
    meter_type = relationship(
        'MeterTypeModel',
        back_populates='meters',
        # lazy='joined'
    )

    created_by_id = Column(
        BigInteger,
        ForeignKey(f'{CustomerModel.__tablename__}.id'),
        nullable=False
    )
    updated_by_id = Column(
        BigInteger,
        ForeignKey(f'{CustomerModel.__tablename__}.id')
    )
    created_by = relationship(
        'CustomerModel', foreign_keys=[created_by_id],
        back_populates='created_meter_inlines'
    )
    updated_by = relationship(
        'CustomerModel',
        foreign_keys=[updated_by_id],
        back_populates='updated_meter_inlines'
    )
