"""created azure is active

Revision ID: 15c8a7f71120
Revises: 342856222981
Create Date: 2023-10-22 23:03:45.377785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15c8a7f71120'
down_revision: Union[str, None] = '342856222981'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('azure_is_active', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patients', 'azure_is_active')
    # ### end Alembic commands ###
