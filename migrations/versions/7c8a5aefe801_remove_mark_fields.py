"""remove mark fields

Revision ID: 7c8a5aefe801
Revises: a41f004cad1a
Create Date: 2023-05-25 15:44:06.072076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7c8a5aefe801"
down_revision = "a41f004cad1a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.drop_column("marked")

    with op.batch_alter_table("interpretations", schema=None) as batch_op:
        batch_op.drop_column("marked")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("interpretations", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("marked", sa.BOOLEAN(), autoincrement=False, nullable=True)
        )

    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("marked", sa.BOOLEAN(), autoincrement=False, nullable=True)
        )

    # ### end Alembic commands ###
