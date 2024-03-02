"""empty message

Revision ID: 9a88efaf8340
Revises: 5736f461d59c
Create Date: 2023-10-04 09:39:09.995200

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "9a88efaf8340"
down_revision = "5736f461d59c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "asistencia",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "userasistencia",
        sa.Column("asistencia_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["asistencia_id"],
            ["asistencia.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("asistencia_id", "user_id"),
    )
    with op.batch_alter_table("qr", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=False,
            autoincrement=True,
        )

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=False,
            autoincrement=True,
        )
        batch_op.create_unique_constraint(None, ["correo"])


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="unique")
        batch_op.alter_column(
            "id",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=False,
            autoincrement=True,
        )

    with op.batch_alter_table("qr", schema=None) as batch_op:
        batch_op.alter_column(
            "id",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=False,
            autoincrement=True,
        )

    op.drop_table("userasistencia")
    op.drop_table("asistencia")
