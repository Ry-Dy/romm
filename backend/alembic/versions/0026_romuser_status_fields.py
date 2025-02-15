"""empty message

Revision ID: 0026_romuser_status_fields
Revises: 0025_roms_hashes
Create Date: 2024-08-29 15:52:56.031850

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "0026_romuser_status_fields"
down_revision = "0025_roms_hashes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("collections", schema=None) as batch_op:
        batch_op.alter_column(
            "path_cover_l",
            existing_type=mysql.VARCHAR(length=1000),
            type_=sa.Text(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "path_cover_s",
            existing_type=mysql.VARCHAR(length=1000),
            type_=sa.Text(),
            existing_nullable=True,
        )

    with op.batch_alter_table("rom_user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("last_played", sa.DateTime(timezone=True), nullable=True)
        )
        batch_op.add_column(sa.Column("backlogged", sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column("now_playing", sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column("hidden", sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column("rating", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("difficulty", sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column("completion", sa.Integer(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "status",
                sa.Enum(
                    "INCOMPLETE",
                    "FINISHED",
                    "COMPLETED_100",
                    "RETIRED",
                    "NEVER_PLAYING",
                    name="romuserstatus",
                ),
                nullable=True,
            )
        )


def downgrade() -> None:
    with op.batch_alter_table("rom_user", schema=None) as batch_op:
        batch_op.drop_column("status")
        batch_op.drop_column("completion")
        batch_op.drop_column("difficulty")
        batch_op.drop_column("rating")
        batch_op.drop_column("hidden")
        batch_op.drop_column("now_playing")
        batch_op.drop_column("backlogged")
        batch_op.drop_column("last_played")

    with op.batch_alter_table("collections", schema=None) as batch_op:
        batch_op.alter_column(
            "path_cover_s",
            existing_type=sa.Text(),
            type_=mysql.VARCHAR(length=1000),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "path_cover_l",
            existing_type=sa.Text(),
            type_=mysql.VARCHAR(length=1000),
            existing_nullable=True,
        )
