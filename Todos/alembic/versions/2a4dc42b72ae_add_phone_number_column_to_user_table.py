"""Add phone number column to user table

Revision ID: 2a4dc42b72ae
Revises: 
Create Date: 2025-01-25 12:08:28.394166

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '2a4dc42b72ae'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('User', sa.Column('phone_number', sa.String(), nullable=True))

    # Populate the column with initial values
    op.execute(
        """
        UPDATE public."User"
        SET phone_number = '000-000-0000'
        """
    )

    # Optionally, set the column to NOT NULL if all rows have been populated
    op.alter_column('User', 'phone_number', nullable=False)


def downgrade() -> None:
    op.drop_column('User', 'phone_number')
