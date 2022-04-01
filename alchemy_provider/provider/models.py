from __future__ import annotations
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Boolean,
    ForeignKey,
    PrimaryKeyConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID


Base = declarative_base()


class AbstractBaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())


class ResourceModel(AbstractBaseModel):
    __tablename__ = 'resource'

    name = Column(String(255), nullable=False, unique=True)
    has_rate = Column(Boolean, nullable=False, default=True)

    meter_types = relationship(
        'MeterTypeResourceAssocModel',
        back_populates='resource'
    )


class MeterTypeModel(AbstractBaseModel):
    __tablename__ = 'meter_type'

    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)

    meters = relationship('MeterInlineModel', back_populates='meter_type')
    resources = relationship(
        'MeterTypeResourceAssocModel',
        back_populates='meter_type',
        lazy='joined'
    )


class MeterTypeResourceAssocModel(Base):
    __tablename__ = 'meter_type_resource_assoc'

    meter_type_id = Column(
        BigInteger,
        ForeignKey(
            f'{MeterTypeModel.__tablename__}.{MeterTypeModel.id.name}',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True
    )
    meter_type = relationship('MeterTypeModel', back_populates='resources')

    resource_id = Column(
        BigInteger,
        ForeignKey(
            f'{ResourceModel.__tablename__}.{ResourceModel.id.name}',
            ondelete='CASCADE',
        ),
        nullable=False,
        index=True
    )
    resource = relationship('ResourceModel', back_populates='meter_types')

    __table_args__ = PrimaryKeyConstraint(
        'meter_type_id', 'resource_id',
        name='meter_type_resource_pk_constraint'
    ),


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
        lazy='joined'
    )
