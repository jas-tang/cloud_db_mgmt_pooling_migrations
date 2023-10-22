"""created is active

Revision ID: e31e6d5e4817
Revises: 4ddf04bb5782
Create Date: 2023-10-22 22:36:54.762000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e31e6d5e4817'
down_revision: Union[str, None] = '4ddf04bb5782'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('is_active', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patients', 'is_active')
    # ### end Alembic commands ###
