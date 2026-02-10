"""add payment fields to reservations

Revision ID: 4c2af9879b2a
Revises: 17c1a971aad5
Create Date: 2026-02-07 16:29:36.212255
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c2af9879b2a'
down_revision = '17c1a971aad5'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite necesita DEFAULT para columnas NOT NULL
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'payment_method',
                sa.String(length=30),
                nullable=False,
                server_default='card'
            )
        )
        batch_op.add_column(
            sa.Column(
                'payment_status',
                sa.String(length=20),
                nullable=False,
                server_default='paid'
            )
        )

    # (opcional) quitar defaults para nuevos inserts
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.alter_column('payment_method', server_default=None)
        batch_op.alter_column('payment_status', server_default=None)


def downgrade():
    with op.batch_alter_table('reservations', schema=None) as batch_op:
        batch_op.drop_column('payment_status')
        batch_op.drop_column('payment_method')
