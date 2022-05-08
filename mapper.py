from uuid import uuid4
from sqlalchemy import *
from sqlalchemy.orm import relationship, validates, declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY


Base = declarative_base()


class AbstractMapper(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True,
                nullable=False)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4,
                  unique=True, nullable=False)


class Customer(AbstractMapper):
    __tablename__ = 'ami_customer'

    name = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, index=True) # TODO validation
    description = Column(String(255))
    type = Column(SmallInteger(), nullable=False, default=0)
    team = Column(SmallInteger(), nullable=False, default=0)
    first_name = Column(String(150))
    last_name = Column(String(150))
    password = Column(String(128), nullable=False) # TODO validation

    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)

    last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    date_joined = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    parent_id = Column(BigInteger, ForeignKey(f'{__tablename__}.id'))
    children = relationship('Customer')

    __table_args__ = (
        UniqueConstraint('email', 'team', name='unique_email_and_team'),
        CheckConstraint(id != parent_id, name='id not equal to parent_id')
    )
    # history = HistoricalRecords()


class DeviceType(AbstractMapper):
    __tablename__ = 'ami_device_type'

    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    capability = Column(JSON, default=dict())


class Resource(AbstractMapper):
    __tablename__ = 'ami_resource'

    name = Column(String(255), unique=True, nullable=False)
    parameters = Column(JSON)
    icon = Column(String(255))
    has_rate = Column(Boolean, nullable=False, default=True)
    category = Column(SmallInteger, default=0)


class Field(AbstractMapper):
    __tablename__ = 'ami_field'

    name = Column(String(255), nullable=False)
    value_type = Column(SmallInteger, nullable=False, default=0)


class MeterType(AbstractMapper):
    __tablename__ = 'ami_meter_type'

    name = Column(String(255), nullable=False, unique=True)
    coefficient = Column(Float)
    unit_of_measurement = Column(String(100))
    multiplier = Column(Float)
    description = Column(String(255))
    parameters = Column(JSON)


class MountEvent(AbstractMapper):
    __tablename__ = 'ami_mount_event'

    directory = Column(JSON)
    meter_inline = Column(JSON)
    device = Column(JSON)

    device_type_id = Column(BigInteger)
    device_type = relationship(
        'DeviceType', primaryjoin='foreign(MountEvent.device_type_id) == DeviceType.id')

    resource_id = Column(BigInteger)
    resource = relationship(
        'Resource', primaryjoin='foreign(MountEvent.resource_id) == Resource.id')

    field_id = Column(BigInteger)
    field = relationship(
        'Field', primaryjoin='foreign(MountEvent.field_id) == Field.id')

    meter_type_id = Column(BigInteger)
    meter_type = relationship(
        'MeterType', primaryjoin='foreign(MountEvent.meter_type_id) == MeterType.id')

    status = Column(SmallInteger, nullable=False, default=0)
    event_type = Column(SmallInteger, nullable=False, default=0)

    mounted_datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated_datetime = Column(DateTime(timezone=True), server_default=None)

    mounted_by_id = Column(
        BigInteger, ForeignKey(f'{Customer.__tablename__}.id'), nullable=False)

    updated_by_id = Column(
        BigInteger, ForeignKey(f'{Customer.__tablename__}.id'))

    mounted_by = relationship('Customer', foreign_keys=[mounted_by_id])

    updated_by = relationship('Customer', foreign_keys=[updated_by_id])
