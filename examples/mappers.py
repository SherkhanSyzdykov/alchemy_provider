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


class AbstractBaseMapper(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())


class CustomerMapper(AbstractBaseMapper):
    __tablename__ = 'customer'

    username = Column(String(250), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    first_name = Column(String(250))
    last_name = Column(String(250))
    description = Column(String(250))

    parent_id = Column(
        BigInteger,
        ForeignKey(f'{__tablename__}.id', ondelete='SET NULL'),
        index=True
    )
    parent = relationship('CustomerMapper')

    created_meter_inlines = relationship(
        'MeterInlineMapper', back_populates='created_by',
        foreign_keys='MeterInlineMapper.created_by_id'
    )
    updated_meter_inlines = relationship(
        'MeterInlineMapper', back_populates='updated_by',
        foreign_keys='MeterInlineMapper.updated_by_id'
    )


class MeterTypeResourceMapper(Base):
    __tablename__ = 'meter_type_resource_m2m'

    meter_type_id = Column(
        BigInteger,
        ForeignKey('meter_type.id', ondelete='CASCADE'),
        index=True, nullable=False
    )
    resource_id = Column(
        BigInteger,
        ForeignKey('resource.id', ondelete='CASCADE'),
        index=True, nullable=False
    )

    __table_args__ = PrimaryKeyConstraint(
        meter_type_id, resource_id,
        'meter_type_id_resource_id_primary_key_constraint'
    )


class ResourceMapper(AbstractBaseMapper):
    __tablename__ = 'resource'

    name = Column(String(255), nullable=False, unique=True)
    has_rate = Column(Boolean, nullable=False, default=True)

    meter_types = relationship(
        'MeterTypeMapper',
        secondary=MeterTypeResourceMapper.__table__,
        back_populates='resources'
    )


class MeterTypeMapper(AbstractBaseMapper):
    __tablename__ = 'meter_type'

    name = Column(String(255), nullable=False, unique=True)
    description = Column(String)

    meters = relationship('MeterInlineMapper', back_populates='meter_type')
    resources = relationship(
        'ResourceMapper',
        secondary=MeterTypeResourceMapper.__table__,
        back_populates='meter_types'
    )


class MeterInlineMapper(AbstractBaseMapper):
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
    parent = relationship('MeterInlineMapper', lazy='joined')

    meter_type_id = Column(
        BigInteger,
        ForeignKey(
            f'{MeterTypeMapper.__tablename__}.{MeterTypeMapper.id.name}',
            ondelete='CASCADE'
        ),
        nullable=False,
    )
    meter_type = relationship(
        'MeterTypeMapper',
        back_populates='meters',
        # lazy='joined'
    )

    created_by_id = Column(
        BigInteger,
        ForeignKey(f'{CustomerMapper.__tablename__}.id'),
        nullable=False
    )
    updated_by_id = Column(
        BigInteger,
        ForeignKey(f'{CustomerMapper.__tablename__}.id')
    )
    created_by = relationship(
        'CustomerMapper', foreign_keys=[created_by_id],
        back_populates='created_meter_inlines'
    )
    updated_by = relationship(
        'CustomerMapper',
        foreign_keys=[updated_by_id],
        back_populates='updated_meter_inlines'
    )
