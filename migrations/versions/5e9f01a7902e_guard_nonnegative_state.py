"""guard_nonnegative_state

Revision ID: 5e9f01a7902e
Revises:
Create Date: 2026-11-16 20:24:01.169610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e9f01a7902e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_check_constraint(
        "ck_users_balance_nonnegative",
        "users",
        "balance >= 0",
    )

    op.create_check_constraint(
        "ck_products_stock_nonnegative",
        "products",
        "stock >= 0",
    )


def downgrade():
    op.drop_constraint(
        "ck_products_stock_nonnegative",
        "products",
        type_="check",
    )

    op.drop_constraint(
        "ck_users_balance_nonnegative",
        "users",
        type_="check",
    )
