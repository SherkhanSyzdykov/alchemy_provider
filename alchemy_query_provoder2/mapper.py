from __future__ import annotations
from uuid import uuid4
from sqlalchemy import Column, String, BigInteger, ForeignKey, Boolean, \
    DateTime, PrimaryKeyConstraint, Float, SmallInteger, func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID as PS_UUID


Base = declarative_base()


class AbstractBaseMapper(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(PS_UUID(as_uuid=True), primary_key=True, default=uuid4())


class MeterTypeResource(Base):
    __tablename__ = 'meter_type_resource_m2m'

    meter_type_id = Column(
        BigInteger,
        ForeignKey('meter_type.id', ondelete='CASCADE'),
        nullable=False
    )
    resource_id = Column(
        BigInteger,
        ForeignKey('resource.id', ondelete='CASCADE'),
        nullable=False
    )

    __table_args__ = PrimaryKeyConstraint(
        meter_type_id, resource_id,
        name='meter_type_resource_pk'
    ),


class MeterType(AbstractBaseMapper):
    __tablename__ = 'meter_type'

    name = Column(String(255), nullable=False, unique=True)
    coefficient = Column(Float)
    unit_of_measurement = Column(String(100))
    multiplier = Column(Float)
    description = Column(String(255))
    parameters = Column(JSONB)

    resources = relationship(
        'Resource',
        secondary=MeterTypeResource.__table__,
        back_populates='meter_types'
    )


class Resource(AbstractBaseMapper):
    __tablename__ = 'resource'

    name = Column(String(255), unique=True, nullable=False)
    parameters = Column(JSONB)
    icon = Column(String(255))
    has_rate = Column(Boolean, nullable=False, default=True)
    category = Column(SmallInteger, default=0)

    meter_types = relationship(
        'MeterType',
        secondary=MeterTypeResource.__table__,
        back_populates='resources'
    )


class CustomerDevice(Base):
    __tablename__ = 'customer_device_m2m'

    customer_id = Column(
        BigInteger,
        ForeignKey('customer.id', ondelete='CASCADE'),
        nullable=False
    )
    device_id = Column(
        BigInteger,
        ForeignKey('device.id', ondelete='CASCADE'),
        nullable=False
    )

    __table_args__ = PrimaryKeyConstraint(
        customer_id, device_id,
        name='customer_device_pk'
    ),


class Customer(AbstractBaseMapper):
    __tablename__ = 'customer'

    name = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, index=True)  # TODO validation
    description = Column(String(255))
    type = Column(SmallInteger(), nullable=False, default=0)
    team = Column(SmallInteger(), nullable=False, default=0)
    first_name = Column(String(150))
    last_name = Column(String(150))
    password = Column(String(128), nullable=False)  # TODO validation

    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)

    last_activity = Column(DateTime(timezone=True),
                           onupdate=func.now())
    date_joined = Column(DateTime(timezone=0),
                         server_default=func.now(), nullable=False)

    parent_id = Column(BigInteger, ForeignKey(f'{__tablename__}.id'))
    children = relationship('Customer')

    devices = relationship(
        'Device',
        secondary=CustomerDevice.__table__,
        back_populates='customers'
    )


class DeviceType(AbstractBaseMapper):
    __tablename__ = 'device_type'

    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    capability = Column(JSONB, default=dict())

    devices = relationship('Device', back_populates='device_type')


class Device(AbstractBaseMapper):
    __tablename__ = 'device'

    eui = Column(String(16), nullable=False, index=True)
    dev_addr = Column(String(8), index=True)
    description = Column(String(255))
    parameters = Column(JSONB)
    active = Column(Boolean, nullable=False, default=True)
    new_fw_timestamp = Column(Boolean, nullable=False, default=True)

    device_type_id = Column(
        BigInteger,
        ForeignKey('device_type.id', ondelete='SET NULL')
    )
    device_type = relationship('DeviceType', back_populates='devices')

    customers = relationship(
        'Customer',
        secondary=CustomerDevice.__table__,
        back_populates='devices'
    )


from sqlalchemy import update

update_stmt = update(Device)
