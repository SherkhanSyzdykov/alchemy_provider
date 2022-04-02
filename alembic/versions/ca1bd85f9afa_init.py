"""init

Revision ID: ca1bd85f9afa
Revises: 
Create Date: 2022-04-02 18:40:53.883651

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ca1bd85f9afa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meter_type',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', 'uuid'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('resource',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('has_rate', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'uuid'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('meter_inline',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('serial_number', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('parent_id', sa.BigInteger(), nullable=True),
    sa.Column('meter_type_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['meter_type_id'], ['meter_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_id'], ['meter_inline.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'uuid'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_meter_inline_serial_number'), 'meter_inline', ['serial_number'], unique=False)
    op.create_table('meter_type_resource_assoc',
    sa.Column('meter_type_id', sa.BigInteger(), nullable=False),
    sa.Column('resource_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['meter_type_id'], ['meter_type.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('meter_type_id', 'resource_id', name='meter_type_resource_pk_constraint')
    )
    op.create_index(op.f('ix_meter_type_resource_assoc_meter_type_id'), 'meter_type_resource_assoc', ['meter_type_id'], unique=False)
    op.create_index(op.f('ix_meter_type_resource_assoc_resource_id'), 'meter_type_resource_assoc', ['resource_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_meter_type_resource_assoc_resource_id'), table_name='meter_type_resource_assoc')
    op.drop_index(op.f('ix_meter_type_resource_assoc_meter_type_id'), table_name='meter_type_resource_assoc')
    op.drop_table('meter_type_resource_assoc')
    op.drop_index(op.f('ix_meter_inline_serial_number'), table_name='meter_inline')
    op.drop_table('meter_inline')
    op.drop_table('resource')
    op.drop_table('meter_type')
    # ### end Alembic commands ###
