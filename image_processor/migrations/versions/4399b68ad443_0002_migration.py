"""0002_migration

Revision ID: 4399b68ad443
Revises: 4de08b1f01d6
Create Date: 2024-11-03 22:18:13.706343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4399b68ad443'
down_revision: Union[str, None] = '4de08b1f01d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('file_path', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('upload_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('resolution', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('size', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='images_pkey'),
    sa.UniqueConstraint('file_path', name='images_file_path_key')
    )
    op.drop_table('users')
    # ### end Alembic commands ###
